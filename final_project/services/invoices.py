from datetime import datetime
from typing import Optional, Tuple, List

from db import sqlite
from services import organisations as org, items as itm, clients as cl, addresses as addr
from utils.mailer import Mailer


def find_all(cols: tuple = ("*",)) -> list[tuple]:
  return sqlite.query(
    f"SELECT {','.join(cols)} FROM invoices WHERE organisation_id = ?",
    org.current(cols=("id",))
  )


def create(items: List[Tuple[int, int]], client_id: int, name: str = "", due_at: datetime = datetime.today()):
  items_ids = [id for (id, _) in items]
  items_details: list[tuple] = []
  (org_id, org_name) = org.current(cols=("id",'name'))
  inv_items = itm.find_all(ids=tuple(items_ids), cols=("id", "name", "price"))
  inv_name: str = name if name else f"Invoice - from {org_name}"
  total = float(0)

  for (id1, name, price) in inv_items:
    for (id2, qty) in items:
      if id1 == id2:
        item_total = price * float(qty)
        total += item_total
        items_details.append((name, id2, qty, price, item_total))

  inv_sql: str = """
    INSERT INTO invoices (name, total, client_id, organisation_id, due_at)
    VALUES (?, ?, ?, ?, ?)"""

  (curs, _) = sqlite.exec(inv_sql, (inv_name, total, client_id, org_id, due_at.strftime("%Y-%m-%d %H:%M:%S")))
  invoice_id = curs.lastrowid

  li_sql: str = """
    INSERT INTO line_items (name, quantity, price, total, item_id, invoice_id, organisation_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)"""

  for (name, item_id, qty, price, total) in items_details:
    sqlite.exec(li_sql, (name, qty, price, total, item_id, invoice_id, org_id))


def find_by_id(id: int, cols: tuple = ("*",), required: bool = False) -> Optional[Tuple]:
  (org_id,) = org.current(cols=("id",))

  organisation: Optional[Tuple] = sqlite.query_one(
    f"SELECT {','.join(cols)} FROM invoices WHERE id = ? AND organisation_id = ? LIMIT 1",
    (id, org_id)
  )

  if required and organisation is None:
    raise ValueError(f"Invoice id ({id}), was not found.")

  return organisation


def update(id: int, sent_at: datetime | None = None, paid_at: datetime | None = None):
  updates: list[str] = []
  values: tuple = ()

  if sent_at:
    updates.append("sent_at = ?")
    values += (sent_at.strftime("%Y-%m-%d %H:%M:%S"),)

  if paid_at:
    updates.append("paid_at = ?")
    values += (paid_at.strftime("%Y-%m-%d %H:%M:%S"),)

  values += (id,)

  sqlite.exec(f"UPDATE invoices SET {','.join(updates)} WHERE id = ?", values)


def get_line_items(id: int, organisation_id: int, cols: Tuple = ("*",)) -> List[Tuple]:
  return sqlite.query(
    f"SELECT {','.join(cols)} FROM line_items WHERE invoice_id = ? AND organisation_id = ?",
    (id, organisation_id)
  )


def generate(id: int) -> list[str]:
  inv_info: dict = get_invoice_info(id)
  return org.get_plugin(inv_info["org_id"]).gen(inv_info)


def send(id: int):
  inv_info: dict = get_invoice_info(id)
  mail = org.find_by_id(inv_info["org_id"], cols=("mail_host", "mail_port", "mail_user", "mail_pwrd"), required=True)
  (host, port, user, pwrd) = (None, None, None, None) if mail is None else mail

  sender: str = inv_info["org_email"]
  receipient: str = inv_info["client_email"]
  subject: str = inv_info["name"]

  if not (host or port or user or pwrd or sender or receipient):
    raise ValueError("Mail not properly configured")

  plugin = org.get_plugin(inv_info["org_id"])
  text: str = "" if not plugin.email_text else plugin.email_text(inv_info)
  html: str = "" if not plugin.email_html else plugin.email_html(inv_info)
  files: list[str] = plugin.gen(inv_info)
  mailer: Mailer = Mailer(host, port, user, pwrd)

  mailer.send(sender, receipient, subject, text, html, files)
  # update invoice sent_at datetime column
  update(id, sent_at=datetime.now())


def mark_as_paid(id: int, date: Optional[datetime] = None):
  update(id, paid_at=date or datetime.now())


def get_invoice_info(id: int) -> dict:
  organisation: Tuple = org.current(cols=("id", "name", "email", "phone", "address_id"))
  invoice: Optional[Tuple] = find_by_id(id, cols=("id", "name", "total", "client_id", "organisation_id", "created_at", "due_at"))

  if not invoice:
    raise ValueError("No invoice")

  client: Optional[Tuple] = cl.find_by_id(invoice[3], cols=("billing_address_id", "shipping_address_id", "name", "email", "phone"))

  if not client:
    raise ValueError("No client")

  line_items: List[Tuple] = get_line_items(id, invoice[4])
  org_addr: Optional[Tuple] = addr.find_by_id(organisation[4])
  ba: Optional[Tuple] = addr.find_by_id(client[0]) if client else None
  sa: Optional[Tuple] = addr.find_by_id(client[1]) if ba and client[0] != client[1] else ba

  inv_info: dict = {
    "id": id,
    "num": id,
    "name": invoice[1],
    "total": invoice[2],
    "created_at": invoice[5],
    "due_at": invoice[6],
    "items": [
      {
        "id": id,
       "name": name,
       "price": price,
       "qty": qty,
       "total": total,
       "item_id": item_id,
       "created_at": created_at,
       "updated_at": updated_at
      } for (id, name, price, qty, total, item_id, client_id, org_id, created_at, updated_at) in line_items
    ],
    "org_id": organisation[0],
    "org_name": organisation[1],
    "org_email": organisation[2],
    "org_phone": organisation[3],
    "address": {
      "street": org_addr[1],
      "city": org_addr[2],
      "state": org_addr[3],
      "country": org_addr[4],
      "postcode": org_addr[5],
    } if org_addr is not None else None,
    "client_name": client[2],
    "client_email": client[3],
    "client_phone": client[4],
    "billing_address": {
      "street": ba[1],
      "city": ba[2],
      "state": ba[3],
      "country": ba[4],
      "postcode": ba[5],
    } if ba is not None else None,
    "shipping_address": {
      "street": sa[1],
      "city": sa[2],
      "state": sa[3],
      "country": sa[4],
      "postcode": sa[5],
    } if sa is not None else None
  }

  inv_info["num"] = org.get_plugin(organisation[0]).num(inv_info)

  return inv_info
