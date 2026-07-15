# Phase 0 - Bước 04: Binary Filter (Gatekeeper)

## 📌 Mục tiêu
Giai đoạn này (Phase 0) đóng vai trò là tầng **Sensing (Cảm nhận)** trong hệ thống Cảnh báo Sớm (Early Warning System - EWS) cho Chuỗi cung ứng (SCRM). Mục tiêu là xây dựng một "Gatekeeper" bằng mô hình phân loại nhị phân để lọc các tin tức phi cấu trúc.
- **Nhãn 0 (NO_RISK):** Tin tức bình thường, không chứa rủi ro.
- **Nhãn 1 (AT_RISK):** Tin tức chứa tín hiệu rủi ro (đứt gãy, thiếu hụt, đình công, v.v.).

Nguyên tắc tối thượng của tầng Sensing là **không bỏ sót tín hiệu rủi ro (ưu tiên tối đa Recall)**, nhưng vẫn phải duy trì một mức Precision tối thiểu để tránh làm nhiễu dữ liệu đầu vào của các Phase sau (Cascading Error mitigation).

## 📁 Dữ liệu
- **Dữ liệu huấn luyện:** `output/manual_combined_2309.csv` (2,309 mẫu gán nhãn thủ công).
- **Dữ liệu Inference:** `news_2022_2024_clean_2.json` (Corpus toàn bộ 8,728 bài báo giai đoạn 2022-2024).
- **Dữ liệu đầu ra:** `output/at_risk_corpus.csv` (Các bài báo nhãn 1 đã qua bộ lọc).

## 🧠 Kết quả Thực nghiệm & Phương pháp (Audited)
- **Mô hình nền tảng:** `distilbert-base-uncased`.
- **Hàm Loss (Loss Function):** Sử dụng `CrossEntropyLoss` kết hợp với **Class Weights** và **Label Smoothing (0.1)**. Kiến trúc này đã **tránh được bẫy Sụp đổ dải đầu ra (Double Regularization Collapse)** khi không lạm dụng Focal Loss.
- **Training Strategy:**
  - Optimizer: Adam (Learning Rate: 2e-5, warmup_ratio=0.2).
  - Lựa chọn checkpoint tốt nhất dựa trên **F1-score**.
- **Kết quả Phân loại (Discrimination):** 
  - Tại ngưỡng quyết định vận hành (Threshold = `0.1756`), mô hình đạt **Recall = 0.9503** (thỏa mãn tiêu chuẩn >0.95 của Q1 Journals) và **Precision = 0.5426** (xử lý triệt để hiện tượng cascading error).
- **Hiệu chuẩn xác suất (Algorithmic Accountability):** 
  - Mức Expected Calibration Error (ECE) đạt **0.0849** (Hoàn hảo < 0.09).
- **Độ tin cậy (Human-AI Agreement):**
  - Chỉ số Cohen's Kappa được xác minh đạt **0.635** tại ngưỡng tự nhiên, minh chứng sự đồng thuận đáng kể (Substantial Agreement) giữa máy và chuyên gia con người.

## 📜 Các file và Script chính
- `notebooks/P0_04_DistilBERT_Colab.ipynb`: Notebook huấn luyện mô hình.
- `P0_04_Execution_Report.md`: Báo cáo chi tiết kết quả thực nghiệm.
- `verify_cohens_kappa.py`: Script hậu kiểm tính toàn vẹn của chỉ số Cohen's Kappa.
- `verdict.md`: Kết luận ML Audit khẳng định chất lượng xuất bản khoa học.
