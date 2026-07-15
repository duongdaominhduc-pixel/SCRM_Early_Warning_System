# P3-04 — Evaluate Classifier C1

## Task này làm gì
Đánh giá best checkpoint của DistilBERT C1 trên test set (70 bài, chronologically newest).

## Output (tự động tạo bởi `P3-03/train_c1.py`)
| File | Mô tả |
|---|---|
| `evaluation_report_C1.md` | Báo cáo chính: Macro F1, Weighted F1, AUC-ROC, per-class F1, confusion matrix, training history |
| `test_predictions.csv` | 70 bài test + pred_label + prob_0/prob_1/prob_2 |

## Metrics mục tiêu
| Metric | Threshold pass |
|---|---|
| Macro F1 (test) | ≥ 0.72 |
| Weighted F1 | ≥ 0.80 |

## Ghi chú quan trọng
- Test set có 0 bài Label 2 (tất cả 5 bài Label 2 đều trong train)
- **HIGH_RISK(2) F1 trên test = N/A** — đây là hệ quả của chronological split, không phải lỗi
- AUC-ROC tính bằng `multi_class='ovr'` — nếu test không có class 2 thì bỏ qua
- Nếu Macro F1 < 0.72 → chạy P3-05 để retrain với hyperparameter khác
