text = input("Input: ")
vowels = ["a", "e", "i", "o", "u"]
no_vowels = ""

for char in text:
    if char.lower() in vowels:
        continue
    else:
        no_vowels += char


print(no_vowels)
