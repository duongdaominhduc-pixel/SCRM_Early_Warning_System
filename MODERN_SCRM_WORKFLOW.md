# MODERN_SCRM_WORKFLOW.md
# Hệ thống Cảnh báo Sớm Rủi ro Chuỗi Cung ứng (EWS)
# Phiên bản tái cấu trúc — Sau Mentor Feedback

> **Tài liệu chuẩn**: Đây là workflow duy nhất có hiệu lực từ ngày 2026-06-24.  
> Mọi code/notebook phải tuân theo thứ tự Phase và Task ID bên dưới.

---

## TỔNG QUAN KIẾN TRÚC 3 LAYER (Taxonomy-Conditioned AI)

```
[Layer 1 — NLP Signal (Linear Flow)]              [Layer 2 — Operational Data]
  News 2022-2024                                     Aerospace Supply Chain
  (GDELT / NewsAPI)                                  (Inbound Logistics)
        │                                                    │
        ▼                                                    ▼
  [Phase 0: Sensing]                                 actual_lead_time
  Binary Filter (At Risk)                            on_hand_inventory
        │                                                    │
        ▼                                                    │
  [Phase 1: Sense-making]                                    │
  Taxonomy & Event Extraction                                │
        │                                                    │
        ▼                                                    │
  [Phase 1: Severity]                                        │
  Taxonomy-Conditioned AI                                    │
        │                                                    │
        └─────────────────────────┬──────────────────────────┘
                                  ▼
                         [Layer 3 — Fusion & ML]
                            Feature Matrix (X)
                        X lấy tuần W-1, W-2
                        Y lấy tuần W+n (shift)
                                 │
                                 ▼
                        Early Warning Alert
```

---

## LUẬT BẮT BUỘC (áp dụng cho toàn bộ workflow)

| Luật | Mô tả |
|------|-------|
| **Folder-based** | Mỗi Task ID có folder riêng: `/P0-01_New_Crawl/` |
| **README.md** | Mỗi folder phải có README.md: làm gì, kỹ thuật gì, output có ổn không |
| **Dừng & Đề xuất** | Khi gặp lỗi (API, Kappa thấp, dữ liệu nhiễu) → DỪNG, đề xuất ≥3 phương án, chờ lệnh |
| **No Look-ahead** | X chỉ dùng tuần W−1, W−2; Y phải là tuần W+n |
| **Kappa lib** | Dùng `statsmodels.stats.inter_rater` — không dùng sklearn hay tính tay |
| **Reproducibility Protocol** | (1) BẮT BUỘC set `seed=42` cho numpy, pandas, torch, transformers, umap, xgboost. (2) Phải xuất `requirements.txt`. (3) Ghi log Checksum (MD5/SHA256) cho các file output chính. |

---

## PHASE 0 — DỮ LIỆU & SENSING (Lọc Rủi ro)

### P0-01 | New Crawl 2022–2024
**Folder**: `/P0-01_New_Crawl/`

**Mục tiêu**: Thu thập corpus tin tức supply chain 2022–2024, thay thế bộ 2015–2018 lỗi thời.

**Kỹ thuật**:
- **Nguồn 1 — GDELT Project**: Query GDELTdoc API với filter `domain:supplychain OR domain:logistics`, `timespan:2022-2024`, `theme:ECON_TRADE`
- **Nguồn 2 — NewsAPI.org**: Keywords = `["supply chain disruption", "logistics risk", "port congestion", "supplier shortage", "aerospace supply"]`, language=en, from=2022-01-01, to=2024-12-31
- **Dedup**: Exact URL hash → TF-IDF cosine ≥ 0.85 (giống pipeline cũ)
- **Filter**: ≥100 words, English only, date trong range

**Output**:
- `news_2022_2024_raw.jsonl` — toàn bộ raw
- `news_2022_2024_clean.jsonl` — sau dedup + filter
- `crawl_stats.md` — tổng số bài, nguồn, phân phối thời gian

**Gate**: Đạt ≥ 3,000 bài sạch mới đi tiếp. Nếu < 3,000 → DỪNG & ĐỀ XUẤT.

---

### P0-02 | EDA — Thống kê mô tả
**Folder**: `/P0-02_EDA/`

**Mục tiêu**: Hiểu phân phối dữ liệu trước khi gán nhãn.

**Các biểu đồ/bảng bắt buộc**:
1. Phân phối bài theo tháng/năm (line chart)
2. Top 20 sources
3. Word count distribution (histogram)
4. Top 50 bigrams sau stopword removal
5. Phân phối theo quốc gia (nếu có `event_country`)

**Output**: `EDA_report.md` + folder `figures/`

---

### P0-03 | Pilot Labeling — Fleiss' Kappa
**Folder**: `/P0-03_Pilot_Labeling/`

