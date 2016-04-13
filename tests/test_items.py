import unittest

from nose import tools

from app import items


class TestQuantifiedItems(unittest.TestCase):

    def test_one_item(self):
        apple = items.QuantifiedItem('apple', 1.00, 1)
        tools.assert_equal(apple.name, 'apple')
        tools.assert_equal(apple.quantity, 1)
        tools.assert_equal(apple.price, 1.00)
        tools.assert_equal(apple.subtotal(), 1.00)

    def test_multiple_items(self):
        apple = items.QuantifiedItem('apple', 1.00, 2)
        tools.assert_equal(apple.name, 'apple')
        tools.assert_equal(apple.price, 1.00)
        tools.assert_equal(apple.quantity, 2)
        tools.assert_equal(apple.subtotal(), 2.00)
