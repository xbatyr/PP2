n = int(input())
a = list(map(int, input().split()))
f = {}
for x in a:
    if x in f:
        f[x] += 1
    else:
        f[x] = 1
m = 0
ans = a[0]
for k in f:
    if f[k] > m:
        m = f[k]
        ans = k
    elif f[k] == m and k < ans:
        ans = k

print(ans)
