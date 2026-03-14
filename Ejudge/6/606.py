n = int(input())
a = list(map(int, input().split()))
print('Yes' if all(x >= 0 for x in a) else 'No')