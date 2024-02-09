import sys
from pyfiglet import Figlet


flags = ["-f", "--font"]
fonts = ["slant", "rectangles", "alphabet"]
f = Figlet()


if len(sys.argv) == 3 and sys.argv[1] in flags and sys.argv[2] in fonts:
    f = Figlet(font=sys.argv[2])
else:
    sys.exit("Invalid usage")


text = input("Input: ")
print(f.renderText(text))


