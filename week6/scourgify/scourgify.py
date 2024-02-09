import sys
import csv


if len(sys.argv) != 3:
  sys.exit("two argument required, (source file and destination file)")


source = sys.argv[1]
dest = sys.argv[2]


if source[len(source)-4:] != ".csv":
  sys.exit("only csv file supported")


with open(source, "r") as file:
  reader = csv.DictReader(file)
  rows = list()
  for i, row in enumerate(reader):
    last, first = row["name"].split(", ")
    rows.append({"first": first, "last": last, "house": row["house"]})


with open(dest, "w") as dest_file:
  writer = csv.DictWriter(dest_file, fieldnames=["first", "last", "house"])
  writer.writeheader()
  writer.writerows(rows)
