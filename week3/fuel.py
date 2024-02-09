while True:
    try:
        frac = input("Fraction: ").split("/")
        x = int(frac[0])
        y = int(frac[1])

        rem = x/y * 100

        if x > y:
            raise ValueError("X can not be greater than Y")
        elif rem <= 1:
            print("E")
        elif rem >= 99:
            print("F")
        else:
            print(f"{round(rem)}%")

        break
    except (ValueError, ZeroDivisionError, IndexError) as e:
        pass
