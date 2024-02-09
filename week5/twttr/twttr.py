vowels = ["a", "e", "i", "o", "u"]

def main():
    ...


def shorten(text):
    no_vowels = ""

    for char in text:
      if char.lower() in vowels:
          continue
      else:
          no_vowels += char

    return no_vowels


if __name__ == "__main__":
    main()