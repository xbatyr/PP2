from functools import reduce

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares = list(map(lambda x: x ** 2, nums))
print(squares)

evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

total = reduce(lambda a, b: a + b, nums)
print(total)
