class Item(object):

    def __init__(self, name, price, quantity=1):
        self.name = name
        self.quantity = quantity
        self.price = price * self.quantity
