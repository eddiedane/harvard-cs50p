greeting = input("Greeting: ").strip().lower()
hello = greeting[0:5]

if hello == "hello":
    print("$0")
elif greeting[0] == "h":
    print("$20")
else:
    print("$100")