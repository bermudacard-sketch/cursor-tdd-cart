# Test Plan — INV-1, E-1, E-2

| 항목 | 내용 |
|------|------|
| 대상 계약 | INV-1, E-1, E-2 |
| 근거 문서 | [README.md](../README.md), [PRD.md](PRD.md), [AGENTS.md](../AGENTS.md) |
| 작성일 | 2026-06-24 |
| 단계 | RED 준비 — 본 문서는 실패 테스트 작성 전 테스트 설계서 |

---

## 1. 범위

본 테스트 플랜은 아래 세 계약만 다룬다. 계약 ID에 없는 동작은 테스트·구현 모두 금지한다.

| ID | 계약 | 근거 레벨 | 계층 |
|----|------|-----------|------|
| **INV-1** | `subtotal(items) == Σ(price × qty)` | — | Entity |
| **E-1** | `items is None` → `TypeError` | L0 | Boundary\* |
| **E-2** | `price` 또는 `qty`가 음수 → `ValueError`, 오류 메시지에 **인덱스** 포함 | L0 | Boundary\* |

\* E-1, E-2는 Boundary 계약이나, **현재 실습에서는** `src/cart.py`의 도메인 함수 진입점에서 검증한다 ([README.md](../README.md) 계층 의미 참고).

### 범위 밖 (본 플랜에서 다루지 않음)

- INV-2 ~ INV-4, AC-2 ~ AC-4, E-3
- 빈 리스트 `[]` 처리 (E-3, Boundary)
- 소수 단가·수량 (OOS-8)
- 음수 입력 시 0원 반환 (OOS-7 — **반드시 예외**)

---

## 2. 전제 조건

### 2.1 데이터 형식

품목은 `(price, qty)` 튜플의 리스트로 표현한다.

```python
items: list[tuple[int, int]]  # (단가 원, 수량)
```

### 2.2 대상 API (예상)

PRD 및 README 기준 예상 시그니처. TDD 진행 중 확정되며 **임의 변경 금지**.

```python
# src/cart.py
def subtotal(items: list[tuple[int, int]]) -> int:
    """INV-1: Σ(price × qty)"""

def calculate(items: list[tuple[int, int]], vip: bool = False) -> int:
    """최종 결제액. E-1/E-2 검증은 진입점에서 수행."""
```

> INV-1은 `subtotal()` 단위로 검증하는 것을 권장한다. `calculate()`만 존재할 경우, 할인 미적용 경로(소계 그대로 반환)로 간접 검증할 수 있으나 **RED 1순위는 `subtotal` 직접 호출**이다.

### 2.3 테스트 배치

| 계약 | 권장 경로 | 비고 |
|------|-----------|------|
| INV-1 | `tests/entity/test_inv_1_subtotal.py` | 불변식 |
| E-1 | `tests/entity/test_e_1_none_items.py` | Entity 진입점 검증 (실습 범위) |
| E-2 | `tests/entity/test_e_2_negative_input.py` | Entity 진입점 검증 (실습 범위) |

`pytest tests/entity -q`로 세 계약 테스트를 한 번에 실행할 수 있어야 한다.

---

## 3. 테스트 케이스 — INV-1

**목표:** 어떤 유효한 `items`에 대해서도 `subtotal(items)`가 각 품목 `price × qty`의 합과 같다.

### 3.1 케이스 표

| # | 계약 ID | 설명 | 입력 `items` | 기대 `subtotal(items)` | 근거 |
|---|---------|------|--------------|------------------------|------|
| T1 | INV-1 | 단일 품목 | `[(12000, 3)]` | `36000` | 기본 합산 |
| T2 | INV-1 | 인터뷰 대표 사례 (AC-1 동일 입력) | `[(12000, 3), (30000, 1)]` | `66000` | L1 — A×3 + B×1 |
| T3 | INV-1 | 복수 품목 합산 | `[(10000, 2), (5000, 4), (3000, 1)]` | `43000` | 독립 검증 (20000+20000+3000) |
| T4 | INV-1 | 수량 1 | `[(48000, 1)]` | `48000` | #1042 소계 사례와 연결 |

### 3.2 RED 작성 가이드

```python
# tests/entity/test_inv_1_subtotal.py
# 계약: INV-1 — subtotal(items) == Σ(price × qty)

def test_inv_1_single_item():
  ...

def test_inv_1_interview_case_a3_b1():
  ...
```

- 테스트 함수명·파일 상단 주석에 **INV-1** 명시.
- `assert subtotal(...) == <기대값>` 형태. 할인·VIP 인자는 사용하지 않는다.
- T1을 **가장 먼저** RED로 작성한다 (가장 단순한 실패 테스트).

### 3.3 GREEN 최소 구현

- `subtotal`이 입력 리스트를 순회하며 `price * qty`를 누적 합산한다.
- 구현 줄에 `# INV-1` 주석.

### 3.4 의도적 제외

| 입력 | 제외 이유 |
|------|-----------|
| `[]` | 빈 장바구니는 E-3(Boundary) 범위 |
| `None` | E-1 범위 — INV-1 유효 입력이 아님 |
| 음수 `price`/`qty` | E-2 범위 — INV-1과 별도 RED 사이클 |

---

## 4. 테스트 케이스 — E-2

**목표:** 음수 `price` 또는 `qty`가 있으면 `ValueError`를 발생시키고, 메시지에 **문제 품목의 인덱스**가 포함된다. 0원 등 우회 반환 금지 (OOS-7).

README 권장 RED 순서상 **E-2는 INV-1 이후, E-1 이전**에 진행한다.

### 4.1 케이스 표

