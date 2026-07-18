# P2-02 | Hiệu chuẩn Độ nhạy Rủi ro Không gian (Spatial Risk Sensitivity Calibration)

## 📌 Tổng quan
Thực hiện phép nối mềm đa tầng (Geographic Weighting) giữa dữ liệu sự kiện rủi ro trên tin tức và danh mục vị trí vật lý của các nhà cung cấp (Suppliers) trong hệ thống nội bộ nhằm mô phỏng Hiệu ứng gợn sóng (Ripple Effect) của chuỗi cung ứng toàn cầu.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống áp dụng ma trận trọng số không gian: Match (1.0), Region (0.6), Global (0.1), và Macro Events (0.3).
- **Audit Status:** [PASS]. Các biến `weighted_geo_risk` đã được khởi tạo chuẩn xác trong file `news_supplier_joined.parquet`, thay thế hoàn toàn phép Inner Join cứng nhắc ở V1.0.
