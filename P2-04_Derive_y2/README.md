# P2-04 | Dịch chuyển Nhãn Mục tiêu (Target Derivation)

## 📌 Tổng quan
Mô-đun chịu trách nhiệm thiết lập bài toán dự báo. Nhãn `stockout_flag` của tuần tương lai (W+1 và W+2) được dịch ngược về hàng thời gian hiện tại (W0) để tạo thành mục tiêu học máy.

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống đã sử dụng phương thức `.shift()` trên tập dữ liệu đã được sắp xếp để tạo nhãn tương lai.
- **Audit Status:** [PASS]. Không ghi nhận rò rỉ dữ liệu (Data Leakage) từ biến mục tiêu. File output `y2_shifted.parquet` an toàn cho ML training.
