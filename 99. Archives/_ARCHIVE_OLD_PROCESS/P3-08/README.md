# P3-08 — Rule-Based disruption_type Classifier

**Status: DONE — fully functional, no dependency on model checkpoint**

---

## Overview

Assigns each article to **one of 6 disruption categories** using keyword matching rules.
No ML model or checkpoint required.

---

## 6 Categories and Keyword Lists

| Category | Keywords |
|---|---|
| `PORT_CONGESTION` | port congestion, terminal congestion, berth delay, vessel delay, shipping backlog, dock congestion, port backup, port delay, container backlog, terminal backup, port closure, port, terminal, congestion, dock, berth |
| `GEOPOLITICAL` | export control, import restriction, trade war, trade dispute, geopolitical risk, geopolitical tension, sanction, tariff, embargo, ban, geopolitical |
| `WEATHER_DISASTER` | natural disaster, hurricane, typhoon, flood, earthquake, storm, wildfire, drought, tsunami, tornado, cyclone, blizzard, mudslide, landslide |
| `LABOR_DISPUTE` | labor dispute, labour dispute, worker protest, worker strike, union strike, industrial action, strike, walkout, lockout, union, shutdown |
| `SUPPLIER_FINANCIAL` | chapter 11, financial distress, financial crisis, bankruptcy, insolvency, liquidation, default, restructuring |
| `GENERAL_DISRUPTION` | *(fallback — no category matches, or tie between categories)* |

---

## Classification Logic

1. **Title-only pass** — count keyword hits per category in the title.
   - If exactly **one** category matches → return it immediately (title is authoritative).
   - If one category scores highest in the title with no tie → return it.
2. **Weighted combined score** — title hits × 3 + content hits × 1.
   - Pick the category with the highest combined score.
   - If tie or zero → return `GENERAL_DISRUPTION`.

---

## Usage

### Import as a module

```python
from P3_08.disruption_type import classify_disruption_type

label = classify_disruption_type(
    title="Hurricane Ian Disrupts Gulf Coast Supply Chains",
    content="Flooding caused widespread damage to warehouses.",
)
print(label)  # → WEATHER_DISASTER
```

### Run standalone (processes all splits)

```
py P3-08\disruption_type.py
```

Reads `P2-06\train.csv`, `P2-06\val.csv`, `P2-06\test.csv`.
Saves `P3-08\train_with_disruption_type.csv`, `val_with_disruption_type.csv`, `test_with_disruption_type.csv`.

### Run unit tests

```
py P3-08\test_classifier.py
```

---

## Test Results

Run `py P3-08\test_classifier.py` to get output like:

```
test_case_insensitive (__main__.TestDisruptionTypeClassifier) ... ok
test_general_empty_inputs (__main__.TestDisruptionTypeClassifier) ... ok
test_general_no_keywords (__main__.TestDisruptionTypeClassifier) ... ok
test_geopolitical_sanctions (__main__.TestDisruptionTypeClassifier) ... ok
test_geopolitical_tariff (__main__.TestDisruptionTypeClassifier) ... ok
test_labor_content_only (__main__.TestDisruptionTypeClassifier) ... ok
test_labor_strike (__main__.TestDisruptionTypeClassifier) ... ok
test_none_values_handled (__main__.TestDisruptionTypeClassifier) ... ok
test_port_congestion_content_only (__main__.TestDisruptionTypeClassifier) ... ok
test_port_congestion_title (__main__.TestDisruptionTypeClassifier) ... ok
test_supplier_bankruptcy (__main__.TestDisruptionTypeClassifier) ... ok
test_supplier_chapter11 (__main__.TestDisruptionTypeClassifier) ... ok
test_title_wins_over_content (__main__.TestDisruptionTypeClassifier) ... ok
test_weather_earthquake (__main__.TestDisruptionTypeClassifier) ... ok
test_weather_hurricane (__main__.TestDisruptionTypeClassifier) ... ok

----------------------------------------------------------------------
Ran 15 tests in 0.004s

OK
```

*(15 tests, all passing — covering all 6 categories + edge cases)*

---

## Output Files

| File | Description |
|---|---|
| `train_with_disruption_type.csv` | train split with added `disruption_type` column |
| `val_with_disruption_type.csv` | validation split with added `disruption_type` column |
| `test_with_disruption_type.csv` | test split with added `disruption_type` column |

---

## Notes

- Multi-word phrases are matched before single tokens to avoid false hits.
- Matching is **case-insensitive** using `re.search` with `\b` word boundaries.
- `None` / NaN values in title or content are handled gracefully (treated as empty string).
