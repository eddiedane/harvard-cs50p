# CLI Invoice Manager
#### Video Demo: [https://youtu.be/Cl8OC37fSL0](https://youtu.be/Cl8OC37fSL0)
#### Description:
A simple, flexible and extensible CLI invoice manager, for generating and sending invoice.

__How it Works__

To start using the invoicer CLI to manage, send & generate invoices,
First, you must create an organisation which represents a business or an individual (business owner)

```orgs:new --name "John Doe" --email johndoe@example.com --phone +123456789 --mail-config demo.email.com 2525 user password --plugin default```

To set the organisation's address, that can be included in the generated invoice file.
We'll have to create an address...

```adrs:new --street "Street" --city "City" --state "State" --country "Country" --postcode postcode```

Update organisation

```orgs:update --addr addressID```

Next, adding items (goods or services)

```itms:new --name "Working hours" --desc "work logged time" --price 15.50 --type services --uom hour```

To invoice a client or customer who orders any of your items, the client must first be added

```clts:new --name "Jane Doe" --billing 1 --shipping 1 --email janedoe@example.com --phone +987654321```

We can now create an invoice...

```invs:new --item item1ID quantity --item item2ID quantity --client 1 --name "Work time invoice" --due 2024-01-01```

After invoice has been successfully created, list all invoices to see your newly created invoice.

```invs:list```

You can now either generate and invoice file e.g PDF or send the invoice, which will also generate the invoice file and attach it to the sent email.

To just generate the invoice file...

```invs:generate invoiceID```

The invoice file will be generated and saved in the ```storage``` directory.

To send an invoice,

```invs:send invoiceID```

An email with invoice attachments will be sent to the clients email address.

Now to mark an invoice as paid, simply...

```invs:paid invoiceID```

Thats the invoicer CLI in a nutshell.

__Commands:__

_use ```--help``` flag to get all CLI commands and usage_

```orgs:new``` Create an organization, which represents the party issuing invoices

```orgs:list``` List all created organisations

```orgs:current``` Show active/selected organisation

```orgs:update``` Update organisations

```adrs:list``` List all addresses

```adrs:new``` Create a new addresses

```clts:list``` List clients of current organisation

```clts:new``` Create a new client for current organisation

```itms:list``` List all created items in active organisation

```itms:new``` Create new item (goods or services) in active organisation

```invs:list``` List invoices

```invs:generate``` Generate Invoice

```invs:new``` Create new invoice

```invs:paid``` Mark invoice as paid

```invs:send``` Send Invoice as Email

___Warning___ using these commands below, may result in permanet data loss

```db:down``` Undo database setup

```db:reset``` Refresh / Wipe database

```db:seed``` Seed database

```db:up``` Setup database schema and tables
