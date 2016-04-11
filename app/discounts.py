class Discount(object):

    def __init__(self, name, discount_type, trigger, effect):
        self.name = name
        self.discount_type = discount_type
        self.trigger = trigger
        self.effect = effect