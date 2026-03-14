n = int(input())
print(*[f"{i}:{word}" for i, word in enumerate(input().split())])