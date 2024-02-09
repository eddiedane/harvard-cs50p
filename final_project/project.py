from datetime import datetime
from typing import Optional, List, Tuple

import click
from tabulate import tabulate

from services import organisations as org, clients as cl, items as itm, invoices as inv
import services.addresses as addr
from db import migrations, seeder, sqlite


TABLE_FMT = "fancy_grid"


@click.group
def main():
  ...

@click.command("orgs")
def list_orgs():
  """List all organisations"""
  sqlite.exec("DELETE FROM invoices WHERE 1")
  try:
    orgs = [
      [str(id) + " √" if active  else str(id), name, email, phone or "None", address_id or "None", plugin]
      for (id, name, plugin, email, phone, address_id, active) in org.find_all(cols=("id", "name", "plugin", "email", "phone", "address_id", "active"))
    ]
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.echo(tabulate(orgs, headers=["ID", "Name", "E-Mail", "Phone", "Address ID", "Plugin"], tablefmt=TABLE_FMT))


@click.command("orgs:current")
@click.option("--id", type=int, prompt="Organisation ID", prompt_required=False, help="The organisation ID to set as active.")
def current_org(id: int):
  """Display active/selected organisation"""
  try:
    o = org.current(id)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.echo(tabulate([o], headers=["ID", "Name"], tablefmt=TABLE_FMT))


@click.command("orgs:new")
@click.option("--name", prompt="Organisation's name", type=str, required=True, help="The name of the organisation or individual")
@click.option("--email", prompt="Email", type=str, required=True, help="Organisation's email")
@click.option("--phone", prompt="Phone", type=str, default="", help="Organisation's phone")
@click.option("--mail-config", nargs=4, help="Mail server configurations (host, port, user, password)")
@click.option("--plugin", type=str, default="default", help="Invoice generator plugin")
def create_org(name: str, email: str, phone: str, mail_config: tuple, plugin: str):
  """Create a new organisation"""
  try:
    org.create(name, email, phone, mail_config=mail_config or (), plugin=plugin)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Organisation created successfully", fg="green")


@click.command("orgs:update")
@click.option("--name", type=str, help="The name of the organisation or individual")
@click.option("--email", type=str, help="Organisation's email")
@click.option("--phone", type=str, help="Organisation's phone")
@click.option("--addr", type=int, help="Address ID")
@click.option("--mail-config", nargs=4, help="Mail server configurations (host, port, user, password)")
@click.option("--plugin", type=str, help="Invoice generator plugin")
def update_org(name: str, email: str, phone: str, addr: int, mail_config: tuple, plugin: str):
  """Update current organisation"""
  try:
    org.update(None, name, addr, email, phone, mail_config=mail_config or (), plugin=plugin)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Organisation updated successfully", fg="green")


@click.command("adrs")
def list_addresses():
  """List all addresses"""
  try:
    addresses = addr.find_all(cols=("id", "street", "city", "state", "country"))
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.echo(tabulate(addresses, headers=["ID", "Street", "City", "State", "Country"], tablefmt=TABLE_FMT))


@click.command("adrs:new")
@click.option("--street", prompt="Street", required=True, help="Street address.")
@click.option("--city", prompt="City", required=True, help="City location.")
@click.option("--state", prompt="State", required=True, help="State location.")
@click.option("--country", prompt="Country", required=True, help="Country location.")
@click.option("--postcode", prompt="ZIP or Postal code", default="", help="ZIP or Postal code")
def create_address(street: str, city: str, state: str, country: str, postcode: str):
  """Create a new address"""
  try:
    id = addr.create(street, city, state, country, postcode)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho(f"Address (ID: {id}) created successfully", fg="green")


@click.command("clts")
def list_clients():
  """List clients of current organisation"""
  try:
    clients = cl.find_all(cols=("id", "name", "email"))
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.echo(tabulate(clients, headers=["ID", "Name", "E-Mail"], tablefmt=TABLE_FMT))


@click.command("clts:new")
@click.option("--name", prompt="Enter client's name", type=str, required=True, help="The name of the client")
@click.option("--billing", prompt="Billing Address ID", type=int, default=None, help="Address ID to link as client's billing address")
@click.option("--shipping", prompt="Shipping Address ID", type=int, default=None, help="Address ID to link as client's shipping address")
@click.option("--email", prompt="Email", type=str, required=True, help="Client's email")
@click.option("--phone", prompt="Phone", type=str, default="", help="Client's phone")
def create_client(name: str, billing: int, shipping: int, email: str, phone: str):
  """Create a new client for current organisation"""
  try:
    cl.create(name, email, phone, billing, shipping)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Client created successfully", fg="green")


@click.command("itms")
def list_items():
  """List all created items in active organisation"""
  try:
    items = itm.find_all(cols=("id", "name", "description", "type", "price"))
  except ValueError as e:
    click.secho(e, fg="red")
  else:
    click.echo(tabulate(items, headers=["id", "name", "description", "type", "price"], tablefmt=TABLE_FMT))


@click.command("itms:new")
@click.option("--name", prompt="Name", required=True, help="Product's or service's name")
@click.option("--desc", prompt="Description", default="", help="Short description of product")
@click.option("--price", prompt="Price", type=float, required=True, help="Product's price value")
@click.option("--type", prompt="Type", type=click.Choice(["goods", "services"]), default="goods", help="Product type e.g. physical goods or services")
@click.option("--uom", prompt="Unit of Measurement", type=click.Choice(["piece", "hour", "gram", "meter"]), default="piece", help="Product item measurement unit")
def create_item(name: str, desc: str, price: float, type: str, uom: str):
  """Create new item (goods or services) in active organisation"""
  try:
    itm.create(name, desc, price, type, uom)
  except ValueError as e:
    click.secho(e, fg="red")
  else:
    click.secho("Item created successfully", fg="green")


