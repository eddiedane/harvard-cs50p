import sqlite3
import os
from typing import Optional, Tuple, List


def connect() -> sqlite3.Connection:
  return  sqlite3.connect(get_db())


def exec(sql: str, params: tuple = ()) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
  conn: sqlite3.Connection = connect()
  curs: sqlite3.Cursor = conn.cursor()
  curs.execute(sql, params)
  conn.commit()
  return (curs, conn)


def query(sql: str, params: tuple = ()) -> List[Tuple]:
  conn: sqlite3.Connection = connect()
  rows = conn.cursor().execute(sql, params).fetchall()
  conn.commit()
  return rows


def query_one(sql: str, params: tuple = ()) -> Optional[Tuple]:
  conn: sqlite3.Connection = connect()
  row = conn.cursor().execute(sql, params).fetchone()
  conn.commit()
  return row


def get_db() -> str:
  return "db/invoicer.db" if not os.environ.get("TEST") else "db/test_invoicer.db"


def destroy(db: str = "") -> None:
  try:
    os.remove(db or get_db())
  except OSError:
    pass
