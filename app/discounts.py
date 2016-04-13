import abc

import items


class Discount(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    def trigger(self):
        raise NotImplementedError("Each discount must implement it's own trigger method")

    def is_applicable(self, cart):
        raise NotImplementedError("Each discount must implement it's own is_applicable method")

    def get_reward(self):
        raise NotImplementedError("Each discount must implement it's own get_method method")


class BuyMoreForLessDiscount(Discount):

    def __init__(self, name, trigger_amount, reward_price, reward_quantity):
        super(BuyMoreForLessDiscount, self).__init__(name)
        self.trigger_amount = trigger_amount
        self.reward_price = reward_price
        self.reward_quantity = reward_quantity

    def trigger(self, applicable_items):
        return len(applicable_items) >= self.trigger_amount

    def is_applicable(self, cart_items):
        applicable_items, applied_discounts = [], []

        for item in cart_items:
            if item.name == self.name:
                if isinstance(item, items.PhysicalItem):
                    applicable_items.append(item)
                elif isinstance(item, items.DiscountItem):
                    applied_discounts.append(item)

        previously_discounted_items = len(applied_discounts) * self.trigger_amount

        return self.trigger(applicable_items[:-previously_discounted_items]
                            if previously_discounted_items
                            else applicable_items)

    def needs_voiding(self, cart_items):
        applicable_items, applicable_voids, applied_discounts = [], [], []

        for item in cart_items:
            if item.name == self.name:
                if isinstance(item, items.PhysicalItem):
                    applicable_items.append(item)
                elif isinstance(item, items.DiscountItem):
                    applied_discounts.append(item)
                elif isinstance(item, items.VoidedItem):
                    applicable_voids.append(item)

        required_discounted_items = len(applied_discounts) * self.trigger_amount

        return (len(applicable_items) - len(applicable_voids)) < required_discounted_items

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
