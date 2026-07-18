# Schematic Outlines cho 2 Sơ đồ Trọng tâm (SOTA V2.0)

File này định nghĩa cấu trúc (Nodes) và luồng (Edges) để vẽ 2 sơ đồ quan trọng nhất trong bài báo. Đã được chuẩn hóa lại dựa trên hệ thống thực tế V2.0.

---

## 1. Sơ đồ Mô hình Phương pháp Nghiên cứu (Research Methodology Framework)

**Mục tiêu:** Trực quan hóa hành trình từ dữ liệu thô (Raw Data) đến Tri thức Hành động (Actionable Intelligence).
**Kiểu vẽ khuyến nghị:** Flowchart dọc (Top-Down) hoặc Block Diagram.

### Các Khối (Nodes) & Luồng (Edges) chính:

**Khối 1: Giai đoạn Thu thập (Data Acquisition)**
- Node A: Nguồn Dữ liệu Văn bản (GDELT Project & NewsAPI, 2022-2024, ~7,200 bài).
- Node B: Nguồn Dữ liệu Vận hành (Aerospace Inbound Logistics, Tồn kho & Lead-time).
- *Mũi tên:* Hướng xuống Khối 2.

**Khối 2: Giai đoạn Tiền xử lý & Căn chỉnh (Preprocessing & Alignment)**
- Node C: Xử lý NLP Cascading 4 bước (Manual Labeling -> Binary Filter -> Taxonomy Extraction -> Severity Specialist).
- Node D: *[QUALITY GATE 1]* Fleiss' Kappa & Cohen's Kappa >= 0.70 (đóng khung viền đứt nét, màu đỏ).
- Node E: Đồng bộ hóa thời gian (Time-Series Alignment) – ISO Week format.

**Khối 3: Giai đoạn Phát triển (Model Development)**
- Node F: Trích xuất Đặc trưng (Feature Engineering - Delta Features, Geographic Weighting).
- Node G: Cơ chế đánh giá Walk-forward Validation (5 Folds, Tách rời thời gian).
- Node H: Ablation Study (Tier 1 vs Tier 2 vs Tier 3 Hybrid).

**Khối 4: Giai đoạn Đánh giá (Evaluation & Validation)**
- Node I: Metrics Cốt lõi (PR-AUC, F1-Score, Brier Score).
- Node J: Trực quan hóa & Giải trình (SHAP Value).
- Node K: *[QUALITY GATE 2]* Lead-Time Gain (LTG) Analysis (Đánh giá hiệu quả kinh tế).

---

## 2. Sơ đồ Kiến trúc Hệ thống Đề xuất (Proposed System Architecture)

**Mục tiêu:** Hiển thị cấu trúc nội tại của mô hình AI 3 Lớp (Cascading AI).
**Kiểu vẽ khuyến nghị:** 3 Lớp ngang (Left-to-Right) hoặc 3 Tầng xếp chồng (Layered).

### Các Khối (Nodes) & Luồng (Edges) chính:

**Layer 1: Nhận thức Ngôn ngữ (NLP Sensing & Taxonomy-Conditioned AI)**
- Node L1.1: Đầu vào văn bản (News Text).
- Node L1.2: Binary Filter (Lọc rủi ro).
- Node L1.3: Universal Information Extraction (UIE) - Gán nhãn Sự kiện Đa nhãn (Taxonomy).
- Node L1.4: Context Shells Injection (Ví dụ: `[PORT_CONGESTION] Text...`).
- Node L1.5: Đánh giá mức độ nghiêm trọng (Severity Specialist).
- *Output của Layer 1:* `at_risk_count`, `high_severity_count`, `dominant_event_type`.

**Layer 2: Nội suy Vận hành (Operational Mapping & Feature Generation)**
- Node L2.1: Geographic Weighting (Tính toán rủi ro không gian: Match=1.0, Region=0.6, Global=0.1).
- Node L2.2: Trích xuất Biến Vận hành (Inbound Metrics).
- Node L2.3: Delta Features Generation (Sinh biến động lượng: `delta_avg_actual_lead_time`).
- *Output của Layer 2:* `weighted_geo_risk_w1`, `avg_actual_lead_time_w1`, v.v.

**Layer 3: Trí tuệ Tổng hợp & Đóng băng Dữ liệu (Intelligence Fusion & ML)**
- Node L3.1: Feature Matrix X (kết hợp Output L1 và L2 tại thời điểm W-1 và W-2).
- Node L3.2: *[INTEGRITY LOCK]* Biểu tượng Ổ khóa đóng dấu `SHA256 Checksum`.
- Node L3.3: Mô hình XGBoost (Cost-Sensitive Learning thông qua `scale_pos_weight`).
- Node L3.4: Target Shift Mechanism (Dự báo Y tại W+1, W+2).
- *Output Cuối Cùng:* Cảnh báo Sớm (Early Warning Alert Probability) & SHAP Explanations.
