class Animal:
    def speak(self):
        return "hz"

class Cat(Animal):
    def speak(self):
        return "meow"

a = Animal()
c = Cat()
print(a.speak())
print(c.speak())
