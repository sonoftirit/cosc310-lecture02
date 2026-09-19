"""Exercise 5: Your first tests.

Run them with:      pytest -v

These fail until Cart is implemented. Failing tests can also provide some important information.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from exercise3 import Cart, OutOfStockError

GYOZA = {"id": 2, "name": "Gyoza (6 pc)", "price": 8.00, "available": True}
RAMEN = {"id": 1, "name": "Tonkotsu Ramen", "price": 16.50, "available": True}
MISO = {"id": 4, "name": "Spicy Miso Ramen", "price": 17.25, "available": False}


def test_empty_cart_total_is_zero():
    assert Cart().total() == 0


def test_total_across_multiple_items():
    cart = Cart()
    cart.add_item(GYOZA, 2)      # 16.00
    cart.add_item(RAMEN, 1)      # 16.50
    assert cart.total() == 32.50


def test_adding_same_item_twice_increases_quantity():
    cart = Cart()
    cart.add_item(GYOZA, 2)
    cart.add_item(GYOZA, 1)
    assert len(cart.lines) == 1
    assert cart.lines[0]["qty"] == 3


def test_zero_quantity_is_rejected():
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(GYOZA, 0)


def test_unavailable_item_is_rejected():
    cart = Cart()
    with pytest.raises(OutOfStockError):
        cart.add_item(MISO, 1)


def test_removing_an_absent_item_raises():
    cart = Cart()
    with pytest.raises(KeyError):
        cart.remove_item(999)


# --- my own tests: behaviour not covered above ---------------------------


def test_add_item_defaults_to_quantity_one():
    cart = Cart()
    cart.add_item(GYOZA)
    assert cart.lines[0]["qty"] == 1


def test_negative_quantity_is_rejected():
    """qty < 1 covers negatives too, not just zero."""
    cart = Cart()
    with pytest.raises(ValueError):
        cart.add_item(GYOZA, -3)


def test_rejected_add_leaves_the_cart_unchanged():
    """A rejected operation must not half-apply: no line, no quantity bump."""
    cart = Cart()
    cart.add_item(GYOZA, 2)

    with pytest.raises(ValueError):
        cart.add_item(GYOZA, 0)
    with pytest.raises(OutOfStockError):
        cart.add_item(MISO, 1)

    assert len(cart.lines) == 1
    assert cart.lines[0]["qty"] == 2
    assert cart.total() == 16.00


def test_remove_item_removes_only_the_named_line():
    cart = Cart()
    cart.add_item(GYOZA, 2)
    cart.add_item(RAMEN, 1)

    cart.remove_item(GYOZA["id"])

    assert len(cart.lines) == 1
    assert cart.lines[0]["item_id"] == RAMEN["id"]
    assert cart.total() == 16.50


def test_total_is_rounded_to_two_decimal_places():
    """price * qty can drift in binary floating point; total() must round."""
    odd_price = {"id": 99, "name": "Daily Special", "price": 4.10, "available": True}
    cart = Cart()
    cart.add_item(odd_price, 3)
    assert 4.10 * 3 != 12.30          # the drift is real
    assert cart.total() == 12.30      # total() absorbs it


def test_repr_reports_line_count_and_total():
    cart = Cart()
    cart.add_item(GYOZA, 2)
    cart.add_item(RAMEN, 1)
    assert repr(cart) == "<Cart 2 items, $32.50>"