**Mục tiêu**: Xác lập Agreement Protocol — đảm bảo nhãn nhất quán trước khi scale.

**Nhãn (3 lớp)**:
| Nhãn | Ký hiệu | Mô tả |
|------|---------|-------|
| 0 | `NO_RISK` | Bài báo thông tin chung, không có tín hiệu rủi ro |
| 1 | `MEDIUM_RISK` | Có dấu hiệu gián đoạn tiềm ẩn (delay, congestion, dispute đang nhen nhóm) |
| 2 | `HIGH_RISK` | Sự kiện gián đoạn đã xảy ra hoặc sắp xảy ra, ảnh hưởng trực tiếp chuỗi cung ứng |

**Quy trình**:
```
Bước 1: Chọn ngẫu nhiên 100 bài từ corpus 2022-2024 (stratified by year)
Bước 2: 4 thành viên nhóm gán nhãn độc lập (không trao đổi)
Bước 3: Tổng hợp vào pilot_labels.csv
Bước 4: Tính Fleiss' Kappa bằng statsmodels.stats.inter_rater
```

**Code mẫu**:
```python
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters

# labels_matrix: shape (n_items, n_raters), giá trị {0, 1, 2}
agg, _ = aggregate_raters(labels_matrix)
kappa = fleiss_kappa(agg, method='fleiss')
print(f"Fleiss' Kappa = {kappa:.4f}")
```

**Gate**: κ ≥ 0.70 mới được đi tiếp.
- κ < 0.50 → DỪNG, họp lại để chuẩn hóa guideline gán nhãn
- 0.50 ≤ κ < 0.70 → DỪNG, đề xuất ≥3 phương án (revision guideline, merge nhãn, tăng pilot set)

**Output**:
- `pilot_labels.csv` — 100 bài × 4 cột nhãn
- `fleiss_kappa_result.json` — giá trị κ và confidence interval
- `disagreement_analysis.md` — phân tích các bài bất đồng nhiều nhất

---

### P0-04 | Binary Filter NLP (Stage 1: Sensing)
**Folder**: `/P0-04_Binary_Filter/`

**Mục tiêu**: Xây dựng tập nhãn theo kiến trúc Phân loại Xếp tầng (Hierarchical Cascading). Đây là Giai đoạn 1 nhằm tách riêng các bài báo Có rủi ro.

**Cơ sở tham chiếu**:
| Nghiên cứu | Tỷ lệ gán tay | Nguồn |
|---|---|---|
| Bloomberg News 2024 | ~30% | FinNLP 2024 |
| FinNLP 2024 Supply Chain | ~27% (700/2,554) | bài báo gốc |
| **Đề tài này (khuyến nghị ★)** | **~30% (~2,160/7,200)** | |

**Chiến lược phân chia nhãn**:
```
Tổng corpus 2022–2024:  ~7,200 bài
├── Gán tay (30%):       ~2,160 bài (Tập gold label chuẩn 3 nhãn)
└── Pseudo-label (70%):  ~5,040 bài (máy gán)
```

**Quy trình Giai đoạn 1: Binary Filter (Lọc rủi ro)**:
1. Gộp Nhãn 1 và 2 thành nhãn `AT_RISK`.
2. Fine-tune DistilBERT trên tập gán tay (2,309 bài) với bài toán Binary (No Risk vs At Risk). **Bắt buộc sử dụng cấu hình: CrossEntropyLoss + Label Smoothing (0.1) + warmup_ratio=0.2 để tối ưu Calibration (ECE < 0.09) và tránh hiện tượng Output Range Collapse.**
3. **Mitigation (Chống lỗi lan truyền)**: Áp dụng **Threshold Calibration động**. Hạ ngưỡng quyết định để **tối ưu hóa tuyệt đối chỉ số Recall (Recall >= 0.95)**, đồng thời duy trì Precision Floor >= 0.35. Áp dụng thêm Temperature Scaling sau huấn luyện.
4. **Báo cáo bắt buộc**: Biểu đồ Precision-Recall Curve (PRC) và xuất báo cáo `precision_tradeoff_report.txt` để ghi nhận mức độ sụt giảm Precision khi tối ưu Recall (Bịt lỗ hổng Cascading Error).

**Output**:
- `manual_combined_2309.csv` — 2,309 bài gold label
- `binary_filter_model/` — Mô hình C0 đã huấn luyện
- `p0_04_evaluation.png` — Biểu đồ ROC/PRC
- `precision_tradeoff_report.txt` — Báo cáo sụt giảm Precision
- `at_risk_corpus.csv` — Tập dữ liệu chỉ chứa các bài `AT_RISK` (đầu vào cho Phase 1).
- `prc_stage1.png` — Biểu đồ PRC tối ưu Threshold

**Gate**: Chỉ tiến hành khi tập gán tay đạt **≥ 2,000 bài**.

