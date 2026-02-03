def sum_all(*args):
    # sum all
    total = 0
    for x in args:
        total += x
    return total

# many kwargs
def show_profile(**kwargs):
    for k, v in kwargs.items():
        print(k, "=", v)

print(sum_all(1, 2, 3, 4))
show_profile(name="Batyr", city="Almaty", age=18)
