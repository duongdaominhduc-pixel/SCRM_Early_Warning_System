# P4-05 — 3D Soft Join: Time × Geography × Category

## Task này làm gì
Link mỗi structured_risk_event (từ NLP Layer) vào các hàng Feature Matrix theo 3 chiều:
- **T (Time):** event_week nằm trong [feature_week - 4, feature_week]
- **G (Geography):** event_country khớp với supplier_country của part_id đó
- **C (Category):** disruption_type có liên quan đến part_family (theo CATEGORY_MAP)

## Output per (part_id, week)
| Cột | Mô tả |
|---|---|
| `news_risk_score` | max severity_score của event khớp (0 nếu không có match) |
| `disruption_event_flag` | 1 nếu có ≥1 event khớp, else 0 |
| `severity_score_nlp` | = news_risk_score (alias) |

## Files
| File | Mô tả |
|---|---|
| `soft_join_3d.py` | Script chính — hàm `soft_join_3d()` importable |
| `soft_join_mock_output.parquet` | Output test với mock events |

## Trạng thái
**Sườn xong, chờ data thật.**

Phần còn thiếu:
1. `structured_risk_events.csv` từ **P3-10** (chờ DistilBERT xong)
2. Feature Matrix rows từ **P4-06** (chờ P4-01 → P4-05)

Khi có data thật: trong `soft_join_3d.py`, thay `load_events()` bằng:
```python
events = load_events(BASE / 'P3-10' / 'structured_risk_events.csv')
```

## CATEGORY_MAP (logic phân loại liên quan)
| disruption_type | Part families bị ảnh hưởng |
|---|---|
| PORT_CONGESTION | Tất cả |
| GEOPOLITICAL | AVIONICS, PROPULSION, ELECTRICAL |
| WEATHER_DISASTER | Tất cả |
| LABOR_DISPUTE | AEROSTRUCTURES, LANDING_GEAR, PROPULSION |
| SUPPLIER_FINANCIAL | AVIONICS, HYDRAULICS, ELECTRICAL |
| GENERAL_DISRUPTION | Tất cả |

## Test với mock data
```
py soft_join_3d.py
```
Kết quả: match rate ~5-15% (phụ thuộc random seed), logic join chạy đúng.
