# Hệ thống Cảnh báo Sớm Rủi ro Chuỗi Cung ứng Thượng nguồn (EWS - SCRM)

Hệ thống EWS-SCRM (Early Warning System for Supply Chain Risk Management) được thiết kế nhằm dự báo sớm nguy cơ đứt gãy nguồn cung và thiếu hụt tồn kho thượng nguồn (Inbound) của doanh nghiệp thông qua việc kết hợp dữ liệu tin tức toàn cầu (NLP Signal) với dữ liệu vận hành chuỗi cung ứng nội bộ (Operational Data).

---

## 📂 Tổng quan Cấu trúc Thư mục Dự án

Dưới đây là sơ đồ và mô tả tổng quan về các file và thư mục hiện có trong dự án `BBKH`:

```text
BBKH/
├── 0. internal data/                 # Dữ liệu vận hành nội bộ (ERP/Logistics)
├── 0. news data/                     # Dữ liệu tin tức chuỗi cung ứng thu thập từ GDELT & NewsAPI
├── 0. project documents/             # Tài liệu định hướng và thuyết minh đề tài khoa học
├── P0-03_Pilot_Labeling/             # [Phase 0] Quy trình gán nhãn thử nghiệm & kiểm định Fleiss' Kappa
├── P0-04_Binary_Filter/              # [Phase 0] Huấn luyện bộ lọc nhị phân (Gatekeeper) bằng DistilBERT
├── P1-01_Risk_Taxonomy/              # [Phase 1] Trích xuất Taxonomy (Zero-shot BART)
├── P1-02_Severity_Specialist/        # [Phase 1] Đánh giá mức độ nghiêm trọng (Context Shells)
├── P1-03_Label_Distribution/         # [Phase 1] Báo cáo thống kê & Data Integrity Gate (SHA256)
├── P2-01_NLP_NER/                    # [Phase 2] Nhận diện thực thể vị trí địa lý (NER)
├── P2-02_Geo_Join/                   # [Phase 2] Tính toán Soft Join & Geographic Weighting
├── P2-03_Feature_Matrix/             # [Phase 2] Kiểm định ADF & Sinh biến Delta
├── P2-04_Derive_y2/                  # [Phase 2] Khởi tạo biến mục tiêu (Target Shifting)
├── P2-05_ML_Ablation/                # [Phase 2] Ma trận đánh giá 3 tầng (Dual-path Validation)
├── P3-01_Threshold/                  # [Phase 3] Tối ưu hóa ngưỡng cảnh báo (Chronological Split)
├── P3-02_SHAP/                       # [Phase 3] Diễn giải mô hình (SHAP XAI Feedback Loop)
├── P3-03_Integration/                # [Phase 3] Báo cáo Case Study & Lead-time Gain
├── run_phase1_pipeline.py            # Script thực thi toàn bộ Phase 1
├── run_phase2_pipeline.py            # Script thực thi toàn bộ Phase 2
├── run_phase3_pipeline.py            # Script thực thi toàn bộ Phase 3
├── MODERN_SCRM_WORKFLOW.md           # Tài liệu workflow chuẩn hóa toàn bộ dự án
└── 99. Archives/                     # Thư mục lưu trữ code cũ, tài liệu nháp
```

---

## 🏆 Kết quả Đã đạt được - Cấu trúc 4 Giai đoạn (4-Phase Architecture)

Hệ thống đã trải qua quá trình Kiểm toán Máy học (ML Audit) theo chuẩn Gold Standard và thực thi thành công toàn bộ kiến trúc 4 giai đoạn, đạt chuẩn công bố trên các tạp chí Q1 (DSS, IJPE, IJPR).

### 1. Phase 0: Sensing (Tầng Cảm nhận rủi ro & Gatekeeper)
*   **Data Collection:** Thu thập thành công **8,728 bài báo sạch** chuyên ngành logistics và chuỗi cung ứng giai đoạn **2022–2024** qua dự án GDELT và NewsAPI, sau đó xử lý Deduplication bằng Cosine Similarity.
*   **Huấn luyện Gatekeeper (P0-04):** Huấn luyện mô hình `distilbert-base-uncased` phân loại nhị phân. Đạt hệ số hiệu chuẩn **Expected Calibration Error (ECE) = 0.0849** nhờ Temperature Scaling. 
*   **Quality Gate:** Lọc bỏ 34% dữ liệu nhiễu, ưu tiên Recall (đạt 0.9503). Hệ số **Cohen's Kappa = 0.635** tại ngưỡng tự nhiên, chứng minh AI đã học vững logic gán nhãn của chuyên gia, đảm bảo chất lượng dữ liệu.

