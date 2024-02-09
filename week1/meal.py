ONE_MINUTE = 60

def main():
    time = convert(input("What time is it? ").strip())

    if 7 <= time <= 8:
        print("breakfast time")
    elif 12 <= time <= 13:
        print("lunch time")
    elif 18 <= time <= 19:
        print("dinner time")

def convert(time):
    parts = time.split(":")
    hours = float(parts[0])
    minutes = float(parts[1])

    return hours + (minutes / ONE_MINUTE)

if __name__ == "__main__":
    main()