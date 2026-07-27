# P3-03 | Tích hợp Hệ thống (End-to-End Simulation)

## 📌 Tổng quan
Mô phỏng lại toàn bộ luồng chảy của một cảnh báo rủi ro thực tế trong môi trường chuỗi cung ứng, từ khi báo chí đăng tin (Sensing) đến khi kích hoạt cảnh báo vượt ngưỡng (Threshold) và xảy ra đứt gãy tồn kho thực tế. Đồng thời, đánh giá tính hiệu quả kinh tế thông qua chỉ số thời gian bù đắp rủi ro (Lead-Time Gain - LTG).

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống đã vẽ thành công bảng điều khiển **3-Panel Hero Chart** (`case_study_hero_chart.png`) minh họa Case Study cho linh kiện có tần suất đứt gãy cao.
- **Quantitative LTG Breakdown:** Đã trích xuất lịch sử cảnh báo của toàn bộ hệ thống vào file `weekly_alerts.csv` và tính toán định lượng thời gian cảnh báo sớm (`Mean LTW`) cho từng nhóm linh kiện (Avionics, Electrical, Structure...). Kết quả này xóa bỏ rủi ro chọn lựa số liệu có lợi (Cherry-picking) và đảm bảo tiêu chuẩn Giải trình thuật toán (Algorithmic Accountability).
- **Data Governance:** Các file báo cáo cuối cùng (bao gồm cả báo cáo Case Study) đều được băm SHA256 Checksum, hoàn thiện tính toàn vẹn dữ liệu xuyên suốt pipeline.
