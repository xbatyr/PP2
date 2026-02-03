class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def info(self):
        return self.name + " " + str(self.age)

p = Person("Batyr", 18)
print(p.info())
