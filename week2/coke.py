PRICE = 50
denominations = [25, 10, 5]
bal = 0

while True:
    try:
        print(f"Amount Due: {PRICE - bal}")
        coin = int(input("Insert Coin: "))

        if coin not in denominations:
            continue

        bal += coin

        if bal >= PRICE:
            print(f"Change Owed: {bal - PRICE}")
            break
    except ValueError:
        pass