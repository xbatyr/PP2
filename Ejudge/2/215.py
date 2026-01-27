n = int(input())
s = set()
for _ in range(n):
    name = input().strip()
    s.add(name)

print(len(s))
