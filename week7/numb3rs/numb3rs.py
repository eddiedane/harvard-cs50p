import re
import sys


def main():
  print(validate(input("IPv4 Address: ")))


def validate(ip):
  parts = ip.split(".")

  if len(parts) != 4:
    return False

  for part in parts:
    try:
      int_part = int(part)
    except ValueError:
      return False

    if not (0 <= int_part <= 255):
      return False

  return True


if __name__ == "__main__":
  main()