### 2. Phase 1: Structured Disruption Intelligence Extraction (Tầng Khai thác Trí tuệ Phá vỡ)
*   **Taxonomy Extraction (P1-01):** Khắc phục lỗi "ép nhãn" bằng kiến trúc Zero-shot BART với Sigmoid Multi-label, tự động phân loại rủi ro (Port Congestion, Labor Strike...).
*   **Severity Specialist (P1-02):** Sử dụng kỹ thuật **Context Shells** và Focal Loss để đánh giá mức độ nghiêm trọng (High Risk/Medium Risk), loại bỏ bẫy Double Regularization Collapse.
*   **Data Integrity Gate:** Tự động tạo mã băm **SHA256 Checksum** chốt chặn cuối Phase 1 để chứng minh tính toàn vẹn dữ liệu (Data Integrity) trước khi bàn giao sang Phase 2.
*   *Lưu ý (Future Work):* Việc hạ ngưỡng Cascading Guardrail xuống 0.35 đòi hỏi tài nguyên tính toán GPU cực lớn, sẽ được tối ưu ở các nghiên cứu tiếp theo.

### 3. Phase 2: Heterogeneous Modality Fusion & ML Ablation (Tầng Hợp nhất Dị thể)
*   **Spatial Risk Sensitivity Calibration (P2-02):** Sử dụng thuật toán Soft Join (Time × Geo × Category) kết hợp Hàm trọng số địa lý (Geographic Weighting) để hợp nhất tín hiệu NLP với dữ liệu ERP, mô phỏng chính xác "Hiệu ứng gợn sóng" (Ripple Effect).
*   **ADF Stationarity Test (P2-03):** Tự động kiểm định Augmented Dickey-Fuller (ADF). Nhận diện tính dừng và sinh biến Delta Momentum, giúp mô hình ML không bị đánh lừa bởi dữ liệu xu hướng giả mạo.
*   **Dual-path Ablation Study (P2-05):** Cô lập hoàn toàn luồng dữ liệu thông qua 2 quy trình Validation song song (K-Fold TimeSeriesSplit) để tránh rò rỉ dữ liệu (Data Leakage) và Look-ahead bias. Kết quả chứng minh Mô hình Tier 3 (SCRM ML) sử dụng dữ liệu NLP vượt trội hơn hẳn Tier 2 (Baseline ML - Operational Only).

### 4. Phase 3: Evaluation, XAI & Decision Linkage (Tầng Đánh giá và Giải trình)
*   **PR-AUC & Metric Evaluation:** Đánh giá hiệu suất toàn diện bằng Precision, Minority F1-score và PR-AUC trên bài toán mất cân bằng nghiêm trọng (<5% thiểu số).
*   **XAI Feedback Loop (P3-02):** Ứng dụng thuật toán SHAP (Summary & Waterfall) để giải thích sự đóng góp của cả biến NLP và ERP vào cảnh báo rủi ro cuối cùng, cung cấp tính giải trình xuyên suốt (Accountability).
*   **Decision Linkage (P3-03):** Tính toán **Lead-Time Gain** thông qua cơ chế Time-to-Survive (Sức chịu đựng tồn kho) và Time-to-Recover (Thời gian phục hồi), cung cấp giá trị quản trị thực tiễn cho doanh nghiệp.

---

## 🏆 Case Study: Hero Chart (Bằng chứng Thực nghiệm)

Hệ thống đã chọn linh kiện **P00179** để thực hiện phân tích Case Study (Integration Test). Dưới đây là biểu đồ chứng minh thời gian Cảnh báo sớm (Lead-Time Gain):

![Hero Chart](file:///d:/3.%20Research%20&%20Contest/BBKH_PAPA/BBKH/m%E1%BB%9Bi%2013.7/BBKH-20260712T234314Z-2-001/BBKH/P3-03_Integration/case_study_hero_chart.png)

> **Data Governance:** Toàn bộ báo cáo Case Study chi tiết đều được đóng dấu mã băm SHA256 Checksum chống gian lận dữ liệu khoa học, lưu trữ tại `P3-03_Integration/integration_test_report.md`.
