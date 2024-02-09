from services import organisations as org, clients as cl, items as itm, addresses as addr


def seed_organisations():
  # id = 1
  org.create(name="Uwa Osifo", email="uwa.osifo@example.com")
  # org.update(
  #   address_id=addr.create(
  #     "Block 18, Flat A, Osunde Estate, Ojo Street, Akobé QTRS",
  #     "Acient city",
  #     "Kingdom state",
  #     "Free Country",
  #     "1000001"
  #   )
  # )


def seed_clients():
  address_id = addr.create(
    "1, Corp Avenue, Business District",
    "Work city",
    "Producer state",
    "Enterprise Country",
    "2000002"
  )

  cl.update(
    cl.create(name="Employer LLC", email="fin.dept@employer.llc"),
    billing_address_id=address_id,
    shipping_address_id=address_id
  )


def seed_items():
  # id = 1
  itm.create(
    "Working hours",
    "Time (hours) worked on a project or product.",
    14.99,
    "services",
    "hour",
  )


def run():
  seed_organisations()
  seed_clients()
  seed_items()