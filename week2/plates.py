import re

def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    return is_spec_begin(s) and is_spec_len(s) and s.isalnum() and valid_num_chars(s)

def is_spec_begin(s):
    return s[0:2].isalpha()

def is_spec_len(s):
    return 2 <= len(s) <= 6

def valid_num_chars(s):
    end = s[len(s)-1:]
    prev_char = ""

    for char in s:
        if prev_char.isdigit() and char.isalpha():
            return False
        elif prev_char.isalpha() and char.isdigit() and char == "0":
            return False
        prev_char = char
    return True


main()