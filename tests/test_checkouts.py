import unittest

from nose import tools

from app import checkouts, carts, items, discounts


class TestCheckouts(unittest.TestCase):

    def test_receipt_one_product(self):
        apple = items.Item('apple', 1.00)
        cart = carts.Cart()
        cart.add(apple)
        checkout_line = checkouts.Checkout(cart)
        tools.assert_equal((['1 apple $1.00'], 1.00),
                           checkout_line.get_receipt())

    def test_receipt_multiple_products(self):
        apple = items.Item('apple', 1.00)
        orange = items.Item('orange', 2.00, 2)
        cart = carts.Cart()
        for item in [apple, orange]:
            cart.add(item)
        checkout_line = checkouts.Checkout(cart)
        tools.assert_equal((['1 apple $1.00', '2 orange $4.00'], 5.00),
                           checkout_line.get_receipt())
