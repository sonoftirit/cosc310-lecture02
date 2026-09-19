# COSC 310 — Lecture 2 Exercises

Python exercises building a small restaurant ordering cart, covering menu
filtering, class design, business-rule enforcement, Git workflow, and testing.

## Layout

| Path | What it is |
|---|---|
| `exercise1.py` | Loads `data/menu.json` and lists available items under a price limit |
| `exercise2.py` | `Cart` class: add, remove, clear, total |
| `exercise3.py` | `Cart` extended so invalid operations are rejected by the cart itself |
| `tests/test_cart.py` | pytest suite for cart behaviour and business rules |
| `data/menu.json` | Menu data |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

```bash
python exercise1.py
python exercise2.py
python exercise3.py
pytest -v
```

## Business rules

Enforced inside `Cart` (`exercise3.py`), not at the call site:

- `ValueError` — quantity below 1
- `OutOfStockError` — item's `available` field is `False`
- `KeyError` — removing an item that is not in the cart
