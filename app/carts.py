class Cart(object):

    def __init__(self, items=None):
        self.items = items if items else []

    def get_items(self):
        return self.items

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        if item in self.items:
            self.items.append(item.void())

    def get_total(self):
        subtotal = 0.00
        for item in self.items:
            subtotal += item.subtotal()

        return subtotal

    def get_receipt(self):
        return self.items, self.get_total()
