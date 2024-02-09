import sys
from os import path

try:
  if len(sys.argv) > 2:
    raise IndexError
  
  filename = sys.argv[1]
except IndexError:
  sys.exit("One CLI argument required (filename)")

if filename[len(filename)-3:] != ".py":
  sys.exit("Must be a .py file")
elif not path.exists(filename):
  sys.exit("File does not exist")

with open(filename, "r") as file:
  lines = file.readlines()

line_count = 0

for line in lines:
  ln = line.strip()

  if ln == "" or ln[0] == "#": continue

  line_count += 1

print(line_count)