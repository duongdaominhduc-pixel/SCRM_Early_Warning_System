# Phase P2-01: Threshold Optimization (Tối ưu Ngưỡng Cảnh báo)

## 1. Mục tiêu (Objective)
Trong Quản trị rủi ro chuỗi cung ứng (SCRM), tập dữ liệu cảnh báo đứt gãy thường mang tính chất **mất cân bằng cực đại (Extreme Imbalance)**. Tại nghiên cứu này, tỷ lệ lớp dương (Positive Rate) chỉ ở mức **3.16%**. 

Việc sử dụng ngưỡng quyết định mặc định (Threshold = 0.5) của các thuật toán Machine Learning thường không đem lại hiệu quả vận hành tốt nhất. Mục tiêu của Phase P2-01 là chạy phân tích độ nhạy (Sensitivity Analysis) để tìm ra **"Managerial Sweet Spot"** (Điểm cân bằng quản trị) — một ngưỡng quyết định giúp hệ thống cân bằng giữa hai bài toán:
- Tránh **Alert Fatigue** (Mệt mỏi vì cảnh báo giả - Cần Precision cao).
- Đảm bảo **Resilience Safeguard** (Lưới bảo vệ chuỗi cung ứng - Cần Recall hợp lý).

## 2. Phương pháp luận
- **Thuật toán**: XGBoost SCRM (Tích hợp dữ liệu Ops và NLP).
- **Chiến lược kiểm định**: K-Fold `TimeSeriesSplit` (gap=2 tuần) để đảm bảo không rò rỉ dữ liệu tương lai (Look-ahead bias).
- **Quét ngưỡng**: Lặp threshold từ 0.05 đến 0.95 để ghi nhận sự thay đổi của Precision, Recall, F1-Score, và F0.5-Score.

## 3. Quyết định Học thuật (Academic Decision)
Dựa trên tư vấn của chuyên gia bình duyệt (Reviewer) từ các tạp chí Q1 (IJPE, DSS), chúng tôi quyết định chọn ngưỡng **Threshold = 0.70** (tối đa hóa F1-Score) làm "Managerial Sweet Spot".

**Lý do chọn 0.70:**
- **Về mặt kỹ thuật**: Đạt F1-Score cao nhất (`0.220`), cung cấp một điểm neo thống kê (statistical anchor) vững chắc. Precision đạt **18.3%** (cao gấp 6 lần so với dự đoán ngẫu nhiên và gấp 3 lần so với Heuristic Rule-Based hiện hành). Recall đạt **27.6%**.
- **Về mặt quản trị**: 
  - Tránh được cạm bẫy của ngưỡng `0.85` (Nơi Precision đạt 23.1% nhưng Recall rớt thảm hại xuống 17.2%). Một hệ thống bỏ lọt tới hơn 80% rủi ro đứt gãy bị coi là quá "giòn" (brittle) và không đáp ứng được yêu cầu bảo vệ mạng lưới chuỗi cung ứng.
  - Ngưỡng 0.70 đem lại "Khả năng cảm biến" (Visibility) đủ rộng để hệ thống có ý nghĩa về mặt vận hành, đồng thời có Precision đủ sắc bén để thiết lập niềm tin của người dùng.

## 4. Ý nghĩa hệ thống (Downstream Impact)
Ngưỡng `0.70` này sẽ được làm mốc chuẩn (baseline threshold) cho hai Phase tiếp theo:
- **P2-03 (SHAP)**: Giải thích lý do vì sao một trường hợp cụ thể lại tích lũy đủ điểm rủi ro để vượt qua vạch kẻ 0.70 này.
- **P2-02 (Integration Test)**: Hệ thống thời gian thực sẽ tự động kích hoạt Còi báo động (Red Alert) ngay khi `Predicted_Probability >= 0.70`.
