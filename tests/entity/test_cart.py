"""Entity 계층 불변식 테스트."""

import pytest

from src.cart import apply_threshold_discount, final_total, subtotal


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


@pytest.mark.entity
def test_inv_3_vip_discount_applied_after_threshold():
    """INV-3: 문턱 할인 후 VIP면 round(×0.95), 60000→54000→51300."""
    items = [{"price": 60000, "qty": 1}]

    assert final_total(items, is_vip=True) == 51300


@pytest.mark.entity
@pytest.mark.parametrize(
    "items,is_vip",
    [
        ([], False),
        ([], True),
        ([{"price": 49999, "qty": 1}], False),
        ([{"price": 49999, "qty": 1}], True),
        ([{"price": 50000, "qty": 1}], False),
        ([{"price": 50000, "qty": 1}], True),
    ],
)
def test_inv_4_final_total_within_bounds(items, is_vip):
    """INV-4: 0 <= final_total <= subtotal."""
    st = subtotal(items)
    final = final_total(items, is_vip=is_vip)

    assert 0 <= final <= st
