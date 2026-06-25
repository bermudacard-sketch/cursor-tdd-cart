"""Boundary 계층 입력 검증 테스트."""

import pytest

from src.app import app
from src.cart import subtotal


@pytest.fixture
def client():
    return app.test_client()


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


@pytest.mark.boundary
def test_uc_1_get_root_returns_form_with_qty_input(client):
    """UC-1: GET / → 200, 본문에 name=\"qty\" 입력 포함."""
    response = client.get("/")

    assert response.status_code == 200
    assert 'name="qty"' in response.get_data(as_text=True)


@pytest.mark.boundary
def test_uc_2_post_calc_displays_final_total(client):
    """UC-2: POST /calc (price·qty·vip) → 본문에 final_total 결과 표시."""
    response = client.post(
        "/calc",
        data={"price": 60000, "qty": 1, "vip": "on"},
    )

    assert "51300" in response.get_data(as_text=True)


@pytest.mark.boundary
def test_ue_1_non_numeric_qty_returns_400(client):
    """UE-1: qty가 숫자가 아니면 400."""
    response = client.post(
        "/calc",
        data={"price": 60000, "qty": "abc"},
    )

    assert response.status_code == 400
