import inflect

names = []

try:
    while True:
        names.append(input("Names: "))
except EOFError:
    print()
    pass


p = inflect.engine()
names_len = len(names)

for i in range(names_len):
    sub_index = (names_len - i - 1)*-1
    sub_names = names

    if sub_index != 0:
        sub_names = names[:sub_index]

    print("Adieu, adieu, to", p.join(sub_names))