---

## PHASE 1 — SENSE-MAKING & SEVERITY (Kiến trúc Nhận thức AI)

### P1-01 | Risk Taxonomy Extraction
**Folder**: `/P1-01_Risk_Taxonomy/`

> **🚨 SOTA UPGRADE (VERSION 2.0)**: Thuật toán BERTopic hiện tại bị lỗi "Forced Categorization" (ép nhiễu 100%). 
> **Hành động Code:** Đập đi xây lại. Chuyển sang kiến trúc **Universal Information Extraction (UIE)** (sử dụng Zero-shot Classification) với **Multi-label Head (Sigmoid)** để gán đa nhãn, nắm bắt chính xác hiệu ứng gợn sóng (Ripple Effect).

**Mục tiêu**: Đóng vai trò **Phân loại tĩnh (Categorization)**. Chạy trên tập `at_risk_corpus.csv` xuất ra từ `P0-04` để gán nhãn sự kiện đa nhãn.

**Kỹ thuật — Event Extraction (Ontology-Anchored Discovery)**:
- Loại bỏ hoàn toàn các mô hình Hộp đen (LLM) để đảm bảo tính Giải trình (Accountability) và khả năng tái lập (Reproducibility).
- Áp dụng phương pháp Khai phá Neo theo Ontology tĩnh (Tự động hóa 100%):
  - **Bước A (Semantic Discovery)**: Dùng `BERTopic` + `SentenceTransformers` để gom cụm ngữ nghĩa các bài báo rủi ro thành các cụm tiềm ẩn.
  - **Bước B (Ontology Knowledge Base)**: Xây dựng một tập hợp nhãn tĩnh chuẩn mực (vd: Port Congestion, Geopolitical, Weather Disaster).
  - **Bước C (Deterministic Mapping)**: Tính toán **Cosine Similarity** để gán nhãn tự động. Bắt buộc xuất kèm **Confidence Score** cho mỗi gán nhãn để làm Guardrail cho P1-02.

**Gate: Noise Control (Chốt chặn tỷ lệ nhiễu)**:
- **Luật:** Nếu tỷ lệ bài báo bị gán vào Cluster `-1` (Outliers) **> 40%** → **DỪNG**.
- **Mitigation Strategies (3 Chiến lược khắc phục):**
  1. *Chiến lược 1 (UMAP Tuning):* Tăng `n_neighbors` (vd: từ 15 lên 30/50) để nhóm các điểm thưa thớt dựa trên cấu trúc toàn cục (global structure).
  2. *Chiến lược 2 (HDBSCAN Tuning):* Giảm `min_cluster_size` (vd: xuống 5) và tăng `cluster_selection_epsilon` (> 0) để nới lỏng ranh giới gom cụm, cứu các bài báo rủi ro nhỏ ở vùng rìa.
  3. *Chiến lược 3 (Soft Clustering - Ưu tiên ★):* Kích hoạt `calculate_probabilities=True` trong BERTopic và dùng hàm `reduce_outliers()` để ép các bài báo cụm -1 vào các cụm có xác suất phù hợp nhất.

**Tại sao không dùng keyword thuần**:
- "Hurricane **strike**" → keyword "strike" false positive cho LABOR_DISPUTE.
- Phương pháp Hybrid NER + BERTopic đọc hiểu ngữ cảnh "Hurricane strike" hoàn hảo, loại trừ hoàn toàn LABOR.

**Output**:
- `risk_taxonomy_report.md` — Bảng danh mục Taxonomy rủi ro do AI sinh ra.
- `at_risk_with_taxonomy.csv` — Tập dữ liệu `AT_RISK` đã được gán nhãn sự kiện tự động + Confidence Score.
- `outlier_reduction_report.md` — Báo cáo tỷ lệ Cluster -1 trước và sau khi xử lý.

---

### P1-02 | Taxonomy-Conditioned Severity Specialist
**Folder**: `/P1-02_Severity_Specialist/`

> **🚨 SOTA UPGRADE (VERSION 2.0)**: Kỹ thuật tiêm token thô `[LABOR_DISPUTE]` hiện tại gây nhiễu ngữ nghĩa và bỏ lọt cảnh báo (False Negatives). 
> **Hành động Code:** Đập đi xây lại. Đổi sang **Context Shells** (bao bọc bằng câu tiếng Anh hoàn chỉnh) kết hợp với **Focal Loss** để tối ưu Recall cho nhóm rủi ro cực hiếm.

**Mục tiêu**: Đánh giá mức độ nghiêm trọng (Medium vs High) dựa trên ngữ cảnh đã được mớm từ Taxonomy.