@click.command("invs")
def list_invoices() -> None:
  """List invoices"""
  cols: Tuple = ("id", "total", "client_id", "sent_at", "paid_at", "due_at", "created_at")
  try:
    invoices: List[Tuple] = inv.find_all(cols=cols)
    invs: List[Tuple] = []

    for (id, total, client_id, sent_at, paid_at, due_at, created_at) in invoices:
      client: Optional[Tuple] = cl.find_by_id(client_id, cols=("name",))
      invs.append((id, total, client[0] if client else client, sent_at, paid_at, datetime.strptime(due_at, "%Y-%m-%d %H:%M:%S").date(), created_at))
  except Exception as e:
    click.secho(e, fg="red")
  else:
    headers = ["ID", "Total", "Client", "Sent", "Paid", "Due", "Created At"]
    click.echo(tabulate(invs, headers=headers, tablefmt=TABLE_FMT))


def validate_items(ctx, param, value: list[tuple[int, int]]):
  items_ids = []
  for (id, _) in value:
    if not itm.find_by_id(id):
      raise click.BadParameter(f"Item with ID \"{id}\" was not found", param_hint=f"item {id}")

    if id in items_ids:
      raise click.BadParameter(f"Duplicate item ID \"{id}\"")
    else:
      items_ids.append(id)

  return value


def validate_client(ctx, params, value: int):
  if not cl.find_by_id(value):
    raise click.BadParameter(f"Client with ID \"{value}\" was not found", param_hint=f"client {value}")

  return value


@click.command("invs:new")
@click.option("-i", "--item", nargs=2, multiple=True, type=int, required=True, callback=validate_items, help="Items (IDs) to be paid for")
@click.option("--client", type=int, prompt="Client ID", required=True, callback=validate_client, help="Client (ID) to be invoiced")
@click.option("--name", type=str, prompt="Name", default="", help="Invoice name, also email subject, when invoice is sent as email")
@click.option("--due", type=click.DateTime(formats=["%Y-%m-%d"]), prompt="Due At", default=datetime.today().strftime("%Y-%m-%d"), help="Invoice due date")
def create_invoice(item: List[Tuple[int, int]], name: str, client: int, due: datetime):
  """Create new invoice"""
  try:
    inv.create(items=item, name=name, client_id=client, due_at=due)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Invoice created successfully", fg="green")


@click.command("invs:generate")
@click.argument('id', type=int)
def generate_invoice(id: int):
  """Generate Invoice"""
  try:
    files: list[str] = inv.generate(id)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho(f"Invoice generated", fg="green")
    click.secho('\n'.join(files), fg="cyan")


@click.command("invs:send")
@click.argument("id", type=int)
def send_invoice(id: int):
  """Send Invoice as Email"""
  try:
    inv.send(id)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Invoice sent successfully", fg="green")


@click.command("invs:paid")
@click.argument("id", type=int)
@click.option("--date", type=click.DateTime(formats=["%Y-%m-%d %H:%M:%S"]), default=datetime.today(), help="When invoice was paid")
@click.option("--modify", is_flag=True, default=False, help="Allow update to when invoice was paid")
def mark_as_paid_invoice(id: int, date: datetime, modify: bool):
  """Mark invoice as paid"""
  try:
    result = inv.find_by_id(id, cols=("paid_at",))
    if not modify and (result and result[0]):
        raise ValueError("Invoice already paid!")

    inv.mark_as_paid(id, date)
  except Exception as e:
    click.secho(e, fg="red")
  else:
    if result and result[0]:
      click.secho(f"Invoice #{id} paid - updated", fg="green")
    else:
      click.secho(f"Invoice #{id} paid", fg="green")


@click.command("db:up")
def db_migrate_up():
  """Setup database schema and tables"""
  migrations.up()


@click.command("db:down")
def db_migrate_down():
  """Undo database setup"""
  migrations.down()


@click.command("db:reset")
def db_migrate_reset():
  """Refresh / Wipe database"""
  try:
    migrations.down()
    migrations.up()
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Database reset successful", fg="green")


@click.command("db:seed")
def db_run_seeder():
  """Seed database"""
  try:
    seeder.run()
  except Exception as e:
    click.secho(e, fg="red")
  else:
    click.secho("Seeder ran and completed successfully", fg="green")


if __name__ == "__main__":
  main.add_command(list_orgs)
  main.add_command(list_orgs, "orgs:list")
  main.add_command(current_org)
  main.add_command(create_org)
  main.add_command(update_org)
  main.add_command(list_addresses)
  main.add_command(list_addresses, "adrs:list")
  main.add_command(create_address)
  main.add_command(list_clients)
  main.add_command(list_clients, "clts:list")
  main.add_command(create_client)
  main.add_command(list_items)
  main.add_command(list_items, "itms:list")
  main.add_command(create_item)
  main.add_command(list_invoices)
  main.add_command(list_invoices, "invs:list")
  main.add_command(create_invoice)
  main.add_command(generate_invoice)
  main.add_command(send_invoice)
  main.add_command(mark_as_paid_invoice)
  main.add_command(db_migrate_up)
  main.add_command(db_migrate_down)
  main.add_command(db_migrate_reset)
  main.add_command(db_run_seeder)

  main()
