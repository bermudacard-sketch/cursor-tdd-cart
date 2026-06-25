"""Entity 계층 불변식 테스트."""

import pytest

from src.cart import apply_threshold_discount, subtotal


@pytest.mark.entity
def test_inv_1_subtotal_equals_sum_of_price_times_qty():
    """INV-1: subtotal(items) == Σ(price × qty)."""
    items = [{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]

    assert subtotal(items) == 7000


@pytest.mark.entity
def test_inv_2_threshold_discount_applies_at_boundary():
    """INV-2: amount ≥ 50000 → round(amount × 0.9), 경계 포함."""
    assert apply_threshold_discount(50000) == 45000


@pytest.mark.entity
def test_inv_2_threshold_discount_not_applied_below_threshold():
    """INV-2: amount < 50000 → amount 그대로."""
    assert apply_threshold_discount(49999) == 49999
