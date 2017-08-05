class Person:

    def __init__(self):
        self.name = None

    def setName(self, name):
        self.name = name
        print(self)

n = Person()
n.setName('123')
Person.setName(n, '234')
