import unittest

from nose import tools

from app import carts, items


class TestCarts(unittest.TestCase):

    def test_new_cart(self):
        cart = carts.Cart()
        
        tools.assert_list_equal([], cart.get_items())

    def test_add_item(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)

        tools.assert_equal(apple, cart.get_items()[0])
        tools.assert_equal(1, len(cart.get_items()))

    def test_receipt_one_product(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)

        tools.assert_equal(([apple], 1.00), cart.get_receipt())

    def test_receipt_multiple_products(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        orange = items.QuantifiedItem('orange', 2.00, 2)
        for item in [apple, orange]:
            cart.add(item)

        tools.assert_equal(([apple, orange], 5.00), cart.get_receipt())
