from fpdf import FPDF, XPos, YPos, Align
from datetime import datetime


def gen(inv: dict) -> list[str]:
  pdf = FPDF("P", "mm", "Letter")
  filename = f"storage/{inv['num']}.pdf"
  margin_x = 25
  t = 18
  m = t
  n = t

  pdf.add_page()

  # Organisation Address

  org_name = str(inv["org_name"])
  pdf.set_font("helvetica", "B", 12)
  pdf.set_xy(margin_x, m)
  pdf.set_draw_color(10, 10, 10)
  pdf.cell(pdf.get_string_width(org_name), 10, text=org_name, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  if inv["address"]:
    street = str(inv["address"]["street"])
    pdf.set_font("helvetica", size=9)
    pdf.set_xy(margin_x, m:=m+5)
    pdf.cell(pdf.get_string_width(street), 10, text=street, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.set_font("helvetica", size=9)
    city_state_postcode = f"{inv['address']['city']}, {inv['address']['state']}, {inv['address']['postcode']}"
    pdf.set_xy(margin_x, m:=m+4)
    pdf.cell(pdf.get_string_width(city_state_postcode), 10, text=city_state_postcode, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.set_font("helvetica", size=9)
    country = str(inv['address']['country'])
    pdf.set_xy(margin_x, m:=m+4)
    pdf.cell(pdf.get_string_width(country), 10, country, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  # pdf.set_font("helvetica", size=9)
  org_phone = str(inv['org_phone'])
  pdf.set_xy(margin_x, m:=m+4)
  pdf.cell(pdf.get_string_width(org_phone), 10, org_phone, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  # Client Address

  bill_to = "Bill To"
  pdf.set_font("helvetica", size=10)
  pdf.set_xy(margin_x, m:=m+25)
  pdf.set_draw_color(10, 10, 10)
  pdf.cell(pdf.get_string_width(bill_to), 10, bill_to, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  client_name = inv["client_name"]
  pdf.set_font("helvetica", "B", 12)
  pdf.set_xy(margin_x, m:=m+5)
  pdf.set_draw_color(10, 10, 10)
  pdf.cell(pdf.get_string_width(client_name), 10, client_name, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  if inv["billing_address"]:
    street = str(inv["billing_address"]["street"])
    pdf.set_font("helvetica", size=9)
    pdf.set_xy(margin_x, m:=m+5)
    pdf.cell(pdf.get_string_width(street), 10, street, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.set_font("helvetica", size=9)
    city_state_postcode = f"{inv['billing_address']['city']}, {inv['billing_address']['state']}, {inv['billing_address']['postcode']}"
    pdf.set_xy(margin_x, m:=m+4)
    pdf.cell(pdf.get_string_width(city_state_postcode), 10, city_state_postcode, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # pdf.set_font("helvetica", size=9)
    country = str(inv['billing_address']['country'])
    pdf.set_xy(margin_x, m:=m+4)
    pdf.cell(pdf.get_string_width(country), 10, country, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  org_phone = str(inv['org_phone'])
  pdf.set_font("helvetica", size=9)
  pdf.set_xy(margin_x, m:=m+4)
  pdf.cell(pdf.get_string_width(org_phone), 10, org_phone, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  # Invoice Overview

  invoice_text = "INVOICE"
  pdf.set_font("helvetica", style="", size=25)
  invoice_text_w = pdf.get_string_width(invoice_text)
  pdf.set_xy(pdf.w-invoice_text_w-margin_x, n)
  pdf.cell(invoice_text_w, 10, invoice_text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  inv_num = f"# {inv['num']}"
  pdf.set_text_color(70, 70, 70)
  pdf.set_font("helvetica", style="B", size=10)
  inv_num_w = pdf.get_string_width(inv_num)
  pdf.set_xy(pdf.w-inv_num_w-margin_x, n:=n+9)
  pdf.cell(inv_num_w, 10, inv_num, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  bal_due = "Balance Due"
  pdf.set_font("helvetica", style="B", size=9)
  bal_due_w = pdf.get_string_width(bal_due)
  pdf.set_xy(pdf.w-bal_due_w-margin_x, n:=n+10)
  pdf.cell(bal_due_w, 10, bal_due, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  bal_due = f"${inv['total']:,.2f}"
  pdf.set_font("helvetica", style="B", size=15)
  bal_due_w = pdf.get_string_width(bal_due)
  pdf.set_xy(pdf.w-bal_due_w-margin_x, n:=n+6)
  pdf.cell(bal_due_w, 10, bal_due, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  summary = {
    "Invoice Date :": date(inv["created_at"]),
    "Due Date :": date(inv["due_at"]),
    "P.O.# :": f"{inv['id']:07}",
  }

  pdf.set_y(n:=n+12)
  pdf.set_text_color(0, 0, 0)

  for key, value in summary.items():
    sum_key = key
    pdf.set_font("helvetica", style="", size=11)
    sum_key_w = pdf.get_string_width(sum_key)
    pdf.set_xy(pdf.w-sum_key_w-(margin_x+30), n:=n+7)
    pdf.cell(sum_key_w, 10, sum_key, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    sum_val = value
    pdf.set_font("helvetica", style="", size=10)
    sum_val_w = pdf.get_string_width(sum_val)
    pdf.set_xy(pdf.w-sum_val_w-margin_x, n)
    pdf.cell(sum_val_w, 10, sum_val, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

  pdf.set_font("Times", size=9)
  pdf.set_y(m:=m+20)
  pdf.set_draw_color(180, 180, 180)

  with pdf.table(cell_fill_mode="ALL", cell_fill_color=(230, 230, 230)) as table:
    headers = (("#", Align.C), ("Item & Description", Align.L), ("Qty", Align.R), ("Price", Align.R), ("Total", Align.R))
    row = table.row()
    for (text, align) in headers:
      pdf.set_text_color(50, 50, 50)
      row.cell(text=text, align=align)

    for item in inv["items"]:
      row = table.row()
      cells = ((item["id"], Align.C), (item["name"], Align.L), (item["qty"], Align.R), (f"${item['price']:,.2f}", Align.R), (f"${item['total']:,.2f}", Align.R))
      for (datum, align) in cells:
        row.cell(str(datum), align=align)

  pdf.output(filename)

  return [filename]


def num(inv: dict) -> str:
  return f"INV-{inv['id']:07}"


def email_html(inv: dict) -> str:
  return f"""
<!DOCTYPE html>
<html>
  <body
    style="
      background-color: #e2e1e0;
      font-family: Open Sans, sans-serif;
      font-size: 100%;
      font-weight: 400;
      line-height: 1.4;
      color: #000;
    "
  >
    <div>
      <div>
        <div>
          <div>
            <div>
              <div style="background: #fbfbfb">
                <div style="max-width: 560px; margin: auto; padding: 0 3%">
                  <div style="padding: 30px 0; color: #555; line-height: 1.7">
                    Dear {inv["client_name"]}, <br /><br />Thank you for your business.
                    Your invoice can be viewed, printed and downloaded as PDF
                    from the email attachments.
                    <br />
                  </div>
                  <div
                    style="
                      padding: 3%;
                      background: #fefff1;
                      border: 1px solid #e8deb5;
                      color: #333;
                    "
                  >
                    <div
                      style="
                        padding: 0 3% 3%;
                        border-bottom: 1px solid #e8deb5;
                        text-align: center;
                      "
                    >
                      <h4 style="margin-bottom: 0">INVOICE AMOUNT</h4>
                      <h2 style="color: #d61916; margin-top: 10px">
                        ${inv["total"]}
                      </h2>
                    </div>
                    <div style="margin: auto; max-width: 350px; padding: 3%">
                      <p>
                        <span style="width: 40%; padding-left: 10%; float: left"
                          >Invoice No</span
                        ><span
                          style="
                            width: 40%;
                            padding-left: 10%;
                            display: inline-block;
                          "
                          ><b>{inv["num"]}</b></span
                        >
                      </p>
                      <p>
                        <span style="width: 40%; padding-left: 10%; float: left"
                          >Invoice Date</span
                        ><span style="width: 40%; padding-left: 10%"
                          ><b>{date(inv["created_at"])}</b></span
                        >
                      </p>
                      <p>
                        <span style="width: 40%; padding-left: 10%; float: left"
                          >Due Date</span
                        ><span style="width: 40%; padding-left: 10%"
                          ><b>{date(inv["due_at"])}</b></span
                        >
                      </p>
                    </div>
                  </div>
                  <br />
                  <div style="padding: 3% 0; line-height: 1.6">
                    Regards,
                    <div style="color: #8c8c8c; font-weight: 400">
                      {inv["org_name"]}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </body>
</html>
"""


def email_text(inv: dict) -> str:
  return f"""
Dear {inv["client_name"]},
Thank you for your business.
Your invoice can be viewed, printed and downloaded as PDF
from the email attachments.
"""

def date(d: str, format: str = "%Y-%m-%d %H:%M:%S") -> str:
  return datetime.strptime(d, format).strftime("%m %b, %Y")


if __name__ == "__main__":
  gen({
    "id": 1,
    "num": num({"id": 1}),
    "name": "Invoice - from Joaquin Heaney",
    "total": 2500.00,
    "created_at": "2001-01-01 00:00:00",
    "due_at": "2001-01-01 00:00:00",
    "items": [
      {
        "id": 1,
        "name": "Item 1",
        "price": 500.00,
        "qty": 5,
        "total": 2500.00,
        "item_id": 1,
        "created_at": "2001-01-01 00:00:00",
        "updated_at": "2001-01-01 00:00:00"
      }
    ],
    "org_name": "Joaquin Heaney",
    "org_email": "jh@example.com",
    "org_phone": "+1.834.661.7154",
    "address": {
      "street": "932 Kilback Roads",
      "city": "New Terence",
      "state": "Minnesota",
      "country": "United States of America",
      "postcode": "86588",
    },
    "client_name": "Davion Bartoletti",
    "client_email": "davion@example.com",
    "client_phone": "1-358-746-0111",
    "billing_address": {
      "street": "68439 Sanford Road Suite 399",
      "city": "Hellerhaven",
      "state": "West Virginia",
      "country": "United States of America",
      "postcode": "76789",
    },
    "shipping_address": {
      "street": "68439 Sanford Road Suite 399",
      "city": "Hellerhaven",
      "state": "West Virginia",
      "country": "United States of America",
      "postcode": "76789",
    },
  })