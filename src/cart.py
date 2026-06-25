def _validate_line_items(items):
    for index, item in enumerate(items):
        price = item["price"]
        qty = item["qty"]
        if price < 0 or qty < 0:  # E-2
            raise ValueError(f"index {index}")


THRESHOLD = 50000


def apply_threshold_discount(amount):
    if amount >= THRESHOLD:  # INV-2
        return round(amount * 0.9)  # INV-2
    return amount  # INV-2


def subtotal(items):
    if items is None:  # E-1
        raise TypeError

    _validate_line_items(items)

    total = 0
    for item in items:
        total += item["price"] * item["qty"]  # INV-1

    return total
