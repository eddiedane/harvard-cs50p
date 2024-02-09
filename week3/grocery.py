items = {}

try:
    while True:
        item = input().upper()

        if item in items:
            items[item] += 1
        else:
            items[item] = 1
except EOFError:
    sorted_items = dict(sorted(items.items(), key=lambda key: key[0]))
    for item in sorted_items:
        print(f"{items[item]} {item}")
