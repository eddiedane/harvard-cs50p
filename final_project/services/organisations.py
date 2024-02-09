from sqlite3 import Connection, Cursor, Row
from importlib import import_module
from db import sqlite
from services import addresses as addr


def create(name: str, email: str, phone: str = "", mail_config: tuple = (), plugin: str = "default") -> None:
  set_inactive()

  opts_cols: str = ", mail_host, mail_port, mail_user, mail_pwrd" if len(mail_config) == 4 else ""
  opts_params: str = ", ?" * 4 if len(mail_config) == 4 else ""

  sql: str = f"""
    INSERT INTO organisations (name, email, phone, active, plugin{opts_cols})
    VALUES (?, ?, ?, ?, ?{opts_params})"""

  sqlite.exec(sql, (name, email, phone, 1, plugin) + mail_config)


def update(
    id: int | None = None,
    name: str | None = None,
    address_id: int | None = None,
    email: str | None = None,
    phone: str | None = None,
    mail_config: tuple = (),
    plugin: str | None = None
  ) -> None:
  updates: list = []
  values: tuple = ()

  if id is None:
    (org_id,) = current(cols=("id",))
    id = org_id

  if name is not None:
    updates.append("name = ?")
    values += (name,)

  if address_id and addr.find_by_id(address_id):
    updates.append("address_id = ?")
    values += (address_id,)

  if email is not None:
    updates.append("email = ?")
    values += (email,)

  if phone is not None:
    updates.append("phone = ?")
    values += (phone,)

  if len(mail_config) == 4:
    updates.append("mail_host = ?")
    updates.append("mail_port = ?")
    updates.append("mail_user = ?")
    updates.append("mail_pwrd = ?")
    values += mail_config

  if plugin is not None:
    updates.append("plugin = ?")
    values += (plugin,)

  values += (id,)

  if len(values) > 1:
    sqlite.exec(f"UPDATE organisations SET {','.join(updates)} WHERE id = ?", values)


def find_by_id(id: int, cols: tuple = ("*",), required: bool = False) -> tuple | None:
  org: tuple | None = sqlite.query_one(
    f"SELECT {','.join(cols)} FROM organisations WHERE id = ? LIMIT 1",
    (id,)
  )

  if required and org is None:
    raise ValueError(f"Organisation id ({id}), was not found")

  return org


def find_all(cols: tuple[str] = ("*",)) -> list[tuple]:
  conn: Connection = sqlite.connect()
  cur: Cursor = conn.cursor()

  return cur.execute(f"SELECT {','.join(cols)} FROM organisations ORDER BY id").fetchall()


def set_active(id: int) -> None:
  set_inactive()
  sqlite.exec("UPDATE organisations SET active = ? WHERE id = ?", (1, id))


def set_inactive() -> None:
  sqlite.exec("UPDATE organisations SET active = FALSE")


def current(id: int = 0, cols: tuple = ("id", "name")) -> tuple:
  if id: set_active(id)

  org = sqlite.query_one(f"SELECT {','.join(cols)} FROM organisations WHERE active = TRUE LIMIT 1")

  if not org: raise ValueError("No active organisation set")

  return org


def get_plugin(id: int):
  result = find_by_id(id, cols=("plugin",), required=True)
  plugin = "default" if result is None else result[0]

  try:
    return import_module(f"plugins.{plugin}.gen")
  except Exception:
    return import_module("plugins.default.gen")
