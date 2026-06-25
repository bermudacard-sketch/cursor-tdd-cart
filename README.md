# Cart Discount TDD Practice

## 목적

장바구니 할인 계산 로직을 **TDD(Test-Driven Development)** 방식으로 구현하는 연습 프로젝트입니다.

도메인 로직은 `src/cart.py`의 Entity 계층에 위치합니다. 테스트와 구현은 **계약 ID**(INV-*, E-*)를 기준으로 작성·추적합니다. 계약 ID는 테스트와 구현을 잇는 "추적의 못"이며, 사람 개발자와 AI 코딩 에이전트가 함께 참고하는 프로젝트 지도입니다.

**현재 단계: GREEN** — INV-1, E-1, E-2 구현 완료. 다음 계약은 INV-2. 상세 체크리스트는 아래 [INV-1, E-1, E-2 작업 체크리스트](#inv-1-e-1-e-2-작업-체크리스트)를 참고하세요.

상세 요구사항은 [docs/PRD.md](docs/PRD.md)를 참고하세요.

## 릴리스 노트

> **2026-06-25** · `513c7b0` → `3ff611b` (HEAD) · 첫 기능 릴리스

장바구니 소계 계산(INV-1)과 입력 검증(E-1, E-2)을 포함한 첫 기능 릴리스.

### ✨ 기능

- **INV-1 — 소계 계산**: `subtotal(items)`가 각 품목 `price × qty`의 합을 반환합니다.
- **E-1 — None 입력 검증**: `items`가 `None`이면 `TypeError`를 발생시킵니다.
- **E-2 — 음수 입력 검증**: `price` 또는 `qty`가 음수이면 `ValueError`를 발생시키며, 오류 메시지에 해당 품목 **인덱스**를 포함합니다.
- **Dual-Track TDD 프로젝트 구조**: Entity(`src/cart.py`) / Boundary(`tests/boundary/`) 계층 분리, pytest 기반 계약 ID(INV-*, E-*) 추적 체계를 도입했습니다.

### 🐛 버그 수정

- 해당 없음

### 🧹 기타

- INV-1, E-1, E-2 테스트 플랜 및 PRD, README 계약 ID 문서 추가
- RED → GREEN TDD 사이클에 따른 테스트·문서 커밋 정리
- Cursor export 커맨드 및 Prompting/Report 아카이브 추가

**테스트**: `pytest -q` — 4 passed

## 핵심 원칙

- **ID에 없는 동작은 만들지 않는다.** 계약 표에 없는 할인·예외·기능은 구현하지 않습니다.
- **테스트가 먼저다.** 구현보다 실패하는 테스트가 항상 앞섭니다.
- **RED → GREEN → REFACTOR** 순서를 따릅니다.
  - RED: `tests/`만 수정. `src/`는 건드리지 않습니다.
  - GREEN: 해당 계약 ID를 만족하는 최소 구현만 추가합니다.
  - REFACTOR: 전부 통과한 뒤에만 구조를 정리합니다.
- **과잉 구현을 금지한다.** 요청·계약에 없는 기능, 정책, 예외 처리를 미리 넣지 않습니다.

## 계약 ID 목록

| ID    | 계약(불변식 / 에러)                                                 | 근거 레벨 | 계층        |
| ----- | ------------------------------------------------------------ | ----- | --------- |
| INV-1 | `subtotal(items) == Σ(price × qty)`                          | —     | Entity    |
| INV-2 | `amount ≥ 50000 → round(amount×0.9)` / `< 50000 → 그대로` 경계 포함 | L1    | Entity    |
| INV-3 | `final = 문턱할인 적용 후, VIP면 round(×0.95)`. 순서 문턱→VIP 고정         | L2    | Entity    |
| INV-4 | 모든 입력에서 `0 ≤ final_total ≤ subtotal`. 할인은 금액을 늘리지 않는다        | L3    | Entity    |
| E-1   | `items is None → TypeError`                                  | L0    | Boundary* |
| E-2   | `price` 또는 `qty`가 음수 → `ValueError`, 인덱스 포함                  | L0    | Boundary* |

## 계약 ID 설명

- **INV-1** — 소계는 각 품목의 `단가 × 수량`을 모두 더한 값과 같아야 합니다.
- **INV-2** — 소계가 50,000원 이상이면 10% 할인(`round(소계 × 0.9)`), 미만이면 소계 그대로 반환합니다. 경계값(50,000원) 포함 여부는 L1 근거 기준으로 판단합니다.
- **INV-3** — VIP 고객은 문턱 할인을 적용한 **후** 금액에 5% 할인(`round(×0.95)`)을 적용합니다. 적용 순서는 문턱 → VIP로 고정됩니다.
- **INV-4** — 어떤 유효 입력에서도 최종 결제액은 0 이상이며 소계를 초과하지 않습니다. 할인은 금액을 늘리지 않습니다.
- **E-1** — `items`가 `None`이면 `TypeError`를 발생시킵니다.
- **E-2** — `price` 또는 `qty`가 음수이면 `ValueError`를 발생시키며, 오류 메시지에 해당 인덱스를 포함합니다. 0원을 반환하는 등의 우회는 금지됩니다.

## 계층 의미

- **Entity** — 순수 도메인 계산 로직을 담당합니다. Flask 등 외부 프레임워크를 import 하지 않습니다. INV-1 ~ INV-4가 이 계층의 핵심 계약입니다.
- **Boundary\*** — 입력 검증 경계에 가까운 규칙입니다. E-1, E-2는 원래 Boundary 계층에 해당하지만, **현재 실습에서는 도메인 함수 진입점**(`src/cart.py`)에서 검증합니다.

## 예상 파일 구조

```text
.
├── README.md
├── src/
│   └── cart.py          # Entity — subtotal(), calculate()
└── tests/
    ├── entity/
    │   └── test_cart.py # INV-* 불변식
    └── boundary/
        └── test_app.py  # E-* 입력 검증
```

## INV-1, E-1, E-2 작업 체크리스트

근거: [docs/TEST-PLAN-INV-1-E-1-E-2.md](docs/TEST-PLAN-INV-1-E-1-E-2.md) §1 범위. 본 체크리스트는 아래 세 계약만 다룹니다.

| ID | 계약 | 근거 레벨 | 계층 |
|----|------|-----------|------|
| **INV-1** | `subtotal(items) == Σ(price × qty)` | — | Entity |
| **E-1** | `items is None` → `TypeError` | L0 | Boundary\* |
| **E-2** | `price` 또는 `qty`가 음수 → `ValueError`, 오류 메시지에 **인덱스** 포함 | L0 | Boundary\* |

\* E-1, E-2는 Boundary 계약이지만, 현재 실습에서는 `src/cart.py`의 `subtotal()` 진입점에서 검증합니다.

권장 사이클 순서: **INV-1 → E-2 → E-1**. 각 계약마다 RED → GREEN → REFACTOR를 완료한 뒤 다음 계약으로 넘어갑니다.

### RED 단계 (`tests/`만 수정, `src/` 금지)

공통

- [x] 테스트 함수명·docstring에 계약 ID(INV-1, E-1, E-2) 명시
- [x] `pytest.skip`, `assert True` 등 우회 없이 실패하는 assert·예외 검증 작성
- [x] `pytest -q` 실행 — 의도된 실패(또는 import 오류) 확인

**1. INV-1** — `tests/entity/test_cart.py`

- [x] `from src.cart import subtotal` import
- [ ] `test_inv_1_…` — 단일 품목: `[(12000, 3)]` → `36000` (T1, 가장 먼저 작성)
- [ ] `test_inv_1_…` — 인터뷰 대표 사례: `[(12000, 3), (30000, 1)]` → `66000` (T2)
- [ ] `test_inv_1_…` — 복수 품목: `[(10000, 2), (5000, 4), (3000, 1)]` → `43000` (T3)
- [ ] `test_inv_1_…` — 수량 1: `[(48000, 1)]` → `48000` (T4)
- [x] 할인·VIP 인자 사용하지 않음 (`subtotal`만 호출)

**2. E-2** — `tests/boundary/test_app.py` (INV-1 RED 이후)

- [x] `test_e_2_…` — 음수 수량, 인덱스 0: `[(12000, -1)]` → `ValueError`, 메시지에 `"0"` (T5, E-2 첫 RED)
- [x] `test_e_2_…` — 음수 단가, 인덱스 0: `[(-100, 1)]` → `ValueError`, 메시지에 `"0"` (T6)
- [ ] `test_e_2_…` — 두 번째 품목 음수 수량, 인덱스 1: `[(12000, 3), (30000, -1)]` (T7)
- [ ] `test_e_2_…` — 두 번째 품목 음수 단가, 인덱스 1: `[(12000, 3), (-500, 1)]` (T8)
- [x] `pytest.raises(ValueError)` + `assert "<인덱스>" in str(exc_info.value)`
- [x] 0원 반환으로 우회하는 테스트 없음 (OOS-7)

**3. E-1** — `tests/boundary/test_app.py` (E-2 GREEN 이후)

- [x] `test_e_1_…` — `subtotal(None)` → `TypeError` (T9)
- [ ] `test_e_1_…` — `calculate(None, vip=True)` → `TypeError` (T10, `calculate` export 시)
- [x] `pytest.raises(TypeError)` — `ValueError` 아님

### GREEN 단계 (`src/cart.py` 최소 구현)

공통

- [x] RED에서 작성한 테스트만 통과시키는 최소 코드만 추가
- [x] 구현 줄에 충족한 계약 ID 주석 (`# INV-1`, `# E-2`, `# E-1`)
- [x] 할인·VIP·범위 밖 예외 처리 미리 넣지 않음
- [x] `pytest -q` 전체 통과 확인

**1. INV-1**

- [x] `src/cart.py`에 `subtotal(items)` 정의
- [x] 품목 리스트를 순회하며 `price × qty` 누적 합산
- [ ] T1 ~ T4 테스트 통과

**2. E-2**

- [x] 품목 순회 시 `price < 0` 또는 `qty < 0`이면 `ValueError` 발생
- [x] 예외 메시지에 해당 품목 인덱스(0, 1, …) 포함
- [ ] T5 ~ T8 테스트 통과

**3. E-1**

- [x] `subtotal()` (및 `calculate()` export 시) 최상단에서 `items is None` 검사
- [x] `None` 입력 시 `TypeError` 발생
- [ ] T9 ~ T10 테스트 통과

### 완료 기준

- [x] INV-1, E-2, E-1 관련 테스트 전부 통과
- [x] `pytest tests/entity -q` 통과
- [x] `pytest tests/boundary -q` 통과
- [x] `pytest -q` 통과
- [x] 구현에 `# INV-1`, `# E-2`, `# E-1` 주석 존재

## TDD 진행 순서 (전체 프로젝트)

1. **RED** — 계약 ID별 실패 테스트를 `tests/entity/`, `tests/boundary/`에 작성합니다. 테스트 이름·docstring에 계약 ID를 명시합니다.
2. **GREEN** — 해당 ID를 만족하는 최소 구현을 `src/cart.py`에 추가합니다. 구현 줄에 충족한 계약 ID를 주석으로 단습니다.
3. **REFACTOR** — 모든 테스트가 통과한 상태에서만 구조를 개선합니다. 리팩터 전후로 `pytest -q`로 동작 불변을 확인합니다.

권장 RED 진입 순서 (전체): INV-1 → INV-2(미달) → INV-2(문턱) → E-2 → INV-3 → INV-4 → E-1

## REFACTOR 계획 (Track B · subtotal)

E-2 검증 로직을 `_validate_line_items(items)` private 함수로 추출하는 구조 정리입니다. **적용 완료** — `pytest -q` 4 passed, 동작 불변.

### 목적

- **Mixed Responsibilities** 해소: `subtotal()` 안에 섞여 있는 E-2(음수 검증)와 INV-1(합산)을 분리합니다.
- E-2만 `_validate_line_items(items)`로 이동합니다. **E-1**(`items is None` → `TypeError`)은 `subtotal()` 진입점에 그대로 둡니다.

### 변경 범위

| 항목 | 내용 |
|------|------|
| 변경 파일 | `src/cart.py`만 |
| 테스트 | `tests/` 수정 없음 (동작 불변) |
| 예상 diff | `cart.py` **+3 ~ +5줄** |

### 제외 (이번 REFACTOR에서 하지 않음)

- `sum()` 변환
- `"price"` / `"qty"` 상수 추출
- `apply_threshold_discount`, `final_total`, `THRESHOLD` 등 INV-2 관련 함수·상수

### 동작 불변 체크리스트

REFACTOR 전후로 아래가 동일해야 합니다.

| 계약 | 입력 | 기대 |
|------|------|------|
| E-1 | `subtotal(None)` | `TypeError` (bare, 메시지 없음) |
| E-2 | `[{"price": 1000, "qty": -1}]` | `ValueError`, 메시지에 `"0"` 포함 |
| E-2 | `[{"price": -100, "qty": 1}]` | `ValueError`, 메시지에 `"0"` 포함 |
| INV-1 | `[{"price": 1000, "qty": 3}, {"price": 2000, "qty": 2}]` | `7000` |

### 완료 기준

- REFACTOR **전** `pytest -q` — GREEN
- REFACTOR **후** `pytest -q` — GREEN (4 passed, 동작 불변)

## 테스트 실행

```bash
pytest -q
```

`-q`는 quiet mode로, 테스트 결과를 간략히 출력합니다.

## 구현 금지 사항

- 할인 정책 추가 금지 (계약에 없는 새 할인율·문턱)
- 쿠폰, 세금, 배송비, 포인트 기능 추가 금지
- ID에 없는 예외 처리 추가 금지
- UI, CLI, DB, API 코드 추가 금지
