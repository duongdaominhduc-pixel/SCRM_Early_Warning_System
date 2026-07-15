# P2-03 | Ma trận Biến số Thời gian (Feature Matrix Aggregation)

## 📌 Tổng quan
Khởi tạo ma trận chuỗi thời gian theo tuần (ISO week) cho từng mã linh kiện (Part ID). Kết hợp dữ liệu vận hành nội bộ (ERP) và tín hiệu cảnh báo bên ngoài (NLP SCRM) vào một bảng phân tích chung.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống đã kết dính chuẩn xác dữ liệu theo `w1_` (T-1) và `w2_` (T-2) để phục vụ cho Stress Test về độ trễ hệ thống ERP.
- **Cảnh báo (Audited: NEED REFACTOR):** ML Audit phát hiện hệ thống bỏ qua kiểm định tính dừng (Stationarity / ADF Test) cho các biến nội bộ ERP. Cần tạo biến Delta (sai phân bậc 1) cho các biến như tồn kho hoặc khối lượng đơn hàng để tránh hiện tượng Spurious Regression trước khi đưa vào XGBoost. Đọc `verdict.md` để xem chi tiết.
