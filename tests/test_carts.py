import unittest

from nose import tools

from app import discounts, carts, items


class TestAddAndRemoveFromCarts(unittest.TestCase):

    def test_new_cart(self):
        cart = carts.Cart()
        
        tools.assert_list_equal([], cart.get_items())

    def test_add_item(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)

        tools.assert_equal([apple], cart.get_items())

    def test_add_item_adds_discount(self):
        add_on_discount = discounts.AddOnDiscount('apple', 3, 1)
        discount_apple = add_on_discount.get_reward()
        cart = carts.Cart(discounts=[add_on_discount])
        apple = items.QuantifiedItem('apple', 1.00, 1)
        for _ in xrange(6):
            cart.add(apple)

        tools.assert_equal(8, len(cart.get_items()))
        tools.assert_equal([apple, apple, apple], cart.get_items()[:3])
        tools.assert_equal(discount_apple.__str__(), cart.get_items()[3].__str__())
        tools.assert_equal([apple, apple, apple], cart.get_items()[4:7])
        tools.assert_equal(discount_apple.__str__(), cart.get_items()[7].__str__())

    def test_remove_item(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)
        removed_apple = cart.remove(apple)

        tools.assert_equal([apple, removed_apple], cart.get_items())

    def test_remove_non_existent_item(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        orange = items.QuantifiedItem('orange', 2.00, 1)
        cart.add(apple)
        cart.remove(orange)

        tools.assert_equal([apple], cart.get_items())

    def test_remove_item_voids_discount(self):
        add_on_discount = discounts.AddOnDiscount('apple', 3, 1)
        discount_apple = add_on_discount.get_reward()
        cart = carts.Cart(discounts=[add_on_discount])
        apple = items.QuantifiedItem('apple', 1.00, 1)
        for _ in xrange(3):
            cart.add(apple)

        removed_apple = cart.remove(apple)

        tools.assert_equal(5, len(cart.get_items()))
        tools.assert_equal([apple, apple, apple], cart.get_items()[:3])
        tools.assert_equal(discount_apple.__str__(), cart.get_items()[3].__str__())
        tools.assert_equal(removed_apple, cart.get_items()[4])


class TestCartReceipts(unittest.TestCase):

    def test_receipt_one_product(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)

        tools.assert_equal(([apple], 1.00), cart.get_receipt())

    def test_receipt_one_product_removed(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        cart.add(apple)
        removed_apple = cart.remove(apple)

        tools.assert_equal(([apple, removed_apple], 0.00), cart.get_receipt())

    def test_receipt_multiple_products(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        orange = items.QuantifiedItem('orange', 2.00, 2)
        banana = items.WeightedItem('banana', 3.00, 5)
        for item in [apple, orange, banana]:
            cart.add(item)

        tools.assert_equal(([apple, orange, banana], 20.00), cart.get_receipt())

        removed_banana = cart.remove(banana)
        tools.assert_equal(([apple, orange, banana, removed_banana], 5.00), cart.get_receipt())

        removed_apple = cart.remove(apple)
        tools.assert_equal(([apple, orange, banana, removed_banana, removed_apple], 4.00), cart.get_receipt())

    def test_print_receipt(self):
        cart = carts.Cart()
        apple = items.QuantifiedItem('apple', 1.00, 1)
        orange = items.QuantifiedItem('orange', 2.00, 2)
        banana = items.WeightedItem('banana', 3.00, 5)
        for item in [apple, orange, banana]:
            cart.add(item)

        cart.remove(banana)
        cart.remove(apple)

        expected_receipt = ("1 apple $1.00: $1.00\n"
                            "2 orange $2.00: $4.00\n"
                            "5 kg banana $3.00/kg: $15.00\n"
                            "VOIDED banana: $-15.00\n"
                            "VOIDED apple: $-1.00\n"
                            "----------------------------\n"
                            "TOTAL: $4.00")

        tools.assert_equal(expected_receipt, cart.print_receipt())
