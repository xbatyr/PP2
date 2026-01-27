n = int(input())
a = list(map(int, input().split()))
s = set()
for x in a:
    if x in s:
        print("NO")
    else:
        print("YES")
        s.add(x)