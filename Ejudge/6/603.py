n = int(input())
words = input().split()
print(*[f"{i}:{word}" for i, word in enumerate(words)])