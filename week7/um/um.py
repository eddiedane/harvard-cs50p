import re


def main():
  print(count(input("Text: ")))


def count(s):
 return len(re.findall(r"(?<![a-zA-Z])um(?![a-zA-Z])", s, re.IGNORECASE))


if __name__ == "__main__":
  main()