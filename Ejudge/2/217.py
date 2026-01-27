n = int(input())
f = {}
for _ in range(n):
    num = input().strip()
    if num in f:
        f[num] += 1
    else:
        f[num] = 1
cnt = 0
for k in f:
    if f[k] == 3:
        cnt += 1

print(cnt)
