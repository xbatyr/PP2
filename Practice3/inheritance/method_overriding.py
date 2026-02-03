class Vehicle:
    def move(self):
        return "moves"

class Car(Vehicle):
    def move(self):
        return "drives"

v = Vehicle()
c = Car()
print(v.move())
print(c.move())
