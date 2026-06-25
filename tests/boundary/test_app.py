"""Boundary 계층 입력 검증 테스트."""

import pytest

from src.cart import subtotal


@pytest.mark.boundary
def test_e_1_subtotal_none_raises_type_error():
    """E-1: items is None → TypeError."""
    with pytest.raises(TypeError):
        subtotal(None)


@pytest.mark.boundary
def test_e_2_negative_qty_raises_value_error_with_index():
    """E-2: 음수 qty → ValueError, 메시지에 인덱스 포함."""
    items = [{"price": 1000, "qty": -1}]

    with pytest.raises(ValueError) as exc_info:
        subtotal(items)

    assert "0" in str(exc_info.value)


@pytest.mark.boundary
def test_e_2_negative_price_raises_value_error_with_index():
    """E-2: 음수 price → ValueError, 메시지에 인덱스 포함."""
    items = [{"price": -100, "qty": 1}]

    with pytest.raises(ValueError) as exc_info:
        subtotal(items)

    assert "0" in str(exc_info.value)
