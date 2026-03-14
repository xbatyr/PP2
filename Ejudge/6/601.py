n = int(input())
a = list(map(int, input().split()))
print(sum(map(lambda x: x * x, a)))