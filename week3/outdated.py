months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

def parse_date(s):
    d = s.split("/")
    if len(d) == 3:
        return int_date(d[2], d[0], d[1])

    d = s.split(" ")
    if len(d) != 3: return None

    try:
        i = months.index(d[0])
    except ValueError:
        return None
    else:
        return int_date(d[2], i+1, d[1][:-1])

def int_date(yyyy, mm, dd):
    try:
        return [int(yyyy), int(mm), int(dd)]
    except ValueError:
        return None

while True:
    date = input("Date: ")
    d = parse_date(date)

    if d == None or d[1] > 12 or d[2] > 31: continue

    print(f"{d[0]}-{d[1]:02}-{d[2]:02}")
    break
