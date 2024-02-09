from typing import Optional, Tuple

from services import organisations as org
from db import sqlite

def create(
    street: str = "",
    city: str = "",
    state: str = "",
    country: str = "",
    postcode: str = ""
  ) -> Optional[int]:
  (org_id,) = org.current(cols=("id",))
  sql: str = """
    INSERT INTO addresses (street, city, state, country, postcode, organisation_id)
    VALUES (?, ?, ?, ?, ?, ?)"""

  (curs, _) = sqlite.exec(sql, (street, city, state, country, postcode, org_id))

  return curs.lastrowid


def find_all(order_by:tuple[str] = ("id",), cols: tuple[str] = ("*",)) -> list[tuple]:
  sql = f"SELECT {','.join(cols)} FROM addresses WHERE organisation_id = ? ORDER BY {','.join(order_by)}"

  return sqlite.query(sql, org.current(cols=("id",)))


def find_by_id(id: int, cols: tuple = ("*",)) -> Optional[Tuple]:
  (org_id,) = org.current(cols=("id",))

  return sqlite.query_one(
    f"SELECT {','.join(cols)} FROM addresses WHERE id = ? AND organisation_id = ? LIMIT 1",
    (id, org_id)
  )
