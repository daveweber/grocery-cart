import abc

import items


class Discount(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def is_applicable(self, cart):
        raise NotImplementedError("Each discount must implement it's own is_applicable method")

    @abc.abstractmethod
    def get_reward(self):
        raise NotImplementedError("Each discount must implement it's own get_method method")


class BuyMoreForLessDiscount(Discount):

    def __init__(self, name, trigger_amount, reward_price, reward_quantity):
        super(BuyMoreForLessDiscount, self).__init__(name)
        self.trigger_amount = trigger_amount
        self.reward_price = reward_price
        self.reward_quantity = reward_quantity

    def is_applicable(self, cart_items):
        applicable_items, applied_discounts = 0, 0

        for item in cart_items:
            if item.name == self.name:
                if isinstance(item, items.PhysicalItem):
                    applicable_items += item.quantity
                elif isinstance(item, items.DiscountItem):
                    applied_discounts += self.trigger_amount

        return (applicable_items - applied_discounts) >= self.trigger_amount

    def needs_voiding(self, cart_items):
        applicable_items, applied_discounts = 0, 0

        for item in cart_items:
            if item.name == self.name:
                if isinstance(item, items.PhysicalItem):
                    applicable_items += item.quantity
                elif isinstance(item, items.DiscountItem):
                    applied_discounts += self.trigger_amount
                elif isinstance(item, items.VoidedDiscountItem):
                    applied_discounts -= self.trigger_amount
                elif isinstance(item, items.VoidedItem):
                    applicable_items -= item.quantity

        return applicable_items < applied_discounts

    def get_reward(self):
        return items.DiscountItem(self.name, self.reward_price, self.reward_quantity)


class ReducedRateDiscount(BuyMoreForLessDiscount):

    """
    These discounts are of the type 'Three for $1'
    """

    def __init__(self, name, trigger_amount, reward_price):
        super(ReducedRateDiscount, self).__init__(name, trigger_amount, reward_price, 1)


class AddOnDiscount(BuyMoreForLessDiscount):

    """
    These discounts are of the type 'Buy 2, get 1 free'
    """

    def __init__(self, name, trigger_amount, reward_quantity):
        super(AddOnDiscount, self).__init__(name, trigger_amount, 0.00, reward_quantity)