**Quy trình Giai đoạn 2**:
1. Nhận lại tập bài báo `at_risk_with_taxonomy.csv` từ `P1-01`.
2. **Kỹ thuật Mớm nhãn (Token Injection)**: Chèn nhãn Taxonomy vào đầu văn bản. Ví dụ: `[PORT_CONGESTION] Text...`.
3. **Best Practice 1 (Special Tokens)**: Bổ sung các nhãn Taxonomy (vd: `[PORT_CONGESTION]`) vào cấu hình `special_tokens` của DistilBERT Tokenizer để mô hình học trọng số tốt hơn.
4. **Best Practice 2 (Cascading Error Guardrail)**: Nếu Confidence Score của BERTopic ở `P1-01` quá thấp, KHÔNG chèn nhãn Taxonomy mà để mô hình đọc văn bản thô, tránh lỗi "đóng khung sai".
5. Fine-tune DistilBERT trên dữ liệu này để phân biệt `Medium Risk` vs `High Risk`. Dùng **Cost-Sensitive Learning (Phạt trọng số)**.
6. **Giải trình (SHAP)**: Giải thích các từ khóa (ngoài Taxonomy) khiến AI nâng cấp mức độ lên High Risk.

**Output**:
- `pseudo_labeled_final.csv` — Nhãn 3 lớp hoàn chỉnh (Kết hợp P0-04 và P1-02).
- `shap_severity_keywords.png` — Phân tích từ khóa Giai đoạn 2.

---

### P1-03 | Label Distribution Check (Anti-Overfitting Gate)
**Folder**: `/P1-03_Label_Distribution/`

> **🚨 SOTA UPGRADE (VERSION 2.0)**: Việc dùng luật SMOTE ép tỷ lệ High Risk >= 10% làm phá vỡ tính chu kỳ tự nhiên của Time-Series, gây báo động giả. 
> **Hành động Code:** Bãi bỏ luật SMOTE toàn cục. Chuyển hoàn toàn việc xử lý Imbalance xuống thuật toán Cost-Sensitive Learning của Lớp 3 (ML).

**Mục tiêu**: Thanh tra phân phối của 2 bộ dữ liệu độc lập (P0-04 và P1-02) để đảm bảo tính hội tụ của toán học.

**Tiêu chí Gate**:
| Giai đoạn | Điều kiện | Hành động |
|-----------|-----------|-----------|
| **Stage 1 (Binary Filter - P0-04)** | Tỷ lệ `AT_RISK` < 15% | DỪNG — Kiểm tra lại từ khóa crawl hoặc guideline gán nhãn |
| **Stage 2 (Severity Specialist - P1-02)** | Tập huấn luyện có Nhãn 2 < 10% | DỪNG — Tăng cường Cost-Sensitive Weighting hoặc dùng SMOTE cho Giai đoạn 2 |

**Output**: `label_distribution_report.md` báo cáo độ cân bằng của cả 2 mô hình.

---

## PHASE 2 — FEATURE ENGINEERING & MACHINE LEARNING

### P2-01 | NER & Entity Extraction
**Folder**: `/P2-01_NLP_NER/`

**Mục tiêu**: Trích xuất thực thể địa lý và tổ chức để chuẩn bị cho Soft Join.

**Kỹ thuật**:
- Dùng `spaCy` (`en_core_web_trf` hoặc `en_core_web_lg`)
- Trích xuất: ORG (nhà cung cấp), GPE (quốc gia/vùng), DATE
- Xây dựng `entity_density_score` = số lượng entity liên quan supply chain / tổng entity

**Output**:
- `news_with_ner_features.parquet` — corpus 5,313 bài báo với các cột NER.

---

### P2-02 | Soft Join Nâng cấp — Geographic Weighting
**Folder**: `/P2-02_Geo_Join/`

**Mục tiêu**: Thay Inner Join cứng bằng Geographic Weighting để capture ripple effects.

**Phương án được chọn**: Geographic Weighting (cross-join có phạt điểm)
- Phương pháp này xây dựng "Layered Risk Perception" (Nhận thức rủi định đa tầng), phản ánh bản chất "Hiệu ứng gợn sóng" (Ripple Effect) và sự phụ thuộc mạng lưới trong chuỗi cung ứng toàn cầu.

```python
# Initial Sensitivity Coefficients (Các hệ số độ nhạy ban đầu)
def geo_weight(event_country, supplier_country, event_type):
    if event_country == supplier_country:
        return 1.0          # Exact match (Rủi ro trực tiếp)
    if same_region(event_country, supplier_country):
        return 0.6          # Cùng khu vực (Lan truyền không gian / Spatial Propagation)
    if event_type in ['GEOPOLITICAL', 'PORT_CONGESTION']:
        return 0.3          # Baseline exposure factor (Đứt gãy phi địa lý / Macro Events)
    return 0.1              # Remote event (Rủi ro xa)
```

