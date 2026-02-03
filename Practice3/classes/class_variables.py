class Student:
    uni = "KBTU"
    def __init__(self, name):
        self.name = name
        self.points = 0

s1 = Student("Batyr")
s2 = Student("Dias")

s1.points = 77
s2.points = 55

print(s1.uni, s1.name, s1.points)
print(s2.uni, s2.name, s2.points)

Student.uni = "hz"
print(s1.uni, s2.uni)
