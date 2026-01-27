n = int(input())
d = {}
for _ in range(n):
    s, k = input().split()
    k = int(k)
    if s in d:
        d[s] += k
    else:
        d[s] = k

for name in sorted(d):
    print(name, d[name])
