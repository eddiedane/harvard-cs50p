def main():
    frac = input("Fraction: ").split("/")
    print(gauge(convert(frac)))


def convert(text):
    frac = text.split("/")
    x = int(frac[0])
    y = int(frac[1])

    if y == 0:
        raise ZeroDivisionError("Y can not be zero")
    elif x > y:
        raise ValueError("X can not be greater than Y")

    return x/y * 100


def gauge(percentage):
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{round(percentage)}%"


if __name__ == "__main__":
    main()