| # | 계약 ID | 설명 | 입력 | 호출 | 기대 |
|---|---------|------|------|------|------|
| T5 | E-2 | 음수 수량 (CS 사례) | `[(12000, -1)]` | `calculate(items)` 또는 `subtotal(items)` | `ValueError`, 메시지에 `"0"` 또는 `0` 인덱스 |
| T6 | E-2 | 음수 단가 | `[(-100, 1)]` | 동일 | `ValueError`, 인덱스 `0` |
| T7 | E-2 | 두 번째 품목 음수 수량 | `[(12000, 3), (30000, -1)]` | 동일 | `ValueError`, 인덱스 `1` |
| T8 | E-2 | 두 번째 품목 음수 단가 | `[(12000, 3), (-500, 1)]` | 동일 | `ValueError`, 인덱스 `1` |

### 4.2 검증 포인트

1. **예외 타입:** 반드시 `ValueError` (`pytest.raises(ValueError)`).
2. **인덱스 포함:** `str(exc.value)` 또는 `exc.value.args[0]`에 해당 인덱스가 들어 있어야 한다.
3. **0원 반환 금지:** 예외 없이 `0` 또는 양수를 반환하면 **실패** (버그 재현 금지).

### 4.3 RED 작성 가이드

```python
# tests/entity/test_e_2_negative_input.py
# 계약: E-2 — 음수 price/qty → ValueError (인덱스 포함)

def test_e_2_negative_qty_at_index_0():
  with pytest.raises(ValueError) as exc_info:
    calculate([(12000, -1)])
  assert "0" in str(exc_info.value)  # 또는 프로젝트에서 합의한 인덱스 표현
```

- T5(음수 수량, 인덱스 0)를 E-2의 **첫 RED**로 작성한다.
- 인덱스 표현 형식(예: `"index 0"`, `"at 0"`)은 GREEN 단계에서 메시지를 맞추되, **숫자 0/1이 메시지에 포함**되면 충분하다.

### 4.4 GREEN 최소 구현

- 품목 순회 시 `price < 0` 또는 `qty < 0`이면 `ValueError` 발생.
- 메시지에 루프 인덱스 포함. 구현 줄에 `# E-2` 주석.

---

## 5. 테스트 케이스 — E-1

**목표:** `items`가 `None`이면 `TypeError`를 발생시킨다.

README 권장 RED 순서상 **E-1은 INV-1·E-2 등 이후 마지막 근처**에 진행한다.

### 5.1 케이스 표

| # | 계약 ID | 설명 | 입력 | 호출 | 기대 |
|---|---------|------|------|------|------|
| T9 | E-1 | None items | `None` | `calculate(None)` | `TypeError` |
| T10 | E-1 | None + VIP 플래그 | `None` | `calculate(None, vip=True)` | `TypeError` |

### 5.2 검증 포인트

1. **예외 타입:** `TypeError` only (`ValueError` 아님).
2. `subtotal(None)`을 별도 export할 경우 동일 계약 적용.

### 5.3 RED / GREEN

```python
# tests/entity/test_e_1_none_items.py
# 계약: E-1 — items is None → TypeError

def test_e_1_calculate_none_raises_type_error():
  with pytest.raises(TypeError):
    calculate(None)
```

- GREEN: 함수 최상단에서 `items is None` 검사 후 `TypeError`. `# E-1` 주석.

---

## 6. RED → GREEN → REFACTOR 체크리스트

### 6.1 권장 사이클 순서

README 권장 진입 순서 중 본 플랜 해당 분:

| 순서 | 계약 | 첫 테스트 |
|------|------|-----------|
| 1 | INV-1 | T1 단일 품목 |
| 2 | E-2 | T5 음수 수량 |
| 3 | E-1 | T9 `calculate(None)` |

각 계약마다 **RED(테스트만) → GREEN(최소 구현) → REFACTOR(구조 정리)** 를 완료한 뒤 다음 계약으로 넘어간다.

### 6.2 사이클별 규칙

| 단계 | 허용 | 금지 |
|------|------|------|
| **RED** | `tests/`만 수정 | `src/` 수정, `pytest.skip`, `assert True` |
| **GREEN** | 계약 충족 최소 코드 + ID 주석 | 할인·VIP·추가 예외 처리 |
| **REFACTOR** | 구조 개선 (이름·추출 등) | 동작 변경, RED/GREEN 혼합 커밋 |

### 6.3 완료 기준

- [ ] T1 ~ T4 (INV-1) 전부 통과
- [ ] T5 ~ T8 (E-2) 전부 통과
- [ ] T9 ~ T10 (E-1) 전부 통과
- [ ] `pytest tests/entity -q` 통과
- [ ] 구현 코드에 `# INV-1`, `# E-1`, `# E-2` 주석 존재
- [ ] OOS-7 위반(음수 → 0원) 테스트·구현 없음

---

## 7. 실행 명령

```bash
# 본 플랜 범위 (Entity)
pytest tests/entity/test_inv_1_subtotal.py tests/entity/test_e_1_none_items.py tests/entity/test_e_2_negative_input.py -q

# Entity 전체
pytest tests/entity -q

# 저장소 전체 (다른 계약 테스트 추가 후)
pytest -q
```

---

## 8. 참고 — 계약과 AC 매핑

| 본 플랜 ID | 관련 AC / 사례 | 비고 |
|------------|----------------|------|
| INV-1 | AC-1 (소계 합산) | 동일 입력 `[(12000,3),(30000,1)]` → `66000` |
| E-2 | CS 음수 수량 버그 | 수량 -1 → 0원 표시는 OOS-7 (금지 동작) |
| E-1 | 빈 제출 500 오류의 Entity 측 | Boundary E-3은 별도 플랜 |

---

*본 문서는 docs/TEST-PLAN-INV-1-E-1-E-2.md — INV-1, E-1, E-2 계약용 테스트 설계서(2026-06-24)입니다.*
