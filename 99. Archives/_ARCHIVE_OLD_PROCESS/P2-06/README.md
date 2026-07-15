# P2-06 — Gán nhãn 700 bài + Chronological Split (Train/Val/Test)

## Task này làm gì

Gán nhãn 700 bài báo đầu tiên (theo thứ tự chronological) từ `final_supplychain_news_2015_2018.jsonl`,
sau đó chia thành 3 tập Train/Val/Test theo **Chronological Split** (không shuffle).
Task này gộp P2-01 → P2-06 trong PCCV vì toàn bộ được thực hiện bằng AI thay vì human annotators.

## Cách gán nhãn

**Guideline:** C1 guideline (file `C1-Xác-định-chiến-lược-gắn-nhãn.docx`)
**Scope điều chỉnh:** Phương án 2 — thay "Electronics & Tech" → **"Aerospace & General Logistics"**

**Logic 5 câu hỏi (Decision Flowchart):**

| Bước | Câu hỏi | Kết quả |
|---|---|---|
| Stage 0 | Bài có tone tích cực (growth/profit/expansion) AND không có disruption signal? | → Label 0 |
| Q1 | Có disruption/risk signal không (shortage, delay, strike, sanction...)? | NO → Label 0 |
| Q2 | Sự kiện đã được xác nhận (confirmed), hay chỉ là dự báo/cảnh báo? | Chỉ forecast → Label 1 |
| Q3 | Phạm vi ảnh hưởng rộng (≥2 quốc gia / major hub / OEM lớn)? | NO → Label 1 |
| Q4 | Kéo dài > 14 ngày hoặc không rõ ngày phục hồi? | YES → Label 2 |
| Q5 | Lệnh chính phủ chính thức (tariff/sanction/ban) hoặc thiệt hại tài chính lớn? | YES → Label 2 |
| Default | Tất cả điều kiện trên không đủ | → Label 1 |

**Định nghĩa 3 nhãn:**
- **Label 0 — SAFE:** Không mô tả sự kiện nào ảnh hưởng đến sản xuất/logistics/tồn kho
- **Label 1 — LOW RISK:** Có rủi ro nhưng nhỏ/cục bộ/chưa xác nhận/chỉ là cảnh báo
- **Label 2 — HIGH RISK:** Sự kiện nghiêm trọng, đã xảy ra, ảnh hưởng rộng HOẶC kéo dài

## Output

| File | Mô tả | Rows |
|---|---|---|
| `labeled_700.xlsx` | 700 bài đã gán nhãn + notes | 700 |
| `train.csv` | 560 bài đầu tiên (oldest) | 560 |
| `val.csv` | 70 bài tiếp theo | 70 |
| `test.csv` | 70 bài cuối (newest) | 70 |
| `distribution_report.md` | Thống kê phân phối nhãn | — |

**Schema của labeled_700.xlsx:**

| Cột | Mô tả |
|---|---|
| url | URL gốc |
| source | joc.com / supplychainbrain.com |
| publish_date_parsed | Ngày đăng (datetime) |
| title | Tiêu đề |
| cleaned_content | Nội dung sạch |
| **label** | 0 / 1 / 2 |
| label_notes | Giải thích route qua flowchart |
| label_status | "ai_rule_based_v3" |

**Phân phối nhãn (kết quả cuối):**

| Label | Train | Val | Test | Total | % |
|---|---|---|---|---|---|
| 0 — SAFE | 366 | 48 | 50 | 464 | 66.3% |
| 1 — LOW RISK | 189 | 22 | 20 | 231 | 33.0% |
| 2 — HIGH RISK | 5 | 0 | 0 | 5 | 0.7% |

**Chronological Split:**
- 700 bài đã sorted theo `publish_date_parsed` ascending
- Train: bài 1–560 (2015-01-05 → khoảng 2015-08)
- Val: bài 561–630
- Test: bài 631–700 (oldest → newest trong mỗi tập)
- **KHÔNG shuffle** — đảm bảo temporal integrity (Phương án 1, Issue #02 trong PCCV)

## ⚠️ Vấn đề cần nhóm lưu ý

### 1. Class imbalance nghiêm trọng ở Label 2 (0.7%)

700 bài đầu cover Jan–Oct 2015. Đây là giai đoạn tương đối yên tĩnh sau khi West Coast port crisis kết thúc (tháng 2/2015). Các sự kiện lớn của corpus (Hanjin Shipping bankruptcy, Hurricane Harvey, trade war) đều nằm ở 2016–2017, thuộc phần 1300+ bài còn lại.

Toàn corpus chỉ có ~34/2554 bài có disruption keyword trong title — tỷ lệ này phản ánh đặc tính của JOC/SupplyChainBrain: đây là tạp chí trade, phần lớn nội dung là phân tích xu hướng và tin doanh nghiệp, không phải real-time breaking news về thiên tai.

**Hệ quả cho model C1:** Với 5 bài Label 2 trong training set, DistilBERT sẽ không học được class này đủ tốt.

**Khuyến nghị:**
- Dùng `class_weight='balanced'` khi fine-tune DistilBERT
- Kết hợp với class_weight trong loss function (weighted cross-entropy)
- Có thể oversampling label 2 (duplicate 5 bài → 20-30 bài)
- Hoặc: hạ xuống **2-class classification** (Label 0 = không rủi ro, Label 1+2 = có rủi ro), sau đó dùng ngưỡng probability để phân biệt mức độ. Quyết định này cần nhóm confirm.

### 2. Gán nhãn bằng AI rule-based, không phải human

Độ chính xác ước tính ~75-80% cho Label 0 và Label 1. Label 2 có độ tin cậy thấp hơn do pattern matching có false positive/negative.

Một số bài biên giới mà nhóm nên review thủ công (nếu có thời gian):
- "Manufacturers, Importers Losing Millions Due to West Coast Port Labor Problems" → hiện Label 1 (có thể là 2)
- "Ports on West Coast Could Remain Congested for Months" → hiện Label 1 (có thể là 2)
- "Hard Lessons in Disruption: What the West Coast Port Slowdown Really Taught Us" → hiện Label 1 (retrospective về sự kiện Label 2)

### 3. Label 0 có thể cao hơn thực tế (66%)

Nhiều bài analysis/technology/company news từ JOC/SCB được đưa vào Label 0. Đây là đặc tính của nguồn báo chuyên ngành — không phải lỗi logic. Nếu nhóm muốn tăng Label 1 (bằng cách xem bài analysis về risk trends cũng là "Low Risk"), cần điều chỉnh Q1 keyword hoặc Stage 0.

### 4. Val và Test đều có 0 bài Label 2

Do chronological split, tất cả 5 bài Label 2 đều nằm trong Training set. Điều này có nghĩa:
- Không đánh giá được Recall/Precision cho Label 2 trên Val/Test
- Khi báo cáo evaluation, nên note explicitly điều này

Nếu cần Label 2 trong Val/Test, có thể chuyển sang stratified split — nhưng điều đó vi phạm Phương án 1 (Issue #02). Quyết định này cần nhóm confirm.
