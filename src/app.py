"""Boundary: Flask 주문 폼 (Discovery 4.1).

계약:
- UC-1: GET / → 200, 본문에 qty·price·VIP 입력 폼 포함
- UC-2: POST /calc (price·qty·vip) → 본문에 final_total 결과 표시
- UE-1: qty가 숫자가 아니면 400 + 에러 메시지

ECB 역할:
- Boundary 계층. Entity(src.cart)의 final_total에 할인 계산을 위임한다.
- cart.py는 Flask를 import하지 않는다 (Entity 분리 유지).
"""

from flask import Flask, request

from src.cart import final_total  # Entity 위임 (할인 공식 재구현 금지)

app = Flask(__name__)

# SSOT 폼 필드: price, qty, vip(checkbox) — POST action="/calc"


@app.get("/")
def index():
    # UC-1: 200 + price, qty, vip(checkbox) 입력 폼
    return (
        '<form method="post" action="/calc">'
        '<input name="price" type="number">'
        '<input name="qty" type="number">'
        '<input name="vip" type="checkbox">'
        "</form>",
        200,
    )


@app.post("/calc")
def calc():
    qty_raw = request.form.get("qty", "")
    try:
        qty = int(qty_raw)  # UE-1
    except ValueError:
        return "qty must be a number", 400  # UE-1

    price = int(request.form.get("price", 0))
    is_vip = request.form.get("vip") == "on"
    items = [{"price": price, "qty": qty}]
    total = final_total(items, is_vip=is_vip)  # UC-2
    return str(total)  # UC-2
