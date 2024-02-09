item = input("Item: ").lower()

fruits = {
    "apple": 130,
    "avocado": 50,
    "banana": 110,
    "cantaloupe": 50,
    "grapefruit": 60,
    "grapes": 90,
    "sweet cherries": 100,
    "kiwifruit": 90,
    "pear": 100,
}

if item in fruits:
    print(fruits[item])