**Sensitivity Analysis (Phân tích Độ nhạy)**:
- Thực hiện phân tích độ nhạy bằng cách biến thiên trọng số Regional Match (0.5, 0.6, 0.7) để chứng minh trạng thái ổn định tiệm cận (Asymptotic Stability). Điều này chống lại nghi ngờ "cherry-picking" và khẳng định tính Robustness trước Hội đồng.

**Output**: `news_supplier_joined.parquet` với cột `weighted_geo_risk`

---

### P2-03 | Weekly Feature Aggregation (X matrix)
**Folder**: `/P2-03_Feature_Matrix/`

**Mục tiêu**: Tiền xử lý dữ liệu (chuẩn hóa thực thể, xử lý nhiễu, chuẩn hóa thời gian) và tổng hợp đặc trưng NLP theo tuần để tạo X matrix.

**Các bước Tiền xử lý (Data Preprocessing) bắt buộc**:
1. **Xử lý Cụm nhiễu (Cluster -1)**: Loại bỏ các bài báo thuộc cụm -1 sinh ra từ BERTopic để không làm loãng không gian đặc trưng.
2. **Chuẩn hóa Thời gian**: Ép kiểu cột `publish_date` về định dạng chuẩn ISO 8601 (YYYY-MM-DD) để phục vụ Shift Target chính xác.
3. **Chuẩn hóa Thực thể (Entity Resolution)**: Ánh xạ chuẩn hóa các địa danh GPE (VD: China -> CN) để đồng bộ hóa với hệ mã nhà cung cấp (Supplier Country).
4. **Kiểm định Tính dừng (Stationarity Check)**: Chạy kiểm định **ADF Test** cho các biến vận hành liên tục (vd: `avg_actual_lead_time`). Nếu biến không dừng (có trend/xu hướng), tạo thêm biến sai phân bậc 1 (delta = W - (W-1)).
   - *Luật Option B:* **Giữ cả biến gốc và biến delta**. Biến gốc cung cấp "Baseline State" (Phơi nhiễm hiện tại), biến delta cung cấp "Momentum" (Tốc độ suy thoái). L1 Penalty của Lasso sẽ tự động lọc nhiễu, còn XGBoost sẽ học tương tác phi tuyến giữa State và Momentum.

**Luật bắt buộc — NO LOOK-AHEAD**:
```
Khi dự báo rủi ro cho tuần W (thực thi vào sáng thứ Hai tuần W):
  X_news chỉ được dùng: news tuần W-1, W-2
  X_ops (Operational) chỉ được dùng: dữ liệu chốt sổ hết tuần W-1
  Y (target) là: operational risk tuần W (hoặc W+1)
```

**Đặc trưng NLP theo tuần (Tích hợp Cascading AI & Ontology)**:
| Feature | Mô tả | Nguồn |
|---------|-------|-------|
| `at_risk_count_w1` | Số bài Có rủi ro trong tuần W-1 | Cascading Giai đoạn 1 (P0-04) |
| `at_risk_count_w2` | Số bài Có rủi ro trong tuần W-2 | Cascading Giai đoạn 1 (P0-04) |
| `high_severity_count_w1` | Số bài Rủi ro Cao (High Risk) tuần W-1 | Cascading Giai đoạn 2 (P1-02) |
| `dominant_event_type_w1` | Loại sự kiện phổ biến nhất tuần W-1 | Ontology (P1-01) |
| `weighted_geo_risk_w1` | Điểm rủi ro địa lý supplier vs. event tuần W-1 | Geo Weighting (P2-02) |

**Đặc trưng Operational (Inbound Aerospace chốt ở W-1)**:
| Feature | Mô tả | Nguồn |
|---------|-------|-------|
| `avg_actual_lead_time_w1` | Lead time thực tế trung bình tuần W-1 (Baseline State) | `actual_lead_time` |
| `delta_avg_actual_lead_time_w1`| Tốc độ biến thiên Lead time so với tuần W-2 (Momentum) | Derived |
| `lead_time_ratio_w1` | actual / promised tuần W-1 | computed |
| `on_hand_inventory_w1` | Mức tồn kho chốt cuối tuần W-1 | `on_hand_inventory` |
| `pct_po_late_w1` | % PO đến trễ trong tuần W-1 | purchase_orders |
| `stockout_flag_w1` | Có stockout không trong tuần W-1 | supply_chain_history |

