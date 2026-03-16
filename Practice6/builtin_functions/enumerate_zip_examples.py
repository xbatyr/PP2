fruits = ["apple", "banana", "cherry"]
prices = [1.2, 0.5, 2.0]

for i, fruit in enumerate(fruits):
    print(i, fruit)

print()

for fruit, price in zip(fruits, prices):
    print(fruit, price)

print()

x = 42
print(type(x))
print(isinstance(x, int))
print(str(x))
print(float(x))
