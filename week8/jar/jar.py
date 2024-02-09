def main():
    jar = Jar(100)
    jar.deposit(100)
    print(jar.size)
    jar.withdraw(99)
    print(jar.size)
    jar.withdraw(1)
    print(jar.size)

class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError("Invalid capacity")

        self._capacity = capacity
        self._size = 0

    def __str__(self):
        return "🍪" * self.size

    def deposit(self, n):
        if n < 0: ValueError("Negative deposit not allowed")
        if n + self.size > self.capacity:
            raise ValueError("Over capacity")

        self._size += n

    def withdraw(self, n):
        if n < 0: ValueError("Negative withdrawals not allowed")
        elif self.size - n < 0:
            raise ValueError("Not enough cookies available")

        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size

if __name__ == "__main__":
    main()
