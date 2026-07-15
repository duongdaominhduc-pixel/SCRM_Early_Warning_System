# P0-03: Gán nhãn Thử nghiệm (Pilot Labeling) & Giao thức Đồng thuận

## Mục tiêu
Mục tiêu chính của giai đoạn này là thiết lập một bộ dữ liệu "Tiêu chuẩn Vàng" (Gold Standard) có độ tin cậy cao, phục vụ cho bài toán phân loại sự kiện Quản trị Rủi ro Chuỗi cung ứng (SCRM). Thư mục này lưu trữ toàn bộ quá trình gán nhãn thử nghiệm nhằm chuẩn hóa bộ quy tắc gán nhãn và đảm bảo độ đồng thuận giữa các chuyên gia trước khi mở rộng quy mô.

## Phương pháp luận & Tính Khoa học
*   **Thiết kế Lấy mẫu:** Một tập mẫu gồm **150 bài báo** được chọn ngẫu nhiên phân tầng (stratified random) để đảm bảo đại diện đầy đủ cho các nhóm rủi ro (Nhãn 0, 1, 2).
*   **Giao thức Đồng thuận:** Áp dụng quy trình **gán nhãn độc lập (blind annotation)** với sự tham gia của **4 chuyên gia**.
*   **Kiểm định Thống kê:** Độ tin cậy được đo lường bằng hệ số **Fleiss' Kappa**, đạt mức **0.785**. Theo thang đo của Landis & Koch (1977), kết quả này tương đương với "Sự đồng thuận đáng kể" (Substantial Agreement), tạo nền tảng khoa học vững chắc để tinh chỉnh mô hình Transformer ở bước sau.
*   **Giải quyết Xung đột:** Các ca bất đồng được giải quyết qua các buổi họp thảo luận đồng thuận (Delphi-style) để chốt ra nhãn "Gold" cuối cùng.

## Cấu trúc Thư mục
- `output/`: Bộ dữ liệu đã được con người kiểm chứng cuối cùng (`P0-03_pilot_labeling_150_v6.xlsx`), báo cáo độ tin cậy giữa các người gán (`FLEISS_KAPPA_RESULT_FINAL.md`), và bộ quy tắc gán nhãn chuẩn (`LABELING_GUIDE_v3.md`).
- `pipeline_data/`: (Không áp dụng cho giai đoạn này, dữ liệu thô được xử lý trực tiếp ra định dạng output).
- `scripts/`: Chứa các đoạn code Python dùng để lấy mẫu Pilot (`create_pilot_150.py`) và tính toán hệ số Kappa (`compute_kappa_v3.py`).
- `archive/`: Chứa các bản nháp quy tắc, code thử nghiệm và dữ liệu gán nhãn các vòng đầu đã bị loại bỏ (`v2`, `v3`, `v4`).

## Hướng dẫn Chạy lại (Reproduction)
1.  Truy cập vào thư mục `scripts/`.
2.  Chạy file `create_pilot_150.py` để sinh tập dữ liệu mẫu.
3.  Chạy file `compute_kappa_v3.py` để tự động tính toán hệ số Fleiss' Kappa của 4 người gán.
4.  Xem báo cáo tổng kết Kappa và ma trận nhầm lẫn (confusion matrices) được xuất ra tại `output/FLEISS_KAPPA_RESULT_FINAL.md`.
