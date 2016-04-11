class Checkout(object):

    def __init__(self, cart, discounts=None):
        self.cart = cart
        self.discounts = discounts

    def get_receipt(self):
        history = []
        total = 0.00
        for item in self.cart.items:
            price = '{0:.2f}'.format(item.price)
            history.append('{} {} ${}'.format(item.quantity, item.name, price))
            total += item.price
        return history, total
