import abc


class InvalidRefundException(Exception):
    """ This item cannot be refunded. """


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
        return 'VOIDED {0}: ${1:.2f}'.format(self.name, self.voided_total)

    def subtotal(self):
        return self.voided_total

    def void(self):
        raise InvalidRefundException


class DiscountItem(Item):

    def __init__(self, name, price, quantity):
        super(DiscountItem, self).__init__(name)
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return 'DISCOUNT {0}: ${1:.2f}'.format(self.name, self.subtotal())

    def subtotal(self):
        return self.price * self.quantity

    def void(self):
        return VoidedDiscountItem(self.name, self.subtotal() * -1)


class VoidedDiscountItem(VoidedItem):

    def __init__(self, name, voided_total):
        super(VoidedDiscountItem, self).__init__(name, voided_total)
        self.voided_total = voided_total

    def __repr__(self):
        return 'VOIDED DISCOUNT {0}: ${1:.2f}'.format(self.name, self.voided_total)

    def subtotal(self):
        return self.voided_total

    def void(self):
        raise InvalidRefundException


class PhysicalItem(Item):

    def __init__(self, name, price, quantity):
        super(PhysicalItem, self).__init__(name)
        self.price = price
        self.quantity = quantity

    def subtotal(self):
        return self.price * self.quantity


class QuantifiedItem(PhysicalItem):

    def __repr__(self):
        return '{0} {1} ${2:.2f}: ${3:.2f}'.format(self.quantity, self.name, self.price, self.subtotal())


class WeightedItem(PhysicalItem):

    def __repr__(self):
        return '{0} kg {1} ${2:.2f}/kg: ${3:.2f}'.format(self.quantity, self.name, self.price, self.subtotal())
