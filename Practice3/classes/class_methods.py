class Counter:
    def __init__(self):
        self.value = 0
    def inc(self):
        self.value += 1
    def add(self, x):
        self.value += x

c = Counter()
c.inc()
c.add(5)
print(c.value)