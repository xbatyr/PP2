# list 1..20
nums = list(range(1, 21))

# filter evens
evens = list(filter(lambda x: x % 2 == 0, nums))

# filter > 10
gt_10 = list(filter(lambda x: x > 10, nums))

print(evens)
print(gt_10)
