# P5-02 — Derive y_true (Inbound Ground Truth)

## Task này làm gì
Tạo biến mục tiêu `y_true` cho mỗi (part_group × week) từ dữ liệu vận hành thực tế.

## Định nghĩa y_true (Phương án A — đã được nhóm confirm)

```
y_true = 1 nếu:
  (A) stockout_flag = 1: on_hand_qty ≤ 0 trong bất kỳ ngày nào của tuần đó
  HOẶC
  (B) late_flag = 1: avg_delay ≥ 3 ngày VÀ pct_late ≥ 50% trong tuần đó
y_true = 0 nếu không thỏa mãn điều kiện nào
```

**Tại sao dùng threshold (avg_delay ≥ 3 AND pct_late ≥ 50%)?**
Dataset có 55.85% PO đến trễ → nếu dùng "any late delivery" thì positive rate = 98.2%, model trivially predict all-1. Threshold lọc ra chỉ những tuần có vấn đề thực sự nghiêm trọng.

## Kết quả thực tế
| Metric | Giá trị |
|---|---|
| Total (part_group × week) | 1,331 |
| Positive (y_true=1) | 712 (53.5%) |
| Negative (y_true=0) | 619 (46.5%) |
| Stockout-only | 683 |
| Late-only (threshold) | 22 |
| Cả hai | 7 |

## Output
- `y_true.parquet`: 1,331 rows × cols: part_group, week, stockout_flag, late_flag, avg_delay, pct_late, y_true
- `y_true.csv`: bản CSV để inspect

## Trạng thái
**DONE — dùng real data từ P4-01.**

---

## Ghi chú: 3 phương án định nghĩa y_true (DECISION GATE 2026-06-21)

Phát hiện trong quá trình chạy: positive rate = 98.2% khi dùng định nghĩa gốc. Nhóm đã họp và chọn Phương án A.

| | Phương án | Định nghĩa | Positive rate | Lý do bác bỏ / chọn |
|---|---|---|---|---|
| **A ✓** | **Threshold on delay** | y=1 nếu avg_delay ≥ 3 ngày AND pct_late ≥ 50% | ~53% | **ĐƯỢC CHỌN** — realistic, threshold có thể justify bằng lead_time_days trong paper |
| B | Stockout-only | y=1 chỉ khi on_hand_qty ≤ 0 | ~5% | Quá imbalanced (95% negative), recall sẽ rất thấp |
| C | Composite score | y=1 nếu TTS < 14d OR (avg_delay > 5d AND pct_late > 40%) | ~35% | Phức tạp hơn, khó giải thích trong paper, threshold TTS=14d chưa có cơ sở rõ ràng |

**Khi viết paper (P7-02):** cần giải thích tại sao chọn threshold avg_delay ≥ 3 ngày và pct_late ≥ 50%. Có thể tham chiếu: "threshold được chọn dựa trên phân tích phân phối delay trong dataset, loại bỏ nhiễu từ các chậm trễ nhỏ không ảnh hưởng đến sản xuất."
