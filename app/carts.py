class Cart(object):

    def __init__(self, items=None):
        self.items = items if items else []

    def add(self, item):
        self.items.append(item)
