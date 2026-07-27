# Schematic Outlines cho 2 Sơ đồ Trọng tâm (SOTA V2.0)

File này định nghĩa cấu trúc (Nodes) và luồng (Edges) để vẽ 2 sơ đồ quan trọng nhất trong bài báo. Đã được chuẩn hóa lại dựa trên hệ thống thực tế V2.0 và **đảm bảo khớp 100% thuật ngữ với nội dung bài báo (Phase 0-3, Geographic Weighting, Cascading Stage)**.

---

## 1. Sơ đồ Mô hình Phương pháp Nghiên cứu (Research Methodology Framework)

**Mục tiêu:** Trực quan hóa hành trình từ dữ liệu thô (Raw Data) đến Tri thức Hành động (Actionable Intelligence).
**Kiểu vẽ khuyến nghị:** Flowchart dọc (Top-Down) hoặc Block Diagram.

> **⚠️ YÊU CẦU CẬP NHẬT:** Đổi tên các khối (Phase) để khớp hoàn toàn với mục 3. Methodology trong bài text (bắt đầu từ Phase 0). Tách Data Collection ra khỏi các Phase chính.

### Các Khối (Nodes) & Luồng (Edges) chính:

**Mục Chuẩn bị (Data Collection - Tương ứng mục 3.2):**
- Node A: Nguồn Dữ liệu Văn bản (GDELT Project & NewsAPI, 2022-2024, ~7,200 bài).
- Node B: Nguồn Dữ liệu Vận hành (Aerospace Inbound Logistics, Tồn kho & Lead-time).
- *Mũi tên:* Hướng xuống Khối 1.

**Khối 1: Phase 0 - Sensing Layer (Tương ứng mục 3.3)**
- Node C: Binary Filter (Lọc rủi ro bằng DistilBERT).
- Node D: *[QUALITY GATE 1]* Fleiss' Kappa = 0.785 (đóng khung viền đứt nét, màu đỏ).

**Khối 2: Phase 1 - Sense-making Layer (Tương ứng mục 3.4)**
- Node E: Taxonomy Extraction (Gán nhãn Sự kiện Đa nhãn).
- Node F: Severity Specialist (Đánh giá mức độ nghiêm trọng bằng Context Shells).
- Node G: Đồng bộ hóa thời gian (Time-Series Alignment) – ISO Week format.

**Khối 3: Phase 2 - Feature Fusion and Machine Learning (Tương ứng mục 3.5)**
- Node H: Kiểm định dừng & Sinh biến động lượng (ADF Stationarity Test & Delta Momentum).
- Node I: Trích xuất Đặc trưng (Geographic Weighting).
- Node J: Walk-forward Validation (5 Folds, Chronological Split).
- Node K: Ablation Study (Tier 1 Baseline, Tier 2 Baseline, Tier 3 Hybrid).

**Khối 4: Phase 3 - Evaluation and Data Governance (Tương ứng mục 3.6)**
- Node L: Metrics Cốt lõi (PR-AUC, F1-Score, Brier Score).
- Node M: Trực quan hóa & Giải trình (SHAP Value).
- Node N: *[QUALITY GATE 2]* Lead-Time Gain (LTG) Analysis (Đánh giá hiệu quả kinh tế).
- *Luồng phản hồi:* Mũi tên đứt nét (Feedback Loop) quay về Phase 1 (cho thấy tính Proactive Resilience).

---

## 2. Sơ đồ Kiến trúc Hệ thống Đề xuất (Proposed System Architecture)

**Mục tiêu:** Hiển thị cấu trúc nội tại của mô hình AI 3 Tầng (Cascading AI).
**Kiểu vẽ khuyến nghị:** 3 Tầng xếp chồng (Stage).

> **⚠️ YÊU CẦU CẬP NHẬT:** 
> 1. Đổi chữ "Layer" thành "Stage" để đồng bộ với từ khóa "four-stage Cascading AI architecture" ở đoạn 3.1.
> 2. Bổ sung cho đủ 4 trọng số Geographic Weighting (Exact, Country, Region, Global).

### Các Khối (Nodes) & Luồng (Edges) chính:

**Stage 1: NLP Sensing & Taxonomy-Conditioned AI**
- Node L1.1: Đầu vào văn bản (News Text).
- Node L1.2: Binary Filter (Lọc rủi ro).
- Node L1.3: Universal Information Extraction (UIE) - Gán nhãn Sự kiện Đa nhãn (Taxonomy).
- Node L1.4: Context Shells Injection (Ví dụ: `[PORT_CONGESTION] Text...`).
- Node L1.5: Đánh giá mức độ nghiêm trọng (Severity Specialist).
- *Output của Stage 1:* `at_risk_count`, `high_severity_count`, `dominant_event_type`.

**Stage 2: Operational Mapping & Feature Generation**
- Node L2.1: Geographic Weighting (Tính toán rủi ro không gian: **Exact=1.0, Country=0.6, Region=0.3, Global=0.1**).
- Node L2.2: Trích xuất Biến Vận hành (Inbound Metrics).
- Node L2.3: Delta Features Generation (Sinh biến động lượng: `delta_avg_actual_lead_time`).
- *Output của Stage 2:* `weighted_geo_risk_w1`, `avg_actual_lead_time_w1`, v.v.

**Stage 3: Intelligence Fusion & Data Integrity**
- Node L3.1: Feature Matrix X (kết hợp Output L1 và L2 tại thời điểm W-1 và W-2).
- Node L3.2: *[INTEGRITY LOCK]* Biểu tượng Ổ khóa đóng dấu `SHA256 Checksum`.
- Node L3.3: Mô hình XGBoost (Cost-Sensitive Learning thông qua `scale_pos_weight`).
- Node L3.4: Target Shift Mechanism (Dự báo Y tại W+1, W+2).
- *Output Cuối Cùng:* Cảnh báo Sớm (Early Warning Alert Probability) & SHAP Explanations.
