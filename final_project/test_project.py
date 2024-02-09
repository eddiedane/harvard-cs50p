import os
from click.testing import CliRunner

from project import list_orgs, current_org, create_org, update_org
from project import create_address, list_addresses
from project import create_client, list_clients
from project import list_items, create_item
from project import list_invoices, create_invoice, generate_invoice, send_invoice, mark_as_paid_invoice
from project import db_migrate_up, db_migrate_down, db_migrate_reset, db_run_seeder

from db import migrations, sqlite


os.environ["TEST"] = "1"

sqlite.destroy()


def test_list_orgs():
  migrations.up()

  runner = CliRunner()
  result = runner.invoke(list_orgs)

  assert result.exit_code == 0

  sqlite.destroy()


def test_current_org():
  migrations.up()

  runner = CliRunner()
  result = runner.invoke(current_org)

  assert result.exit_code == 0

  sqlite.destroy()


def test_create_org():
  migrations.up()

  runner = CliRunner()
  result = runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890")

  assert result.exit_code == 0
  assert result.output == "Organisation created successfully\n"

  sqlite.destroy()


def test_update_org():
  migrations.up()

  runner = CliRunner()
  runner.invoke(create_org, "--name=JohnDeo --email=johndoe@example.com --phone=+1234567890")
  result = runner.invoke(update_org, "--name=JohnDoe")

  assert result.exit_code == 0
  assert result.output == "Organisation updated successfully\n"

  sqlite.destroy()


def test_list_address():
  migrations.up()

  result = CliRunner().invoke(list_addresses)

  assert result.exit_code == 0

  sqlite.destroy()


def test_create_addresses():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890")
  result = runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")

  assert result.exit_code == 0
  assert result.output == "Address (ID: 1) created successfully\n"

  sqlite.destroy()


def test_list_clients():
  migrations.up()

  result = CliRunner().invoke(list_clients)

  assert result.exit_code == 0

  sqlite.destroy()


def test_create_client():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890")
  runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")
  result = runner.invoke(create_client, "--name=JaneDoe --billing=1 --shipping=1 --email=janedoe@example.com --phone=+1234567890")

  assert result.exit_code == 0
  assert result.output == "Client created successfully\n"

  sqlite.destroy()


def test_list_items():
  migrations.up()

  result = CliRunner().invoke(list_items)

  assert result.exit_code == 0

  sqlite.destroy()


def test_create_item():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890")
  result = runner.invoke(create_item, "--name=Item1 --desc=description --price=9.99 --type=goods --uom=piece")

  assert result.exit_code == 0
  assert result.output == "Item created successfully\n"

  sqlite.destroy()


def test_list_invoices():
  migrations.up()

  result = CliRunner().invoke(list_invoices)

  assert result.exit_code == 0

  sqlite.destroy()


def test_create_invoice():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890")
  runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")
  runner.invoke(create_client, "--name=JaneDoe --billing=1 --shipping=1 --email=janedoe@example.com --phone=+1234567890")
  runner.invoke(create_item, "--name=Item1 --desc=description --price=9.99 --type=goods --uom=piece")
  result = runner.invoke(create_invoice, "-i 1 1 --client=1 --name=Test --due=2024-01-01")

  assert result.exit_code == 0
  assert result.output == "Invoice created successfully\n"

  sqlite.destroy()


def test_generate_invoice():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890 --plugin=test")
  runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")
  runner.invoke(create_client, "--name=JaneDoe --billing=1 --shipping=1 --email=janedoe@example.com --phone=+1234567890")
  runner.invoke(create_item, "--name=Item1 --desc=description --price=9.99 --type=goods --uom=piece")
  runner.invoke(create_invoice, "-i 1 1 --client=1 --name=Test --due=2024-01-01")

  result = runner.invoke(generate_invoice, "1")

  assert result.exit_code == 0

  sqlite.destroy()


def test_send_invoice():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890 --plugin=test --mail-config sandbox.smtp.mailtrap.io 2525 499f25fb164b99 5dca7f127e9352")
  runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")
  runner.invoke(create_client, "--name=JaneDoe --billing=1 --shipping=1 --email=janedoe@example.com --phone=+1234567890")
  runner.invoke(create_item, "--name=Item1 --desc=description --price=9.99 --type=goods --uom=piece")
  runner.invoke(create_invoice, "-i 1 1 --client=1 --name=Test --due=2024-01-01")

  result = runner.invoke(send_invoice, "1")

  assert result.exit_code == 0

  sqlite.destroy()


def test_mark_as_paid_invoice():
  migrations.up()

  runner = CliRunner()

  runner.invoke(create_org, "--name=JohnDoe --email=johndoe@example.com --phone=+1234567890 --plugin=test --mail-config sandbox.smtp.mailtrap.io 2525 499f25fb164b99 5dca7f127e9352")
  runner.invoke(create_address, "--street=Street --city=City --state=State --country=Country --postcode=1234567")
  runner.invoke(create_client, "--name=JaneDoe --billing=1 --shipping=1 --email=janedoe@example.com --phone=+1234567890")
  runner.invoke(create_item, "--name=Item1 --desc=description --price=9.99 --type=goods --uom=piece")
  runner.invoke(create_invoice, "-i 1 1 --client=1 --name=Test --due=2024-01-01")

  result = runner.invoke(mark_as_paid_invoice, "1")

  assert result.exit_code == 0

  sqlite.destroy()


def test_db_migrate_up():
  runner = CliRunner()
  result = runner.invoke(db_migrate_up)

  assert result.exit_code == 0

  sqlite.destroy()


def test_db_migrate_down():
  runner = CliRunner()
  result = runner.invoke(db_migrate_down)

  assert result.exit_code == 0

  sqlite.destroy()


def test_db_migrate_reset():
  runner = CliRunner()
  result = runner.invoke(db_migrate_reset)

  assert result.exit_code == 0

  sqlite.destroy()


def test_db_run_seeder():
  runner = CliRunner()

  runner.invoke(db_migrate_up)

  result = runner.invoke(db_run_seeder)

  assert result.exit_code == 0

  sqlite.destroy()