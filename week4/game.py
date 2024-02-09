import sys
import random

while True:
    try:
        n = int(input("Level: "))

        if n < 0: continue

        rand = random.randint(1, n)

        while True:
            guess = int(input("Guess: "))

            if guess < 0: continue
            if guess < rand:
                print("Too small!")
                continue
            elif guess > rand:
                print("Too large!")
                continue

            sys.exit("Just right!")
    except ValueError:
        pass
