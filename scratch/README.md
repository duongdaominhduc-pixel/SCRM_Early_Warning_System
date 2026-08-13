# Thư mục Scratch (Mã nguồn Thử nghiệm)

Thư mục này được sử dụng như một **"Sandbox"** (môi trường nháp/thử nghiệm) trong quá trình phát triển dự án EWS-SCRM.

## Mục đích của thư mục:
- Lưu trữ các kịch bản (scripts) chạy độc lập để kiểm chứng nhanh các giả thuyết khoa học (ví dụ: test thử một thuật toán mới, vẽ biểu đồ nháp, kiểm tra dữ liệu đầu ra của một hàm cụ thể).
- Các đoạn mã trong thư mục này **KHÔNG** tham gia trực tiếp vào luồng thực thi chính của hệ thống (Cascading AI Pipeline) và không ảnh hưởng đến kết quả cuối cùng.
- Luồng thực thi chính thức và hoàn chỉnh của hệ thống đã được đóng gói chuẩn mực trong 3 file `run_phase...pipeline.py` ở thư mục gốc.

*💡 Lưu ý dành cho Giảng viên hướng dẫn / Reviewer: Thầy/Cô có thể bỏ qua thư mục này trong quá trình nghiệm thu mã nguồn lõi của dự án.*
