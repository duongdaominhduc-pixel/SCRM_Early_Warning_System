# Hệ thống Cảnh báo Sớm Rủi ro Chuỗi Cung ứng Thượng nguồn (EWS - SCRM)

Dự án khoa học: **EWS-SCRM (Early Warning System for Supply Chain Risk Management)** được thiết kế nhằm dự báo sớm nguy cơ đứt gãy nguồn cung và thiếu hụt tồn kho thượng nguồn (Inbound). Hệ thống tận dụng sức mạnh của **Cascading AI Architecture** để hợp nhất dữ liệu thời sự toàn cầu (Unstructured NLP News) và số liệu vận hành chuỗi cung ứng nội bộ (Structured ERP/Logistics Data).

---

## 📌 Hướng dẫn dành cho Giảng viên Hướng dẫn (Supervisor Guide)

Kính gửi Thầy/Cô hướng dẫn,

Để thuận tiện cho việc nghiệm thu và đánh giá luận điểm khoa học của đề tài, em xin tóm tắt cấu trúc và cách tiếp cận tài liệu như sau:

### 1. Báo cáo Khoa học Chính thức (Bản Draft Article)
Toàn bộ phương pháp luận, kết quả thực nghiệm, tính toán Lead-Time Gain, và các kiểm định thống kê đều được tổng hợp chi tiết trong bản thảo bài báo chuẩn Q1:
👉 **File đọc chính:** [`0. project documents/1. Final Articles/SCRM_EWS_draft_article_v3.md`](0.%20project%20documents/1.%20Final%20Articles/SCRM_EWS_draft_article_v3.md)
*(Đây là bản hoàn thiện cuối cùng, đã cập nhật đầy đủ số liệu từ quá trình sửa lỗi Data Leakage, tinh chỉnh Walk-forward Cross Validation và hoàn thiện kịch bản Stress Test).*

### 2. Những cập nhật Phương pháp luận Quan trọng nhất (Methodological Highlights)
Trong quá trình Audit và Refactor lại mô hình, nhóm đã áp dụng các tiêu chuẩn khắt khe nhất để bảo vệ tính toàn vẹn khoa học:
*   **Chống rò rỉ dữ liệu (No Data Leakage):** Thay vì Random Split, toàn bộ quá trình Validation (Phase 2 & Phase 3) đều sử dụng **5-Fold Walk-forward TimeSeriesSplit**. Quá trình tính toán hệ số cân bằng class (`scale_pos_weight`) được thực hiện nghiêm ngặt bên trong từng fold (In-fold calculation) thay vì tính trên toàn cục.
*   **Đánh giá Công bằng (Fair Ablation & Stress Test):** Tại Table 4 (Ablation) và Table 6 (Stress Test), ngưỡng ra quyết định (decision threshold) được khóa chặt ở mức mặc định **τ=0.50** để đánh giá "sức mạnh nguyên bản" của kiến trúc thuật toán, tránh việc "ăn gian" bằng cách tune threshold.
*   **Thực tiễn Vận hành (Operational Utility):** Tại Phase 3 (Lead-Time Gain), kỹ thuật **Threshold Optimization** mới được kích hoạt. Ngưỡng cảnh báo được tinh chỉnh riêng cho từng nhóm linh kiện (Per-family optimal thresholds) nhằm tối ưu hóa F0.5-score (đề cao Precision), giải quyết triệt để bài toán Alert Fatigue (báo động giả) cho doanh nghiệp.

### 3. Hướng dẫn Tái hiện Kết quả (Reproducibility)
Toàn bộ mã nguồn (Source Code) đã được đóng gói thành các module chạy tuần tự (Pipelines) theo đúng kiến trúc 4 giai đoạn. Thầy/Cô có thể kiểm tra logic code hoặc chạy thử thông qua 3 script chính tại thư mục gốc:
*   `run_phase1_pipeline.py`: Chạy Phase 0 & 1 (Thu thập, Zero-shot Classification, Severity Specialist).
*   `run_phase2_pipeline.py`: Chạy Phase 2 (NER, Geo Join, Feature Engineering, Walk-forward CV Ablation/Stress Test).
*   `run_phase3_pipeline.py`: Chạy Phase 3 (Train mô hình cuối, Global/Local SHAP, Threshold Optimization, Integration Case Study).

---

## 📂 Tổng quan Cấu trúc Thư mục Dự án

```text
BBKH/
├── 0. internal data/                 # Dữ liệu vận hành nội bộ (ERP/Logistics)
├── 0. news data/                     # Dữ liệu tin tức chuỗi cung ứng (GDELT & NewsAPI)
├── 0. project documents/             # Các tài liệu luận văn, bài báo (Draft Article v3)
├── P0-03_Pilot_Labeling/             # [Phase 0] Gán nhãn thử nghiệm & kiểm định Fleiss' Kappa
├── P0-04_Binary_Filter/              # [Phase 0] Huấn luyện bộ lọc Gatekeeper (DistilBERT)
├── P1-01_Risk_Taxonomy/              # [Phase 1] Trích xuất Taxonomy (Zero-shot BART)
├── P1-02_Severity_Specialist/        # [Phase 1] Đánh giá mức độ nghiêm trọng rủi ro
├── P1-03_Label_Distribution/         # [Phase 1] Báo cáo phân bổ & SHA256 Data Integrity
├── P2-01_NLP_NER/                    # [Phase 2] Nhận diện thực thể vị trí (NER)
├── P2-02_Geo_Join/                   # [Phase 2] Soft Join & Geographic Weighting
├── P2-03_Feature_Matrix/             # [Phase 2] Kiểm định ADF & Sinh biến Delta (Momentum)
├── P2-04_Derive_y2/                  # [Phase 2] Khởi tạo biến mục tiêu (Target Shifting)
├── P2-05_ML_Ablation/                # [Phase 2] Điểm chuẩn Mô hình & Stress Test (W-2)
├── P3-01_Threshold/                  # [Phase 3] Tối ưu hóa ngưỡng cảnh báo Per-Family
├── P3-02_SHAP/                       # [Phase 3] Diễn giải mô hình (Global/Local SHAP XAI)
├── P3-03_Integration/                # [Phase 3] Phân tích Case Study & Lead-time Gain
├── 99. Archives/                     # Tài liệu cũ, phiên bản báo cáo trước (v2)
├── scratch/                          # Các script nháp, test logic tạm thời
├── run_phase1_pipeline.py            # Script thực thi Phase 1
├── run_phase2_pipeline.py            # Script thực thi Phase 2
└── run_phase3_pipeline.py            # Script thực thi Phase 3
```

---

## 🏆 Case Study: Khả năng Cảnh báo Sớm (Lead-Time Gain)

Mô hình đã được thử nghiệm thực tế (Integration Test) trên mã linh kiện **P00179**. Bằng việc kết hợp tin tức rủi ro địa chính trị và tín hiệu cảnh báo từ chuỗi cung ứng, hệ thống EWS đã đưa ra cảnh báo sớm trước 3 tuần so với sự cố đứt gãy thực tế xảy ra trong hệ thống ERP. 

Chi tiết diễn giải và biểu đồ Hero Chart xem tại: [`P3-03_Integration/integration_test_report.md`](P3-03_Integration/integration_test_report.md)

> **Data Governance:** Toàn bộ dữ liệu đầu ra trung gian và cuối cùng đều được bảo vệ bằng mã băm SHA256 (Checksum) nhằm chống giả mạo dữ liệu khoa học.

---
*Dự án hoàn thiện và sẵn sàng để nghiệm thu khoa học.*
