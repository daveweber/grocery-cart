import unittest

from nose import tools

from app import items


class TestItems(unittest.TestCase):

    def test_one_item(self):
        item = items.Item('apple', 1.00)
        tools.assert_equal(item.name, 'apple')
        tools.assert_equal(item.price, 1.00)
        tools.assert_equal(item.quantity, 1)

    def test_multiple_items(self):
        item = items.Item('apple', 1.00, quantity=2)
        tools.assert_equal(item.name, 'apple')
        tools.assert_equal(item.price, 2.00)
        tools.assert_equal(item.quantity, 2)