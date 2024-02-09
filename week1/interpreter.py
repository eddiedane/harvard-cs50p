expression = input("Expression: ").strip()
left, op, right = expression.split(" ")
left = float(left)
right = float(right)

match op:
    case "+":
        print(left + right)
    case "*":
        print(left * right)
    case "/":
        print(left / right)
    case "-":
        print(left - right)