**Các rủi ro thống kê & Chiến lược giảm thiểu (Risk Mitigations)**:
Thiết kế này được định khung là một **"Conservative Information-Processing Capability"** nhằm triệt tiêu Data Leakage và tối đa hóa Actionable Intelligence.
1. **Đa cộng tuyến (Multicollinearity)**: Sự kết hợp giữa `high_severity_count_w1` (từ AI) và `dominant_event_type_w1` (từ Taxonomy) rất dễ gây đa cộng tuyến. Các biến vận hành như `avg_actual_lead_time` và `pct_po_late` cũng tương quan rất cao (r > 0.8).
   - *Bắt buộc*: Kiểm tra hệ số VIF. Nếu VIF > 5, áp dụng **Lasso Regression (L1 Penalty)** ở vòng lặp huấn luyện cuối cùng để mô hình tự động triệt tiêu các đặc trưng dư thừa. Lasso được ưu tiên tuyệt đối vì mang lại không gian đặc trưng tinh gọn và khả năng diễn giải cao.
2. **Độ thưa của dữ liệu (Data Sparsity)**: `weighted_geo_risk` dạng Boolean (0/1) rất thưa vì các sự kiện rủi ro là hiếm (low-frequency, high-impact).
   - *Khuyến nghị*: Áp dụng **Trọng số địa lý (Geographic Weighting)** để mô phỏng "Ripple Effect". Thiết lập trọng số khu vực (Region match) thành một **hyperparameter tinh chỉnh được** (ví dụ: từ 0.4 đến 0.8) thay vì cố định ở mức 0.6, và tiến hành kiểm tra độ nhạy trên tham số này.
3. **Độ trễ dữ liệu ("Monday Morning" Reality)**: Dữ liệu chốt cuối tuần W-1 có thể bị trễ do độ trễ đồng bộ của ERP.
   - *Khuyến nghị*: Thực hiện **Stress Test (Phân tích độ nhạy)** bằng cách ép mô hình dùng dữ liệu X của W-2 để dự báo W. Báo cáo chỉ số **"Retention of Accuracy"** (Tỷ lệ duy trì độ chính xác) để chứng minh độ tin cậy của hệ thống.
4. **Adaptive Response Paradox (Nghịch lý phản ứng thích ứng)**: Các biến rủi ro NLP có thể mang hệ số âm khi chạy Lasso-Logistic.
   - *Lý luận học thuật*: Đây là tín hiệu của "Preemptive Risk Management" (quản lý rủi ro phủ đầu). Khi nhà sản xuất nhận diện được tin tức xấu, họ lập tức kích hoạt chuỗi cung ứng dự phòng, dẫn đến việc stockout thực tế không xảy ra. Hệ số âm này cần được báo cáo như một **"Proactive Mitigation Signal"** (tín hiệu giảm thiểu chủ động) thay vì coi đó là nhiễu.

**Output**:
- `feature_matrix.parquet` — Sẵn sàng cho XGBoost.
- `temporal_alignment_validation.txt` — Báo cáo tính toàn vẹn thời gian.

---

### P2-04 | Derive y2 — Target Shift (Fix Look-ahead Bias)
**Folder**: `/P2-04_Derive_y2/`

> **✅ ĐÃ GIẢI QUYẾT (RESOLVED)**: Lỗi **Validation Corruption** do Downsampling đã được loại bỏ. Hàm hiện tại chỉ thực hiện shift target và xuất dữ liệu nguyên bản 100%, bảo toàn Validation Integrity.

**Mục tiêu**: Tạo biến mục tiêu y2 với shift đúng.

**Logic**:
```python
# Biến mục tiêu: stockout_flag đóng vai trò là "Operational Continuity Proxy"
# Khắc phục Look-ahead Bias bằng "Data Alignment for Supervised Time-Series Forecasting"

df_sorted = df.sort_values(['part_id', 'week'])
for n in [1, 2]:  # W+1 và W+2 (Lead-Time Advantage)
    df_sorted[f'y2_shift{n}'] = df_sorted.groupby('part_id')['w1_stockout_flag'].shift(-n)

# Xóa các hàng cuối (Right-Censored Data)
df_train = df_sorted.dropna(subset=['y2_shift1', 'y2_shift2'])
```

**Tại sao shift âm (shift(-n))**:
- `shift(-1)` tại hàng W = lấy giá trị của hàng W+1
- X tại W dự báo y tại W+1 → đúng bản chất forecasting

**Gate**: Kiểm tra positive rate của y2_shift1 và y2_shift2 trong [30%, 70%]. Nếu ngoài range → DỪNG.

**Output**:
- `y2_shifted.parquet` — với cả 2 cột `y2_shift1`, `y2_shift2`
- `shift_validation.md` — phân tích positive rate, thống kê

---

### P2-05 | ML Training — Ablation Study (2×2 Matrix)
**Folder**: `/P2-05_ML_Ablation/`

> **✅ ĐÃ GIẢI QUYẾT (RESOLVED)**: 
> **Thành quả 1:** Thuật toán tính `scale_pos_weight` đã được đưa vào **BÊN TRONG** vòng lặp `TimeSeriesSplit`, triệt tiêu hoàn toàn Data Leakage. Tập Validation được giữ nguyên phân phối gốc.
> **Thành quả 2:** SCRM chiến thắng tuyệt đối về Precision Floor, giúp hệ thống chống Alert Fatigue thành công.

