from fpdf import FPDF

PAGE_W = 210
PAGE_H = 297
IMG_W = IMG_H = 200
IMG_X = (PAGE_W - IMG_W) / 2
IMG_Y = (PAGE_H - IMG_H) / 2

def main():
  name = input("Name: ").strip().title()

  Shirtificate.print(name)


class Shirtificate(FPDF):
  def header(self):
    self.set_font("helvetica", "B", 32)
    self.set_y(15)
    self.cell(h=10, txt="CS50 Shirtificate", center=True)

    self.image(
      "shirtificate.png",
      keep_aspect_ratio=True,
      x=IMG_X, y=IMG_Y, w=IMG_W, h=IMG_H
    )


  @classmethod
  def print(cls, name):
    if name == "":
        raise ValueError("empty name, is not allowed")

    s = cls()

    s.add_page()

    s.set_y(PAGE_H/2 - 35)
    s.set_text_color(255, 255, 255)
    s.set_draw_color(200, 50, 50)
    s.set_line_width(1)
    s.set_font_size(18)
    s.cell(txt=f"{name} took CS50", h=9, border="B", center=True)

    s.output("shirtificate.pdf")


if __name__ == "__main__":
  main()
