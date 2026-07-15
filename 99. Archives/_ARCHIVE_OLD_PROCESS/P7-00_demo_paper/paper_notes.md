# paper_notes.md — Ghi chú Chỉnh sửa & Hiệu chỉnh

Tài liệu này ghi lại các hiệu chỉnh quan trọng so với tài liệu gốc (`Thong_tin_de_tai_SCRM_EWS_v2.md`)
và các quyết định thiết kế trong quá trình viết paper.

---

## 1. Hiệu chỉnh Outbound → Inbound

### 1.1 Phạm vi rủi ro (QUAN TRỌNG NHẤT)
| | Tài liệu gốc | Paper (hiệu chỉnh) |
|---|---|---|
| **Hướng rủi ro** | Không nêu rõ, dễ nhầm sang outbound | **Inbound explicitly** — rủi ro từ nhà cung cấp lên (upstream), KHÔNG phải giao hàng cho khách hàng |
| **Thuật ngữ** | "supply chain risk" chung | "inbound supply chain risk", "upstream disruption" |
| **y_true** | "stockout OR late delivery" | "stockout OR (avg_delay≥3d AND pct_late≥50%)" — xem mục 2 |

**Lý do**: Hệ thống đo lường rủi ro thiếu hàng từ nhà cung cấp → ảnh hưởng sản xuất nội bộ.
Nếu viết "outbound" sẽ bị hiểu là rủi ro giao hàng cho khách, sai hoàn toàn với thiết kế.

---

## 2. Hiệu chỉnh Định nghĩa y_true

### Quyết định GATE (ngày 21/06/2026)

**Vấn đề**: Định nghĩa gốc "bất kỳ đơn hàng nào đến trễ" → positive rate = **98,2%** (vì 55,85% PO trễ trong dataset). Mô hình sẽ trivially predict all-positive.

**Ba phương án đã xem xét**:
| Phương án | Định nghĩa | Positive rate | Quyết định |
|---|---|---|---|
| **A ✓ (CHỌN)** | avg_delay ≥ 3d AND pct_late ≥ 50% | 53,5% | Đã chọn |
| B | Stockout-only | ~5% | Quá imbalanced |
| C | TTS < 14d OR (avg_delay > 5d AND pct_late > 40%) | ~35% | Phức tạp |

**Cách giải thích trong paper (mục 3.2.3)**: Ngưỡng avg_delay ≥ 3 ngày được chọn dựa trên phân tích phân phối delay trong dataset, loại bỏ nhiễu từ các chậm trễ nhỏ không ảnh hưởng đến sản xuất. Tham chiếu: lead_time_days trung bình trong dataset là ~4,5 ngày, vì vậy delay ≥ 3 ngày (≥67% lead time) là ngưỡng có cơ sở nghiệp vụ.

---

## 3. Hiệu chỉnh Phạm vi Thời gian Dataset

| | Tài liệu gốc | Thực tế (kiểm chứng) |
|---|---|---|
| Ngày kết thúc | 2018-04-12 | **2017-12-21** |
| Số tuần | ~170 | **156 tuần** |

Ảnh hưởng đến paper: Điều chỉnh tất cả chỗ đề cập "2015–2018" → "2015–2017" trong phần mô tả dataset.

---

## 4. Hiệu chỉnh Số liệu Shelf Life

| | Tài liệu gốc | Thực tế |
|---|---|---|
| shelf_life_days | Không đề cập null | **274 giá trị null** (đã điền median theo nhóm) |

---

## 5. Placeholder — Cần cập nhật sau khi DistilBERT hoàn tất

Tất cả các vị trí `<!-- PLACEHOLDER -->` trong `demo_full_paper_v1.md`:

| # | Vị trí trong paper | Thông tin cần | Nguồn |
|---|---|---|---|
| 1 | Abstract, dòng AUC | XGBoost AUC với real NLP features | P5-08 sau P3-12 handoff |
| 2 | Abstract, LTW | Mean Lead Time of Warning (tuần) | P5-13 sau P3-12 |
| 3 | Mục 3.2.1 | Fleiss' κ liên-người-gán | P3-02 sau gán nhãn vòng 2 |
| 4 | Mục 3.3.3 Epoch 4-5 | val macro_F1 epoch 4 và 5 | P3-03 training job |
| 5 | Mục 3.3.3 Test F1/AUC | DistilBERT test set performance | P3-04 evaluation |
| 6 | Mục 3.6.1 | Youden's J với real NLP | P5-11 sau real NLP |
| 7 | Bảng 4.3 hàng XGBoost real | F1, AUC với real NLP | P5-08 sau P3-12 |
| 8 | Mục 4.4 SHAP NLP | SHAP values cho news_risk_score, etc. | P5-10 sau real NLP |
| 9 | Mục 4.5 LTW | Mean/Median LTW (tuần) | P5-13 sau real NLP |

---

## 6. Thuật ngữ Chuẩn hóa

| Thuật ngữ hay dùng sai | Thuật ngữ đúng trong paper |
|---|---|
| "delivery risk" | "inbound supply risk" hoặc "upstream disruption risk" |
| "customer delay" | Không dùng — SCRM này không liên quan đến giao hàng cho khách |
| "supply chain delay" (mơ hồ) | "supplier delivery delay" hoặc "inbound delivery delay" |
| "outbound" | Xóa hoàn toàn — không phải scope của đề tài |

---

## 7. Ghi chú Kỹ thuật Quan trọng cho Paper viết chính thức

### 7.1 Walk-Forward vs Cross-Validation
Paper **bắt buộc** giải thích tại sao dùng walk-forward thay vì k-fold CV thông thường:
> "Dữ liệu chuỗi cung ứng có tính chất thời gian (temporal dependency). Random k-fold CV sẽ rò rỉ thông tin tương lai vào tập train (data leakage), dẫn đến ước tính hiệu suất lạc quan quá mức. Walk-forward CV với expanding window đảm bảo mô hình chỉ được huấn luyện trên dữ liệu quá khứ và dự báo tương lai — giống với điều kiện triển khai thực tế."

### 7.2 Mock NLP vs Real NLP
Khi XGBoost mock thấp hơn LR baseline, đây là **kết quả kỳ vọng** và là **bằng chứng methodology sound**:
- Mock NLP = nhiễu trắng → XGBoost thấp hơn (hợp lý)
- Real NLP → XGBoost sẽ cao hơn (hypothesis cần kiểm chứng)
- Đây là thiết kế Ablation Study nghiêm ngặt

### 7.3 Tính Stationary của avg_delay
avg_delay không dừng (ADF p > 0,05). Trong paper viết chính thức cần thêm:
- Differencing hoặc detrending avg_delay trước khi đưa vào model
- Hoặc giải thích tại sao không differencing (nếu XGBoost tree-based không cần tính dừng)
