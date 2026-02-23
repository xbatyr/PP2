# 1
def square_up_to(n):
    for x in range(n + 1):
        yield x * x

n = int(input())

for sq in square_up_to(n):
    print(sq)
print()

# 2 

def evens_up_to(n):
    for x in range(n + 1):
        if x % 2 == 0:
            yield x

n = int(input())

first = True
for x in evens_up_to(n):
    if not first:
        print(", ", end="")
    print(x, end="")
    first = False
print()
print()

# 3 

def div_by_3_and_4(n):
    for x in range(n + 1):
        if x % 3 == 0 and x % 4 == 0:
            yield x

n = int(input())

for x in div_by_3_and_4(n):
    print(x)
print()

# 4

def squares(a, b):
    for x in range(a, b + 1):
        yield x * x

a = int(input())
b = int(input())

for i in squares(a, b):
    print(i)
print()

# 5

def countdown(n):
    for x in range(n, -1, -1):
        yield x

n = int(input())

for x in countdown(n):
    print(x)
