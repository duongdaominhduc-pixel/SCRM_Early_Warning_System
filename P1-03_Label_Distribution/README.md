# P1-03 | Phân phối Nhãn & Chốt chặn Chống Học Vẹt (Anti-Overfitting Gate)

## 📌 Tổng quan
**P1-03** là chốt kiểm định chất lượng cuối cùng (Quality Gate) của Phase 1 trước khi bàn giao dữ liệu đã được xử lý NLP sang Phase 2 (Mô hình Học máy - ML Fusion). Nó đóng vai trò là **Cổng Hiệu chuẩn và Toàn vẹn Dữ liệu Liên pha (Inter-Phase Data Integrity & Calibration Gate)** và thực thi **Giao thức Chốt chặn Phân phối (Distributional Guardrail Protocol)** nhằm đảm bảo tập dữ liệu đủ mạnh, mang tính đại diện và chuẩn xác về mặt toán học cho các mô hình ML phía sau.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
Chức năng chính của bước này là xác thực và đảm bảo tính toàn vẹn thông qua các cổng kiểm duyệt khắt khe:

### 1. Ngăn chặn Sụp đổ Tín hiệu (Anti-Overfitting Gate) - PASS
- **Gate 1 (Kiểm tra màng lọc nhị phân):** Đảm bảo ít nhất **15%** tập dữ liệu được gắn cờ là CÓ RỦI RO (`AT_RISK` - Nhãn 1 & 2). 
  - **Kết quả thực tế:** `AT_RISK` đạt **66.02%** -> **[PASSED]**
- **Gate 2 (Kiểm tra mức độ nghiêm trọng):** Đảm bảo ít nhất **10%** tập dữ liệu `AT_RISK` được phân loại là RỦI RO CAO (`HIGH_RISK` - Nhãn 2).
  - **Kết quả thực tế:** Nhãn 2 ghi nhận 1,207 mẫu, tương đương **25.91%** -> **[PASSED]**
- *Kết luận:* Focal Loss đã xử lý Data Imbalance triệt để, tái thiết lập vùng phủ (Coverage) cho lớp tín hiệu yếu mà không cần phải can thiệp nhân tạo (như SMOTE hay Oversampling).

### 2. Xác thực Chuyển giao Đa phương thức (Data Integrity) - PASS
- Nhằm ngăn chặn việc thao túng dữ liệu hoặc lỗi phát sinh trong quá trình chuyển giao từ tập dữ liệu phi cấu trúc (NLP) sang ma trận cấu trúc (ML), P1-03 tự động tính toán và lưu lại mã băm **SHA256 Checksum** (Dấu vân tay số) của tập dữ liệu hoàn chỉnh cuối cùng.
- **Mã SHA256 (pseudo_labeled_final.csv):** `6e1f9ddd103638ba68ed9bc498a954dc74cbee240d43aaa9be75525ea22ec773`

## 📂 Các File Đầu ra
- `label_distribution_report.md`: Báo cáo tự động ghi nhận các chỉ số thống kê của kho dữ liệu, trạng thái Đạt/Trượt của các Quality Gate, và mã băm SHA256.
- `verdict.md`: Kết luận đánh giá tính hợp lệ khoa học của dữ liệu đầu ra.

## 🚀 Tác động lên Pipeline SCRM
Bằng cách vượt qua các ngưỡng này với tỷ lệ áp đảo, P1-03 đảm bảo mô hình ML ở Phase 2 luôn được cung cấp một "màng lọc tri thức" vô cùng chất lượng. Mô hình phía sau sẽ có đủ dữ liệu High-Risk để học các tương tác ẩn sâu thay vì chỉ chọn "lối tắt" dự báo số đông.
