import abc


class InvalidRefundException(Exception):
    """ This item cannot be refunded. """


class Item(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    @abc.abstractmethod
    def subtotal(self):
        raise NotImplementedError("Each item must implement it's own subtotal method")

    @abc.abstractmethod
    def void(self):
        raise NotImplementedError("Each item must implement it's own void method")


class VoidedItem(Item):

    def __init__(self, name, price, quantity):
        super(VoidedItem, self).__init__(name, price, quantity)

    def __repr__(self):
        return '{0} VOIDED {1}: ${2:.2f}'.format(self.quantity, self.name, self.price)

    def subtotal(self):
        return self.price

    def void(self):
        raise InvalidRefundException


class DiscountItem(Item):

    def __init__(self, name, price, quantity):
        super(DiscountItem, self).__init__(name, price, quantity)

    def __repr__(self):
        return '{0} DISCOUNT {1}: ${2:.2f}'.format(self.quantity, self.name, self.subtotal())

    def subtotal(self):
        return self.price * self.quantity

    def void(self):
        return VoidedDiscountItem(self.name, self.subtotal() * -1, self.quantity)


class PhysicalItem(Item):

    def __init__(self, name, price, quantity):
        super(PhysicalItem, self).__init__(name, price, quantity)

    def subtotal(self):
        return self.price * self.quantity

    def void(self):
        return VoidedItem(self.name, self.subtotal() * -1, self.quantity)


class QuantifiedItem(PhysicalItem):

    def __repr__(self):
        return '{0} {1} ${2:.2f}: ${3:.2f}'.format(self.quantity, self.name, self.price, self.subtotal())


class WeightedItem(PhysicalItem):

    def __repr__(self):
        return '{0} kg {1} ${2:.2f}/kg: ${3:.2f}'.format(self.quantity, self.name, self.price, self.subtotal())


class VoidedDiscountItem(VoidedItem):

    def __init__(self, name, price, quantity):
        super(VoidedDiscountItem, self).__init__(name, price, quantity)

    def __repr__(self):
        return '{0} VOIDED DISCOUNT {1}: ${2:.2f}'.format(self.quantity, self.name, self.price)
