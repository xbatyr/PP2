# return tuple
def min_max(nums):
    if len(nums) == 0:
        return None
    return min(nums), max(nums)

def safe_divide(a, b):
    if b == 0:
        return "Error"
    return a / b

print(min_max([5, 2, 9]))
print(min_max([]))
print(safe_divide(10, 2))
print(safe_divide(10, 0))