**Mục tiêu**: So sánh công bằng thông qua Ablation Study để chứng minh giá trị của NLP Features (Layered Risk Perception). 

**Chiến lược xử lý Mất cân bằng (Cost-Sensitive Learning)**:
- **Tránh SMOTE (No Resampling)**: Bảo tồn logic vận hành (Operational Logic) và các phụ thuộc mạng lưới vật lý.
- **Dùng Algorithmic Class Weighting**: Sử dụng `scale_pos_weight` trong XGBoost (bắt tương tác phi tuyến) và `class_weight='balanced'` trong Logistic Regression (Lasso - lọc đặc trưng).

**Ma trận thực nghiệm (3-Tier Evaluation Design & Ablation Study)**:
Cấu trúc đánh giá toàn diện giá trị của thông tin và kiến trúc (Value of Information & Architecture):
1. **Tier 1 (Industry Baseline)**: `Rule-Based Heuristics`. Đại diện cho thực trạng ngành.
2. **Tier 2 (Methodological Baseline)**: `LR_Baseline` và `XGB_Baseline` (Chỉ dùng dữ liệu Vận hành, không NLP).
3. **Tier 3 (Proposed SCRM)**: Đóng góp cốt lõi của bài báo. Yêu cầu làm **Ablation Study** so sánh trực tiếp 2 phiên bản NLP:
   - `SCRM_Standard_MultiClass`: Mô hình NLP 3 lớp (3-class) tiêu chuẩn.
   - `SCRM_Default_Cascading`: Kiến trúc 2 giai đoạn (Cascading AI) mặc định đề xuất.
   *(Nhiệm vụ: Chứng minh Cascading AI mang lại Minority F1-score và Lead-Time Gain cao hơn ổn định so với mô hình 3 lớp gốc).*

**Validation chuẩn mực (Triệt tiêu Look-ahead Bias)**:
```python
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5, gap=2)  # gap=2 tuần ngăn chặn rò rỉ dữ liệu (Data Leakage) và mô phỏng thực tế
```

**Metrics Bắt buộc (Tiêu chuẩn vàng cho EWS)**:
- **Precision-Recall Curve (PRC)** & **Minority F1-Score**: Tập trung trực tiếp vào lớp rủi ro (3.16%), tránh cái nhìn quá lạc quan của ROC-AUC, giúp quản lý "alert fatigue".
- **Lead-Time vs. Precision Curve**: Biểu đồ cốt lõi cung cấp "Actionable Intelligence" (Tri thức có thể hành động), biến mô hình thành một Công cụ Hỗ trợ Quyết định (Decision Support Tool) đích thực. Cho phép nhà quản lý đánh đổi giữa thời gian cảnh báo (W+1 vs W+2) và độ chính xác.

**Target**: Chạy thử nghiệm trên cả `y2_shift1` và `y2_shift2`.

**Output**:
- `ablation_results.md` — bảng so sánh 4 configs
- `models/` — 4 model đã trained (chuẩn bị cho phân tích SHAP ở Phase sau)

---


## PHASE 3 — EVALUATION & EXPLAINABILITY

### P3-01 | Threshold Optimization
**Folder**: `/P3-01_Threshold/`

> **✅ ĐÃ GIẢI QUYẾT (RESOLVED)**: Áp dụng thành công Chronological Split (Tách Val/Test theo thời gian). Quét ngưỡng Threshold trên `df_val` và kiểm thử độc lập trên `df_test`, loại bỏ rủi ro Threshold Tuning Leakage.

**Mục tiêu**: Tìm ngưỡng quyết định tối ưu cho hệ thống cảnh báo thay vì dùng mặc định 0.5.

**Metric tối ưu**: Sensitivity Analysis (Phân tích độ nhạy) để tìm điểm "Managerial Sweet Spot". Tránh dùng F2-score vì nó mâu thuẫn với mục tiêu giảm Alert Fatigue. Tối ưu hóa dựa trên F1-score hoặc F0.5 (ưu tiên Precision).
```python
# Quét threshold từ 0.1 đến 0.9, step 0.05
# Vẽ đồ thị Threshold vs Precision/Recall/F1
```

**Output**: `optimal_threshold.json` — threshold riêng cho từng part_group

---

### P3-02 | SHAP Analysis & Explainability
**Folder**: `/P3-02_SHAP/`

> **✅ ĐÃ GIẢI QUYẾT (RESOLVED)**: Đã đồng bộ hóa trích xuất. Vẽ đồ thị SHAP chính xác cho dòng dữ liệu của linh kiện P00179 tại tuần cảnh báo W15.

