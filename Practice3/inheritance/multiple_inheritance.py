class Fly:
    def fly(self):
        return "flying"

class Swim:
    def swim(self):
        return "swimming"

class Duck(Fly, Swim):
    pass

d = Duck()
print(d.fly())
print(d.swim())
