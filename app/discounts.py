class Discount(object):

    def __init__(self, name, discount_type, trigger, reward):
        self.name = name
        self.discount_type = discount_type
        self.trigger = trigger
        self.reward = reward

    def is_applicable(self):
        pass


class ReducedRateDiscount(Discount):

    """
    These discounts are of the type 'Three for $1'
    """

    def __init__(self, name, discount_type, trigger, reward):
        super(ReducedRateDiscount, self).__init__(name, discount_type, trigger, reward)

    def is_applicable(self):
        pass

    def reward(self):
        pass


class AddOnDiscount(Discount):

    """
    These discounts are of the type 'Buy 2, get 1 free'
    """

    def __init__(self, name, discount_type, trigger, reward):
        super(AddOnDiscount, self).__init__(name, discount_type, trigger, reward)

    def is_applicable(self):
        pass

    def reward(self):
        pass
