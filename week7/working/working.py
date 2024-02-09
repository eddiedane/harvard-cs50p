import re


def main():
  print(convert(input("Hours: ")))


def convert(s):
  rgx = r"(\d{1,2})(?::(\d{1,2}))?\s+((?:A|P)M)\s+to\s+(\d{1,2})(?::(\d{1,2}))?\s+((?:A|P)M)"
  m = re.fullmatch(rgx, s)

  if m == None: raise ValueError("Invalid time format")

  time1 = get_time(m.group(1), m.group(2), m.group(3))
  time2 = get_time(m.group(4), m.group(5), m.group(6))

  return f"{time1} to {time2}"


def get_time(hh, mm, meridiem):
  h = int(hh)
  m = int(mm if mm else 0)

  if not (1 <= h <= 12 and 0 <= m <= 59):
    raise ValueError("Invalid time")

  match meridiem:
    case "AM": h = 0 if h == 12 else h
    case "PM": h = h + 12 if h != 12 else h

  return f"{h:02}:{m:02}"


if __name__ == "__main__":
  main()