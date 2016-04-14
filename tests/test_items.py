import unittest

from nose import tools

from app import items


class TestQuantifiedItems(unittest.TestCase):

    def test_one_quantified_item(self):
        apple = items.QuantifiedItem('apple', 1.00, 1)
        tools.assert_equal(apple.name, 'apple')
        tools.assert_equal(apple.quantity, 1)
        tools.assert_equal(apple.price, 1.00)
        tools.assert_equal(apple.subtotal(), 1.00)
        tools.assert_equal(apple.__str__(), '1 apple $1.00: $1.00')
        tools.assert_true(isinstance(apple.void(), items.VoidedItem))

    def test_multiple_quantified_items(self):
        apples = items.QuantifiedItem('apple', 1.00, 2)
        tools.assert_equal(apples.name, 'apple')
        tools.assert_equal(apples.price, 1.00)
        tools.assert_equal(apples.quantity, 2)
        tools.assert_equal(apples.subtotal(), 2.00)
        tools.assert_equal(apples.__str__(), '2 apple $1.00: $2.00')


class TestWeightedItems(unittest.TestCase):

    def test_one_item(self):
        apple = items.WeightedItem('apple', 1.00, 1)
        tools.assert_equal(apple.name, 'apple')
        tools.assert_equal(apple.quantity, 1)
        tools.assert_equal(apple.price, 1.00)
        tools.assert_equal(apple.subtotal(), 1.00)
        tools.assert_equal(apple.__str__(), '1 kg apple $1.00/kg: $1.00')
        tools.assert_true(isinstance(apple.void(), items.VoidedItem))

    def test_multiple_items(self):
        apples = items.WeightedItem('apple', 1.00, 2)
        tools.assert_equal(apples.name, 'apple')
        tools.assert_equal(apples.price, 1.00)
        tools.assert_equal(apples.quantity, 2)
        tools.assert_equal(apples.subtotal(), 2.00)
        tools.assert_equal(apples.__str__(), '2 kg apple $1.00/kg: $2.00')


class TestVoidedItem(unittest.TestCase):

    def test_one_item(self):
        apple = items.WeightedItem('apple', 1.00, 1)
        tools.assert_equal(apple.name, 'apple')
        tools.assert_equal(apple.quantity, 1)
        tools.assert_equal(apple.price, 1.00)
        tools.assert_equal(apple.subtotal(), 1.00)
        tools.assert_equal(apple.__str__(), '1 kg apple $1.00/kg: $1.00')

        voided_apple = apple.void()
        tools.assert_equal(voided_apple.name, 'apple')
        tools.assert_equal(voided_apple.subtotal(), -1.00)
        tools.assert_equal(voided_apple.__str__(), '1 VOIDED apple: $-1.00')

    def test_multiple_items(self):
        apples = items.WeightedItem('apple', 1.00, 2)
        tools.assert_equal(apples.name, 'apple')
        tools.assert_equal(apples.price, 1.00)
        tools.assert_equal(apples.quantity, 2)
        tools.assert_equal(apples.subtotal(), 2.00)
        tools.assert_equal(apples.__str__(), '2 kg apple $1.00/kg: $2.00')

        voided_apples = apples.void()
        tools.assert_equal(voided_apples.name, 'apple')
        tools.assert_equal(voided_apples.subtotal(), -2.00)
        tools.assert_equal(voided_apples.__str__(), '2 VOIDED apple: $-2.00')

    def test_cannot_void_voided_item(self):
        apple = items.WeightedItem('apple', 1.00, 1)
        voided_apple = apple.void()
        with tools.assert_raises(items.InvalidRefundException):
            voided_apple.void()


class TestDiscountItem(unittest.TestCase):

    def test_discount_item(self):
        discount_item = items.DiscountItem('apple', 0.00, 1)
        tools.assert_equal(discount_item.name, 'apple')
        tools.assert_equal(discount_item.quantity, 1)
        tools.assert_equal(discount_item.price, 0.00)
        tools.assert_equal(discount_item.subtotal(), 0.00)
        tools.assert_equal(discount_item.__str__(), '1 DISCOUNT apple: $0.00')
        tools.assert_true(isinstance(discount_item.void(), items.VoidedDiscountItem))


class TestVoidedDiscountItem(unittest.TestCase):

    def test_voided_discount_item(self):
        voided_discount = items.VoidedDiscountItem('apple', -1.00, 1)
        tools.assert_equal(voided_discount.name, 'apple')
        tools.assert_equal(voided_discount.subtotal(), -1.00)
        tools.assert_equal(voided_discount.__str__(), '1 VOIDED DISCOUNT apple: $-1.00')

    def test_cannot_void_voided_discount_item(self):
        voided_discount = items.VoidedDiscountItem('apple', -1.00, 1)
        with tools.assert_raises(items.InvalidRefundException):
            voided_discount.void()
