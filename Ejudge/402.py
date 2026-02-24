def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i


n = int(input())

first = True
for x in even_numbers(n):
    if not first:
        print(",", end="")
    print(x, end="")
    first = False