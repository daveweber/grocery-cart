import abc


class Item(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def subtotal(self):
        raise NotImplementedError("Each item must implement it's own subtotal method")

    def void(self):
        return VoidedItem(self.name, self.subtotal() * -1)


class VoidedItem(Item):

    def __init__(self, name, voided_total):
        super(VoidedItem, self).__init__(name)
        self.voided_total = voided_total

    def __repr__(self):
        return 'VOIDED {} for ${}'.format(self.name, self.voided_total)

    def subtotal(self):
        return self.voided_total


class QuantifiedItem(Item):

    def __init__(self, name, price, quantity):
        super(QuantifiedItem, self).__init__(name)
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return '{0} {1} ${2:.2f}'.format(self.quantity, self.name, self.subtotal())

    def subtotal(self):
        return self.price * self.quantity


class WeightedItem(Item):

    def __init__(self, name, amount, rate):
        super(WeightedItem, self).__init__(name)
        self.amount = amount
        self.rate = rate

    def __repr__(self):
        return '{0}kgs of {1} at ${2:.2f}/kg'.format(self.amount, self.name, self.subtotal())

    def subtotal(self):
        return self.amount * self.rate
