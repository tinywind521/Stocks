class Person:
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender


class Male(Person):
    def __init__(self, name):
        super().__init__()
        print("Hello Mr." + name)


class Female(Person):
    def __init__(self, name):
        super().__init__()
        print("Hello Miss." + name)


class Factory:
    def getPerson(self, name, gender):
        if gender == 'M':
            return Male(name)
        if gender == 'F':
            return Female(name)
        else:
            print('Error gender!')
            return None


if __name__ == '__main__':
    factory = Factory()
    person = factory.getPerson("Chetan", "M")
