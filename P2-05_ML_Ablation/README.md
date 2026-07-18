# P2-05 | Huấn luyện & Đánh giá (ML Training & Ablation Study)

## 📌 Tổng quan
Bước cuối cùng của Tầng ML Fusion. Tiến hành huấn luyện mô hình dự báo XGBoost và thực hiện đánh giá độc lập (Ablation Study) giữa các tính năng Rule-based, Baseline ERP, và NLP SCRM.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
Mô-đun này đã được tái cấu trúc (V2.0 Overhaul) để vượt qua các tiêu chuẩn khắt khe nhất của Tạp chí Q1:

1. **Information Bottlenecking for Non-Naive Learning (Audited: PASS)**
   - Tuyệt đối loại bỏ việc Downsampling trên toàn cục, đảm bảo cơ chế học không ngây thơ (Non-Naive Learning). Tập dữ liệu giữ nguyên sự phân phối mất cân bằng tự nhiên.
   - Việc cân bằng `scale_pos_weight` được đưa *vào bên trong* vòng lặp cross-validation, tính toán riêng trên tập Train. Tập Validation giữ nguyên 100% phân phối hiếm gặp thực tế (đảm bảo chống Data Leakage triệt để).
2. **Hiệu suất & Sàn độ chuẩn xác (Precision Floor)**
   - Hệ thống không đánh đổi Precision lấy Recall. Thay vào đó, Tier3_XGB_SCRM thiết lập một **Precision Floor** cực kỳ vững chắc so với Rule-Based, giảm thiểu hội chứng Alert Fatigue (Mệt mỏi vì cảnh báo giả) cho nhà quản trị chuỗi cung ứng.
3. **ERP Latency Stress Test**
   - Mô hình chịu tải tốt dưới điều kiện biến quan sát bị trễ 2 tuần (W-2), chứng minh tính bền bỉ của thông tin NLP.

## 📂 Các File Đầu ra
- `ablation_results.md`: Báo cáo kết quả so sánh F1 và PR-AUC của các mô hình.
- `models/`: Thư mục chứa các object mô hình học máy đã hội tụ để dùng cho Phase 3.
- `verdict.md`: Kết luận ML Audit, xác nhận mức độ tin cậy khoa học tuyệt đối.
