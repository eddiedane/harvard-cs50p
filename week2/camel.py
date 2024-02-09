varName = input("camelCase: ")
var_name = ""

for char in varName:
    if char.isupper():
        var_name += f"_{char.lower()}"
    else:
        var_name += char


print(var_name)
