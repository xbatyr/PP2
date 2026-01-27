n = int(input())
a = list(map(int, input().split()))
l -= 1
r -= 1
while l < r:
    a[l], a[r] = a[r], a[l]
    l += 1
    r -= 1
for x in a:
    print(x, end=" ")
