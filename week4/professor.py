from random import randint
from sys import exit

MAX_PROBLEMS = 10
MAX_ATTEMPTS = 3

lvls = [1, 2, 3]

def main():
    lvl = get_level()
    current = 1
    score = 0

    while current <= MAX_PROBLEMS:
        attempts = 0
        x, y = generate_integer(lvl), generate_integer(lvl)

        while True:

            if attempts == MAX_ATTEMPTS:
                print(f"{x} + {y} = {x + y}")
                current += 1
                break

            try:
                ans = int(input(f"{x} + {y} = "))
            except ValueError:
                print("EEE")
                attempts += 1
                continue

            if x + y != ans:
                print("EEE")
                attempts += 1
                continue
            else:
                score += 1
                current += 1
                break

    print(f"Score: {score}")


def get_level():
    while True:
        try:
            lvl = int(input("Level: "))

            if lvl not in lvls: continue

            return lvl
        except ValueError:
            pass


def generate_integer(lvl):
    if lvl not in lvls: raise ValueError("Level must be 1, 2 or three")

    if lvl == 1: return randint(0, 9)

    lo = int("1" + "0" * (lvl - 1))
    hi = int("9" * lvl)

    return randint(lo, hi)

if __name__ == "__main__":
    main()