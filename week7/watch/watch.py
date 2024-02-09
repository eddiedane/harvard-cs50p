import re

def main():
    print(parse(input("HTML: ")))


def parse(s):
  m = re.search(r"src=\"https?://(?:\w+\.)*youtube\.com/embed/(\w+)\"", s, re.IGNORECASE)

  return f"https://youtu.be/{m.group(1)}" if m else None


if __name__ == "__main__":
    main()