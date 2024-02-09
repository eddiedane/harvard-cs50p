from typing import Optional, Tuple

from db import sqlite
import services.organisations as org
import services.addresses as addr

def create(
    name: str,
    email: str,
    phone: str | None = None,
    billing_address_id: int | None = None,
    shipping_address_id: int | None = None,
  ) -> Optional[int]:
  (org_id,) = org.current(cols=("id",))
  cols: Tuple = ("name", "organisation_id")
  vals: Tuple = (name, org_id)

  if billing_address_id and addr.find_by_id(billing_address_id):
    cols += ("billing_address_id",)
    vals += (billing_address_id,)

  if shipping_address_id and addr.find_by_id(shipping_address_id):
    cols += ("shipping_address_id",)
    vals += (shipping_address_id,)

  if email:
    cols += ("email",)
    vals += (email,)

  if phone:
    cols += ("phone",)
    vals += (phone,)

  sql = f"INSERT INTO clients {cols} VALUES ({', '.join(['?'] * len(vals))})"
  (curs, _) = sqlite.exec(sql, vals)

  return curs.lastrowid


def update(
    id: int | None,
    name: str | None = None,
    billing_address_id: int | None = None,
    shipping_address_id: int | None = None
  ) -> None:
  updates: list[str] = []
  values: tuple = ()

  if billing_address_id and addr.find_by_id(billing_address_id):
    updates.append("billing_address_id = ?")
    values += (billing_address_id,)

  if shipping_address_id and addr.find_by_id(shipping_address_id):
    updates.append("shipping_address_id = ?")
    values += (shipping_address_id,)

  if name is not None:
    updates.append("name = ?")
    values += (name,)

  values += (id,)

  sqlite.exec(f"UPDATE clients SET {','.join(updates)} WHERE id = ?", values)


def find_all(order_by:tuple = ("id",), cols: tuple = ("id", "name")) -> list[tuple]:
  sql = f"SELECT {','.join(cols)} FROM clients WHERE organisation_id = ? ORDER BY {','.join(order_by)}"

  return sqlite.query(sql, org.current(cols=("id",)))


def find_by_id(id: int, cols: tuple = ("*",)) -> Optional[Tuple]:
  (org_id,) = org.current(cols=("id",))

  return sqlite.query_one(
    f"SELECT {','.join(cols)} FROM clients WHERE id = ? AND organisation_id = ? LIMIT 1",
    (id, org_id)
  )


# def get_addresses(id: int) -> tuple[tuple]:
#   sql = f"""
#     SELECT *
#     FROM addresses
#     JOIN clients
#       ON clients.billing_address_id = addresses.id
#         OR clients.shipping_address_id = addresses.id
#     WHERE clients.id = ?
#   """