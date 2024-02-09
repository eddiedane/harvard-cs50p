from db.sqlite import connect
from sqlite3 import Cursor, Connection
from typing import List

ORGANISATIONS_TABLE: str = "organisations"
SETTINGS_TABLE: str = "settings"
ADDRESSES_TABLE: str = "addresses"
CLIENTS_TABLE: str = "clients"
ITEMS_TABLE: str = "items"
INVOICES_TABLE: str = "invoices"
LINE_ITEMS_TABLE: str = "line_items"

create_org_table: str = f"""
CREATE TABLE IF NOT EXISTS {ORGANISATIONS_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  active BOOLEAN NOT NULL,
  email VARCHAR NOT NULL,
  phone VARCHAR,
  plugin VARCHAR NOT NULL DEFAULT 'default',
  mail_host VARCHAR DEFAULT NULL,
  mail_port INTEGER DEFAULT NULL,
  mail_user VARCHAR DEFAULT NULL,
  mail_pwrd VARCHAR DEFAULT NULL,
  -- address_id INTEGER,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""


create_settings_table: str = f"""
CREATE TABLE IF NOT EXISTS {SETTINGS_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  key VARCHAR
  value VARCHAR
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""

create_addr_table: str = f"""
CREATE TABLE IF NOT EXISTS {ADDRESSES_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  street VARCHAR,
  city VARCHAR,
  state VARCHAR,
  country VARCHAR,
  postcode VARCHAR,
  organisation_id INTEGER REFERENCES {ORGANISATIONS_TABLE}(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

add_org_addr_ref_cols_key: str = f"""
ALTER TABLE {ORGANISATIONS_TABLE}
ADD COLUMN address_id INTEGER REFERENCES {ADDRESSES_TABLE}(id) ON DELETE SET NULL"""

create_clients_table: str = f"""
CREATE TABLE IF NOT EXISTS {CLIENTS_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  email VARCHAR NOT NULL,
  phone VARCHAR,
  billing_address_id INTEGER REFERENCES {ADDRESSES_TABLE}(id) ON DELETE SET NULL,
  shipping_address_id INTEGER REFERENCES {ADDRESSES_TABLE}(id) ON DELETE SET NULL,
  organisation_id INTEGER NOT NULL REFERENCES organisations(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)"""

create_items_table: str = f"""
CREATE TABLE IF NOT EXISTS {ITEMS_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  description VARCHAR DEFAULT NULL,
  price DECIMAL(10,2) NOT NULL,
  type VARCHAR CHECK( type IN ("goods", "services") ) NOT NULL DEFAULT "goods",
  uom VARCHAR CHECK( uom IN ("piece", "hour", "gram", "meter") ) NOT NULL DEFAULT "piece",
  organisation_id INTEGER REFERENCES organisations(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
"""

create_invoices_table: str = f"""
CREATE TABLE IF NOT EXISTS {INVOICES_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  client_id INTEGER REFERENCES {CLIENTS_TABLE}(id) ON DELETE CASCADE,
  organisation_id INTEGER REFERENCES {ORGANISATIONS_TABLE}(id) ON DELETE CASCADE,
  sent_at TIMESTAMP DEFAULT NULL,
  paid_at TIMESTAMP DEFAULT NULL,
  due_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
"""

create_line_items_table: str = f"""
CREATE TABLE IF NOT EXISTS {LINE_ITEMS_TABLE} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  quantity INTEGER NOT NULL,
  total DECIMAL(10,2) NOT NULL,
  item_id INTEGER REFERENCES {ITEMS_TABLE}(id) ON DELETE SET NULL,
  invoice_id INTEGER REFERENCES {INVOICES_TABLE}(id) ON DELETE SET NULL,
  organisation_id INTEGER REFERENCES {ORGANISATIONS_TABLE}(id) ON DELETE CASCADE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
)
"""


def up() -> None:
  conn: Connection = connect()
  cursor: Cursor = conn.cursor()
  tables: List[str] = [
     create_org_table,
     create_addr_table,
     add_org_addr_ref_cols_key,
     create_clients_table,
     create_items_table,
     create_invoices_table,
     create_line_items_table
  ]

  for sql in tables:
    cursor.execute(sql)


def down() -> None:
  tables: List[str] = [ORGANISATIONS_TABLE, ADDRESSES_TABLE, CLIENTS_TABLE, ITEMS_TABLE, INVOICES_TABLE, LINE_ITEMS_TABLE]
  conn: Connection = connect()
  cur: Cursor = conn.cursor()

  for table in tables:
      cur.execute(f"DROP TABLE IF EXISTS {table}")