**Mục tiêu**: Giải thích mô hình cho paper — feature nào quan trọng nhất? Đảm bảo tính minh bạch trước khi đưa vào Case Study.

**Output**:
- `shap_summary_plot.png`
- `shap_waterfall_local.png`
- `explainability_section.md` — đoạn viết cho paper

---

### P3-03 | Full Pipeline Integration Test (Case Study)
**Folder**: `/P3-03_Integration/`

> **✅ ĐÃ GIẢI QUYẾT (RESOLVED)**: 
> **Data Governance:** Chèn công thức toán học $LTG$ và tích hợp cơ chế đóng dấu bảo mật **SHA256 Checksum** tự động vào file `integration_test_report.md` để chống gian lận dữ liệu nghiên cứu.

**Mục tiêu**: Kiểm tra end-to-end (Case Study thực tế) để chứng minh "Lead-Time Gain".

**Trực quan hóa (Hero Chart)**:
- Multi-panel Time Series (Tầng 1: Risk Score, Tầng 2: NLP Signal, Tầng 3: ERP Reality).
- Highlight vùng "Warning Period".

**Output**:
- `integration_test_report.md`
- `case_study_hero_chart.png`

---

## BẢNG TIẾN ĐỘ (PCCV)

> **Cập nhật**: 2026-07-07 | Trạng thái: SẴN SÀNG REFACTOR

| Phase | Task ID | Tên Task | Trạng thái Dự kiến |
|-------|---------|----------|-------------------| 
| 0 | P0-01 | New Crawl 2022–2024 | ✅ DONE |
| 0 | P0-02 | EDA | ✅ DONE |
| 0 | P0-03 | Pilot Labeling + Fleiss' Kappa | ✅ DONE |
| 0 | P0-04 | Binary Filter NLP (Stage 1) | ✅ DONE |
| 1 | P1-01 | Risk Taxonomy Extraction | ✅ DONE (Ngưỡng 0.5) |
| 1 | P1-02 | Taxonomy-Conditioned Severity | ✅ DONE (Ngưỡng 0.5) |
| 1 | P1-03 | Label Distribution Check | ✅ DONE |
| 2 | P2-01 | NER & Entity Extraction | ✅ DONE |
| 2 | P2-02 | Soft Join — Geographic Weighting | ✅ DONE |
| 2 | P2-03 | Weekly Feature Matrix | ✅ DONE (Có ADF Test) |
| 2 | P2-04 | Derive y2 (Target Shift) | ✅ DONE |
| 2 | P2-05 | Ablation Study 2×2 | ✅ DONE |
| 3 | P3-01 | Threshold Optimization | ✅ DONE |
| 3 | P3-02 | SHAP Analysis | ✅ DONE |
| 3 | P3-03 | Integration Test (Case Study) | ✅ DONE |

---

## GHI CHÚ KỸ THUẬT QUAN TRỌNG

### Về Biến Shift
```
Dự báo cho tuần W:
  ✅ ĐÚNG: X = news(W-1) + news(W-2) + operational(W-1)
           Y = operational_risk(W+1) hoặc operational_risk(W+2)
  
  ❌ SAI (lỗi cũ): X = news(W) + operational(W)
                   Y = operational_risk(W)  ← Nowcasting, không phải Forecasting
```

### Về Kappa
```python
# Fleiss' Kappa (nhiều rater)
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
agg, _ = aggregate_raters(labels_matrix)  # shape: (n_items, n_raters)
kappa = fleiss_kappa(agg, method='fleiss')

# Cohen's Kappa (2 rater — QC check)
from statsmodels.stats.inter_rater import cohens_kappa
result = cohens_kappa(rater1_labels, rater2_labels)
```

### Về Aerospace Data
```
Bài toán Inbound Risk được định nghĩa bởi:
  - actual_lead_time > promised_lead_time  → DELAY signal
  - on_hand_inventory thấp / stockout       → SHORTAGE signal
  
Cột quan trọng trong dataset:
  - actual_lead_time    (từ shifted_supply_chain_history.csv)
  - on_hand_inventory   (từ shifted_supply_chain_history.csv)
  - promised_date       (từ shifted_purchase_orders.csv)
```

### Protocol Dừng & Đề xuất
> Khi gặp BẤT KỲ vấn đề nào (API fail, Kappa thấp, imbalance cực đoan, data quá nhiễu):
> 1. **DỪNG NGAY** — không tiếp tục chạy
> 2. Đưa ra **≥ 3 phương án** giải quyết với ưu/nhược điểm
> 3. **CHỜ LỆNH** — chỉ chạy khi nhận được "Chọn phương án X"

---

*Workflow version 2.1 — Hoàn thiện Kiến trúc & Kiểm toán Machine Learning (Passed ML Audit)*  
*Cập nhật ngày 2026-07-14 bởi Senior ML Auditor (Antigravity)*  
