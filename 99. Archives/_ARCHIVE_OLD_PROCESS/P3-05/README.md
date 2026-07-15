# P3-05 — Retrain (nếu Macro F1 < 0.72)

## Task này làm gì
Nếu kết quả P3-04 không đạt threshold (Macro F1 < 0.72), retrain với hyperparameter được điều chỉnh.

## Khi nào cần P3-05?
Chỉ thực hiện nếu `P3-04/evaluation_report_C1.md` báo `Macro F1 < 0.72`.

## Các hướng điều chỉnh (theo thứ tự ưu tiên)
| Thử | Thay đổi | Lý do |
|---|---|---|
| 1 | `lr = 3e-5` | lr thấp hơn → underfitting |
| 2 | Tăng oversampling Label 2 lên 10× | Model chưa học được class rare |
| 3 | Giảm `max_length = 256` | Giảm noise từ phần cuối article |
| 4 | `BATCH_TRAIN = 8` | Gradient update thường xuyên hơn |
| 5 | Thêm warmup dài hơn (20%) | Ổn định training đầu |

## Nếu vẫn không đạt sau khi retrain
**DECISION GATE**: Báo cáo nhóm và đề xuất ≥3 phương án:
- Option A: Hạ threshold xuống 0.65 (do imbalance nghiêm trọng)
- Option B: Chuyển sang 2-class (0 vs 1+2) để cải thiện recall
- Option C: Dùng `roberta-base` thay vì `distilbert` (tốn tài nguyên hơn)
