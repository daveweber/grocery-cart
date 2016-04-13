import unittest

from nose import tools

from app import discounts, items


class TestBuyMoreForLessDiscount(unittest.TestCase):

    def setUp(self):
        self.apple = items.QuantifiedItem('apple', 1.00, 1)
        self.discount = discounts.BuyMoreForLessDiscount('apple', 3, 0.00, 1)

    def test_discount_trigger(self):
        tools.assert_true(self.discount.trigger([self.apple]*3))

    def test_discount_trigger_false(self):
        tools.assert_false(self.discount.trigger([self.apple]*2))

    def test_get_reward(self):
        expected_discount_item = items.DiscountItem('apple', 0.00, 1)
        tools.assert_equal(self.discount.get_reward().__str__(), expected_discount_item.__str__())

    def test_is_applicable(self):
        cart_items = [self.apple] * 3
        tools.assert_true(self.discount.is_applicable(cart_items))

    def test_is_applicable_empty_cart(self):
        tools.assert_false(self.discount.is_applicable(cart_items=[]))

    def test_is_applicable_only_considers_applicable_items(self):
        irrelevant_item = items.QuantifiedItem('orange', 1.00, 1)
        cart_items = [self.apple, self.apple, irrelevant_item]
        tools.assert_false(self.discount.is_applicable(cart_items))

    def test_is_applicable_accounts_for_previously_applied_discounts(self):
        apple_discount = self.discount.get_reward()
        cart_items = [self.apple, self.apple, self.apple, apple_discount, self.apple, self.apple]
        tools.assert_false(self.discount.is_applicable(cart_items))

    def test_is_applicable_can_add_multiple_discounts(self):
        apple_discount = self.discount.get_reward()
        cart_items = [self.apple, self.apple, self.apple, apple_discount, self.apple, self.apple, self.apple]
        tools.assert_true(self.discount.is_applicable(cart_items))


class TestReducedRateDiscounts(unittest.TestCase):

    def setUp(self):
        self.apple = items.QuantifiedItem('apple', 1.00, 1)
        self.reduced_rate_discount = discounts.ReducedRateDiscount('apple', 3, -2.00)

    def test_reduced_rate_discount_item(self):
        expected_discount_item = items.DiscountItem('apple', -2.00, 1)
        tools.assert_equal(self.reduced_rate_discount.get_reward().__str__(), expected_discount_item.__str__())


class TestAddOnDiscounts(unittest.TestCase):

    def setUp(self):
        self.apple = items.QuantifiedItem('apple', 1.00, 1)
        self.add_on_discount = discounts.AddOnDiscount('apple', 3, 1)

    def test_reduced_rate_discount_item(self):
        expected_discount_item = items.DiscountItem('apple', 0.00, 1)
        tools.assert_equal(self.add_on_discount.get_reward().__str__(), expected_discount_item.__str__())
