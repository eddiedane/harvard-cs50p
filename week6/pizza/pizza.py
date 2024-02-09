from tabulate import tabulate
import sys
import csv

if len(sys.argv) != 2:
  sys.exit("One argument required.")

try:
  filename = sys.argv[1]
except IndexError:
  sys.exit("filename required")

if filename[len(filename)-4:] != ".csv":
  sys.exit("only .csv file supported")

rows = []

with open(filename) as file:
  reader = csv.reader(file)
  for row in reader:
    rows.append(row)

print(tabulate(rows, headers="firstrow", tablefmt="grid"))

