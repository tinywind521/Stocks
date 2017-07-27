#!/usr/bin/python

"""
工厂方法模式（Factory Method Pattern）：
定义了一个创建对象的接口，但由子类决定要实例化类的哪一个；即通过子类来创建对象。
原则：
要依赖抽象，不要依赖具体类。

案例：
先解释什么是工厂：
如果你开一家Pizza店（PizzaStore抽象类）卖各种风味的Pizza（Pizza子类），
那么你需要根据客户要求准备相应的Pizza（创建Pizza对象），然后烘烤、切片、包装；
最简单的做法就是在PizzaStore中根据客户要求（类型判断）创建相应的Pizza对象，
然后调用Pizza自身（由Pizza抽象类实现）的烘烤、切片和包装方法；
但这样的代码缺乏弹性，因为你让一个抽象类去依赖具体的对象；我们可以创建一个工厂来生产Pizza，
根据传入的不同类型值返回不同Pizza对象，即从PizzaStore中将创建对象的代码挪到工厂中。
但这只是一个编程技巧，并不算模式。
在工厂方法模式中，我们在PizzaStore中定义一个抽象接口（create_pizza）作为抽象的工厂，
而order_pizza是它的客户；将Pizza对象的创建放到PizzaStore子类去解决。
现有Cheese和Clam两款Pizza，以及NY和Chicago两家分店，每家店的同款Pizza的口味不同——为迎合当地口味做了改进，
主要差别来自不同的原材料，
因此我们实现四个Pizza类型（NYStyleCheesePizza、NYStyleClamPizza、ChicagoStyleCheesePizza和ChicagoStyleClamPizza），
每种使用不同的原材料组合，根据客户所在城市和选择款式我们创建不同的对象；根据工厂方法，我们将对象创建的代码放到PizzaStore子类去实现。
"""


class Pizza:
    name = ""
    dough = ""
    sauce = ""
    toppings = []

    def prepare(self):
        print("Preparing %s" % self.name)
        print("    dough: %s" % self.dough)
        print("    sauce: %s" % self.sauce)
        print("    add toppings:")
        for n in self.toppings:
            print("        %s" % n)

    def bake(self):
        print("Bake for 25 minutes at 350.")

    def cut(self):
        print("Cutting into diagonal slices.")

    def box(self):
        print("Put into official box.")

    def get_name(self):
        return self.name


class PizzaStore:
    def order_pizza(self, pizza_type):
        self.pizza = self.create_pizza(pizza_type)
        self.pizza.prepare()
        self.pizza.bake()
        self.pizza.cut()
        self.pizza.box()
        return self.pizza

    def create_pizza(self, pizza_type):
        pass


class NYStyleCheesePizza(Pizza):
    def __init__(self):
        self.name = "NY Style Cheese Pizza"
        self.dough = "NY Dough"
        self.sauce = "NY Sauce"
        self.toppings.append("NY toopping A")
        self.toppings.append("NY toopping B")


class ChicagoStyleCheesePizza(Pizza):
    def __init__(self):
        self.name = "Chicago Style Cheese Pizza"
        self.dough = "Chicago Dough"
        self.sauce = "Chicago Sauce"
        self.toppings.append("Chicago toopping A")

    def cut(self):
        print("Cutting into square slices.")


class NYStyleClamPizza(Pizza):
    def __init__(self):
        self.name = "NY Style Clam Pizza"
        self.dough = "NY Dough"
        self.sauce = "NY Sauce"
        self.toppings.append("NY toopping A")
        self.toppings.append("NY toopping B")


class ChicagoStyleClamPizza(Pizza):
    def __init__(self):
        self.name = "Chicago Style Clam Pizza"
        self.dough = "Chicago Dough"
        self.sauce = "Chicago Sauce"
        self.toppings.append("Chicago toopping A")

    def cut(self):
        print("Cutting into square slices.")


class NYPizzaStore(PizzaStore):
    def create_pizza(self, pizza_type):
        if pizza_type == "cheese":
            return NYStyleCheesePizza()
        elif pizza_type == "clam":
            return NYStyleClamPizza()
        else:
            return None


class ChicagoPizzaStore(PizzaStore):
    def create_pizza(self, pizza_type):
        if pizza_type == "cheese":
            return ChicagoStyleCheesePizza()
        elif pizza_type == "clam":
            return ChicagoStyleClamPizza()
        else:
            return None

if __name__ == "__main__":
    ny_store = NYPizzaStore()
    chicago_store = ChicagoPizzaStore()

    pizza = ny_store.order_pizza("cheese")
    print("Mike ordered a %s." % pizza.get_name())
    print()

    pizza = chicago_store.order_pizza("clam")
    print("John ordered a %s." % pizza.get_name())
    print()

