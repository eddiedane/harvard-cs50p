import sys
import os
import inflect
from PIL import Image, ImageOps

allowed_extensions = ["jpg", "jpeg", "png"]

def main():
  err_msg = args_error()
  if err_msg:
    sys.exit(err_msg)

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  shirt = Image.open("shirt.png")
  image = Image.open(input_file)
  image = ImageOps.fit(image, size=shirt.size)
  image.paste(shirt, (0, 0), shirt)
  image.save(output_file)


def is_allowed_file(filename):
  return get_file_ext(filename) in allowed_extensions


def get_file_ext(filename):
  parts = filename.split(".")
  l = len(parts)

  return parts[l-1] if l != 1 else ""


def args_error(argv=None):
  args = argv if argv else sys.argv
  args_len = len(args)

  if args_len < 3:
    return "Too few arguments"
  elif args_len > 3:
    return "Too many arguments"

  if not (is_allowed_file(args[1]) and is_allowed_file(args[2])):
    p = inflect.engine()
    return f"Only {p.join(allowed_extensions)}"
  elif get_file_ext(args[1]) != get_file_ext(args[2]):
    return "File types must match"
  elif not os.path.exists(args[1]):
    return f"File ({args[1]}) does not exists"

  return None


if __name__ == "__main__":
  main()
