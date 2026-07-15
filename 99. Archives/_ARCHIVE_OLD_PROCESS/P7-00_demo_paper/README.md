# P7-00_demo_paper — Bản Demo Paper

Thư mục này chứa bản demo full paper để gửi thầy/người hướng dẫn xem trước.

## Nội dung thư mục

| File | Mô tả |
|---|---|
| `demo_full_paper_v1.md` | Full paper tiếng Việt, cấu trúc IMRaD đầy đủ |
| `pipeline_diagram.mmd` | Source Mermaid cho sơ đồ pipeline (mở bằng mermaid.live) |
| `pipeline_diagram.png` | Sơ đồ pipeline render bằng Python (chạy render_diagram.py) |
| `render_diagram.py` | Script Python render sơ đồ (dùng matplotlib, không cần mermaid-cli) |
| `paper_notes.md` | Ghi chú hiệu chỉnh outbound→inbound và các quyết định design |
| `for_advisor.md` | **Đọc trước** — Báo cáo tình trạng dự án gửi thầy |
| `README.md` | File này |

---

## Hướng dẫn đọc paper

### Ký hiệu Placeholder
Tất cả số liệu chưa có thực được đánh dấu rõ ràng:
```
<!-- PLACEHOLDER: mô tả -->
```
Danh sách đầy đủ các placeholder → xem `paper_notes.md` mục 5.

### Số liệu đã có thực (không phải mock)

| Kết quả | Giá trị | Nguồn |
|---|---|---|
| LR Baseline F1 | 0,7398 | P5-07 (real data) |
| LR Baseline AUC | 0,7159 | P5-07 (real data) |
| LR Baseline Recall | 0,8355 | P5-07 (real data) |
| DistilBERT Epoch 2 val macro-F1 | 0,5749 | P3-03 (đang train) |
| DistilBERT Epoch 3 val macro-F1 | 0,6599 | P3-03 (đang train) |
| Feature matrix | 1.248 × 10, 156 tuần | P5-01 (real data) |
| y_true positive rate | 53,5% | P5-02 (real data) |
| SHAP top feature (burn_rate) | 0,477 | P5-10 (real model) |
| Dataset: total POs | 29.666, 55,85% late | P4-01 (real data) |
| Dataset: inventory records | 280.800 bản ghi | P4-02 (real data) |
| Disruption types (GENERAL dominant) | 423/700 | P3-08 (real data) |

### Số liệu Mock (đặc trưng NLP — sẽ thay thế)

| Kết quả | Trạng thái | Khi nào có thật |
|---|---|---|
| XGBoost với real NLP: F1, AUC | MOCK | Sau khi P3-12 handoff |
| Lead Time of Warning | MOCK (2,5 tuần từ data giả) | Sau P5-13 với real alerts |
| Youden's J final threshold | MOCK (0,48) | Sau real XGBoost predictions |
| SHAP NLP features | 0 (mock = noise) | Sau P3-12 |
| DistilBERT test F1/AUC | PLACEHOLDER | Sau epoch 5 hoàn tất |
| Fleiss' κ inter-annotator | PLACEHOLDER | Sau gán nhãn vòng 2 |

---

## Cách render sơ đồ pipeline

### Option 1: Python (khuyến nghị, không cần internet)
```bash
cd P7-00_demo_paper
python render_diagram.py
# → tạo file pipeline_diagram.png
```

### Option 2: Mermaid Live (online)
1. Mở https://mermaid.live/
2. Copy nội dung `pipeline_diagram.mmd` vào editor
3. Export PNG/SVG

---

## Cập nhật paper khi có kết quả thật

1. Chạy DistilBERT hoàn tất → lấy test F1/AUC từ `P3-04/evaluation_report_C1.md`
2. Chạy P3-12 để tạo `structured_risk_events.csv` với real NLP features
3. Chạy lại P5-01 → P5-13 với real NLP features
4. Tìm tất cả `<!-- PLACEHOLDER -->` trong `demo_full_paper_v1.md` và thay thế
5. Cập nhật bảng so sánh mô hình (mục 4.3) với kết quả thật
6. Cập nhật LTW (mục 4.5) với real LTW

Ước tính: ~2-4 tiếng để cập nhật sau khi có đủ pipeline kết quả.
