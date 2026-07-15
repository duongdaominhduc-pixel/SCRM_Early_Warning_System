# P2-01 | Trích xuất Thực thể Có tên (NER)

## 📌 Tổng quan
Bước đầu tiên của Tầng ML Fusion. Chuyển đổi các bài báo nhãn 1 thành dữ liệu có cấu trúc bằng cách trích xuất Thực thể (Tổ chức, Quốc gia) để làm bản lề (join key) với dữ liệu chuỗi cung ứng.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Mô hình mặc định: Sử dụng `spaCy` (en_core_web_trf) để lấy ORG, GPE, DATE.
- **Audit Status:** [PASS]. Đã tạo thành công file `news_with_ner_features.parquet` chứa các tính năng thực thể.
