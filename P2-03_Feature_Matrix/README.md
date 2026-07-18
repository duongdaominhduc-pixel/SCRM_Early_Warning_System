# P2-03 | Ma trận Biến số Thời gian (Feature Matrix Aggregation)

## 📌 Tổng quan
Khởi tạo ma trận chuỗi thời gian theo tuần (ISO week) cho từng mã linh kiện (Part ID). Kết hợp dữ liệu vận hành nội bộ (ERP) và tín hiệu cảnh báo bên ngoài (NLP SCRM) vào một bảng phân tích chung.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống đã kết dính chuẩn xác dữ liệu theo `w1_` (T-1) và `w2_` (T-2) để phục vụ cho Stress Test về độ trễ hệ thống ERP.
- **Audit Status:** [PASS - V2.0 SOTA]. Hệ thống đã được tích hợp kiểm định tính dừng (Stationarity / ADF Test) cho các biến nội bộ ERP. Các biến Delta (sai phân bậc 1) như `w1_delta_avg_actual_lead_time` và `w1_delta_on_hand_inventory` đã được tự động sinh ra để cung cấp "Momentum" (Động lượng) cho chuỗi thời gian, loại bỏ hoàn toàn rủi ro Hồi quy giả mạo (Spurious Regression) trước khi đưa vào XGBoost.
