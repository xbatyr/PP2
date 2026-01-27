n = int(input())
first = {}
for i in range(1, n+1):
    s = input().strip()
    if s not in first:
        first[s] = i

for k in sorted(first):
    print(k, first[k])
