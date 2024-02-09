import inflect
from datetime import date
import re
import sys

p = inflect.engine()

def main():
    print(date_to_words(input("Date: ")))


def date_to_words(d):
    before = str_to_date(d)
    delta = date.today() - before
    minutes = round(delta.total_seconds()/60)
    words = p.number_to_words(minutes, andword=" ")

    return words[0].upper() + words[1:] + " " + p.plural("minute", minutes)


def str_to_date(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        sys.exit("Invalid date")

    try:
        return date.fromisoformat(s)
    except ValueError:
        sys.exit("Invalid date")


if __name__ == "__main__":
    main()