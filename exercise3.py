"""Exercise 3: Enforce a business rule.

Extend your Cart so invalid operations are rejected by the CART.

  ValueError        when qty < 1
  OutOfStockError   when the item's "available" field is False
  KeyError          when removing an item that is not in the cart

Then demonstrate each one with try/except.
"""

from exercise1 import load_menu


class OutOfStockError(Exception):
    """Raised when a customer tries to order an item that is unavailable."""
    pass


class Cart:
    def __init__(self) -> None:
        self.lines: list[dict] = []

    def add_item(self, item: dict, qty: int = 1) -> None:
        if qty < 1:
            raise ValueError(f"quantity must be at least 1, got {qty}")
        if not item["available"]:
            raise OutOfStockError(f"{item['name']} is out of stock")
        for line in self.lines:
            if line["item_id"] == item["id"]:
                line["qty"] += qty
                return 
        new_line = {
            "item_id": item["id"],
            "name": item["name"],
            "price": item["price"],
            "qty": qty,
        }
        self.lines.append(new_line)

    def remove_item(self, item_id: int) -> None:
        for index, line in enumerate(self.lines):
            if line["item_id"] == item_id:
                del self.lines[index]
                return
        raise KeyError(f"item {item_id} is not in the cart")

    def total(self) -> float:
        return round(sum(line["price"] * line["qty"] for line in self.lines), 2)

    def __repr__(self) -> str:
        return f"<Cart {len(self.lines)} items, ${self.total():.2f}>"


if __name__ == "__main__":
    menu = load_menu()
    gyoza = menu[1]           # available
    miso = menu[3]            # NOT available

    cart = Cart()

    try:
        cart.add_item(gyoza, 0)
    except ValueError as e:
        print(f"Rejected: {e}")
 
    try:
        cart.add_item(miso, 1)
    except OutOfStockError as e:
        print(f"Rejected: {e}")
 
    try:
        cart.remove_item(99)
    except KeyError as e:
        print(f"Rejected: {e}")
 
    cart.add_item(gyoza, 2)
    print(cart)

    

