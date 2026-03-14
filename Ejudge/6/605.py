s = input()
print('Yes' if any(c in 'aeiouAEIOU' for c in s) else 'No')