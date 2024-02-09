from validators import email

def main():
  print("Valid" if email(input("Email: ")) else "Invalid")

if __name__ == "__main__":
  main()