# P3-03 — Fine-tune DistilBERT (Classifier C1)

## Task này làm gì
Fine-tune `distilbert-base-uncased` trên 560 bài train (+ oversampled Label 2) để phân loại rủi ro chuỗi cung ứng 3 class.

## Script chính
`train_c1.py` — chạy bằng lệnh:
```
py train_c1.py
```

Script này gộp P3-02 (DataLoader) + P3-03 (fine-tune) + P3-04 (eval) thành một pipeline hoàn chỉnh.

## Config
| Parameter | Giá trị |
|---|---|
| Model | distilbert-base-uncased |
| Input | `title + " [SEP] " + cleaned_content` (truncate 512 tokens) |
| Batch size (train) | 16 |
| Batch size (eval) | 32 |
| Learning rate | 2e-5 |
| Max epochs | 5 |
| Early stopping patience | 3 |
| Class weights | `balanced` (tính từ original train labels) |
| Label 2 oversampling | 5× (5 bài → ~25 bài) |

## Quyết định thiết kế (Phương án 1)
- **Chronological split**: không shuffle toàn bộ dataset, chỉ shuffle trong DataLoader khi train
- **3-class**: giữ nguyên Label 0/1/2 (không gộp 2-class)
- **class_weight='balanced' + oversampling**: Option A được nhóm confirm

## Output
| File | Mô tả |
|---|---|
| `best_model_c1/` | Best checkpoint (saved khi val macro_f1 cải thiện) |
| `training_history.json` | Loss + F1 mỗi epoch |
| `../P3-04/evaluation_report_C1.md` | Báo cáo đánh giá trên test set |
| `../P3-04/test_predictions.csv` | Predictions + probabilities cho 70 bài test |
| `../P3-01/requirements.txt` | Dependencies |

## Lưu ý
- Val và Test đều có 0 bài Label 2 → Macro F1 sẽ báo 0 cho class 2
- Dùng **Weighted F1** làm metric chính khi so sánh checkpoint
- Nếu Macro F1 trên test < 0.72 → xem xét retrain (P3-05)
