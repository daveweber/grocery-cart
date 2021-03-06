class Cart(object):

    def __init__(self, items=None, discounts=None):
        self.items = items if items else []
        self.discounts = discounts if discounts else []

    def get_items(self):
        return self.items

    def add(self, item):
        self.items.append(item)
        self._add_discounts()

    def _add_discounts(self):
        for discount in self.discounts:
            while discount.is_applicable(self.items):
                self.items.append(discount.get_reward())

    def remove(self, item):
        if item in self.items:
            voided_item = item.void()
            self.items.append(voided_item)
            self._remove_discounts()
            return voided_item

    def _remove_discounts(self):
        for discount in self.discounts:
            while discount.needs_voiding(self.items):
                self.items.append(discount.get_reward().void())

    def get_total(self):
        subtotal = 0.00
        for item in self.items:
            subtotal += item.subtotal()

        return subtotal

    def get_receipt(self):
        return self.items, self.get_total()

    def print_receipt(self):
        items, total = self.get_receipt()
        printed_receipt = '\n'.join([item.__str__() for item in items])
        printed_receipt += "\n----------------------------\nTOTAL: ${0:.2f}".format(total)
        return printed_receipt
