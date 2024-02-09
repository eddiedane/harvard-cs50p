response = input("What is the Answer to the Great Question of Life, the Universe, and Everything? ").lower().strip()
affirmative = response == "42" or response == "forty-two" or response == "forty two"

if affirmative:
    print("Yes")
else:
    print("No")