# P2-02 | Kết nối Không gian Địa lý (Geo Join)

## 📌 Tổng quan
Thực hiện phép nối (Join) mềm giữa dữ liệu sự kiện rủi ro trên tin tức và danh mục vị trí vật lý của các nhà cung cấp (Suppliers) trong hệ thống nội bộ.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống ghép nối dựa trên `news_country_code` và vị trí nhà cung cấp.
- **Audit Status:** [PASS]. Các tính năng kết nối không gian đã được khởi tạo chuẩn xác trong file `news_supplier_joined.parquet`.
