# P0-05: Đánh giá Phân phối Tổng thể & Rào chắn Chống Học Vẹt (Anti-Overfitting Gate)

## Mục tiêu
Bước cuối cùng trong Giai đoạn 0 là cuộc thanh tra thống kê (statistical audit) trên toàn bộ tập dữ liệu tổng hợp. Việc này đảm bảo rằng sự tham gia của dữ liệu Pseudo-label không gây ra hiện tượng "thiên kiến số đông" (majority-class bias) làm bóp méo đi các tín hiệu rủi ro cốt lõi cần thiết cho Giai đoạn Machine Learning (ML) phía sau.

## Phương pháp luận & Tính Khoa học
*   **Thanh tra Phân phối:** Chúng tôi xác minh lại tỷ lệ phân bố nhãn trên toàn bộ **5.313 bài báo**:
    *   **Nhãn 0 (Không Rủi ro):** 66%
    *   **Nhãn 1 (Rủi ro Trung bình):** 25%
    *   **Nhãn 2 (Rủi ro Cao):** 8%
*   **Rào chắn Chống Học vẹt (Anti-Overfitting Gate):** Chúng tôi đối chiếu phân phối của tập dữ liệu tăng cường với phân phối của tập Tiêu chuẩn Vàng ban đầu. Sự nhất quán này khẳng định rằng đường ống Pseudo-label đã nắm bắt chính xác tần suất xuất hiện các rủi ro ẩn trong toàn bộ kho tin tức mà không làm mô hình trở nên "quá nhạy cảm" với lớp Nhãn Rủi ro Cao.
*   **Giá trị Ứng dụng:** Tỷ lệ phân phối này cung cấp một tham số quan trọng cho kỹ thuật **Học Nhạy cảm với Chi phí (Cost-Sensitive Learning)** trong Giai đoạn ML, đảm bảo hệ thống luôn nhạy bén với các sự kiện gián đoạn chuỗi cung ứng dù chúng có xác suất xảy ra rất thấp.

## Cấu trúc Thư mục
- `output/`: Chứa Báo cáo Phân phối cuối cùng (`label_distribution_report.md`) và script kiểm định (`check_distribution_p0_05.py`).
- `pipeline_data/`: (Dữ liệu được lấy trực tiếp từ thư mục đầu ra của `P0-04_Pseudo_Labeling`).
- `scripts/`: (Trong giai đoạn này, script kiểm định đã được xếp vào output).
- `archive/`: Chứa các bản chụp (snapshots) phân phối lỗi thời của các vòng lặp trước.

## Hướng dẫn Chạy lại (Reproduction)
1.  Đảm bảo cả 2 file `manual_combined_2309.csv` và `pseudo_labeled_refined.csv` đều nằm trong thư mục output của P0-04.
2.  Chạy script `output/check_distribution_p0_05.py` để nạp tập dữ liệu gộp.
3.  Xem kết quả hiển thị trên Console để kiểm chứng dữ liệu đã vượt qua "Rào chắn Chống Học vẹt".
4.  Xuất kết quả chốt hạ ra file `output/label_distribution_report.md`.
