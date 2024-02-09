from db import sqlite
from services import organisations as org

def find_all(ids: tuple = (), cols: tuple = ("*",)) -> list[tuple]:
  conds: str = f"id IN ({','.join([str(id) for id in ids])}) AND" if len(ids) else ""

  return sqlite.query(
    f"SELECT {','.join(cols)} FROM items WHERE {conds} organisation_id = ?",
    org.current(cols=("id",))
  )


def find_by_id(id: int, cols: tuple[str] = ("*",)) -> tuple | None:
  (org_id,) = org.current(cols=("id",))

  return sqlite.query_one(
    f"SELECT {','.join(cols)} FROM items WHERE id = ? AND organisation_id = ? LIMIT 1",
    (id, org_id)
  )


def create(name: str, description: str, price: float, type: str = "goods", uom: str = "piece") -> None:
  (org_id,) = org.current(cols=("id",))
  sql: str = """
    INSERT INTO items (name, description, price, type, uom, organisation_id)
    VALUES (?, ?, ?, ?, ?, ?)"""

  sqlite.exec(sql, (name, description, price, type, uom, org_id))
