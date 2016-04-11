import unittest

from nose import tools

from app import carts, items


class TestCarts(unittest.TestCase):

    def test_new_cart(self):
        cart = carts.Cart()
        tools.assert_list_equal([], cart.items)

    def test_add_item(self):
        cart = carts.Cart()
        item = items.Item('apple', 1.00)
        cart.add(item)
        tools.assert_equal(item, cart.items[0])
        tools.assert_equal(1, len(cart.items))
