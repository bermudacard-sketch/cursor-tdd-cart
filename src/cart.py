def _validate_line_items(items):
    for index, item in enumerate(items):
        price = item["price"]
        qty = item["qty"]
        if price < 0 or qty < 0:  # E-2
            raise ValueError(f"index {index}")


THRESHOLD = 50000
THRESHOLD_RATE = 0.9


def apply_threshold_discount(amount):
    if amount >= THRESHOLD:  # INV-2
        return round(amount * THRESHOLD_RATE)  # INV-2
    return amount  # INV-2


def subtotal(items):
    if items is None:  # E-1
        raise TypeError

    _validate_line_items(items)

    total = 0
    for item in items:
        total += item["price"] * item["qty"]  # INV-1

    return total


def final_total(items, is_vip=False):
    total = subtotal(items)
    total = apply_threshold_discount(total)  # INV-3
    if is_vip:
        total = round(total * 0.95)  # INV-3
    return total  # INV-4
