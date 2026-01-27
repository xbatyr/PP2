n = int(input())
a = list(map(int, input().split()))
mx = max(a)
for i in range(len(a)):
    if a[i] == mx:
        print(i + 1)
        break