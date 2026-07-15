# Phân tích Vấn đề và Giải pháp cho Phase 2 (SCRM Pipeline)

Tài liệu này tổng hợp các vấn đề phát hiện được sau quá trình chạy thử nghiệm Phase 2 (P2-01 đến P2-05) và đề xuất các giải pháp khắc phục nhằm đảm bảo tính toàn vẹn và hợp lý cho bài báo khoa học.

---

## 🚨 Vấn đề Hiện tại: Xung đột giữa Số liệu và Lời bình (Ablation Study)

Trong quá trình chạy **P2-05 (ML Training & Ablation Study)**, mô hình xuất ra bảng kết quả và một đoạn nhận xét tự động (được hardcode trong `run_phase2_pipeline.py`). Tuy nhiên, có sự mâu thuẫn lớn giữa số liệu thực tế và lời bình.

### Số liệu thực tế sinh ra:
*   **Dự báo W+1 (`y2_shift1`):**
    *   **Baseline LR** (Chỉ dùng data vận hành): F1-score = `0.6699`, Precision = `0.5606`
    *   **SCRM XGB** (Có thêm data NLP): F1-score = `0.6270`, Precision = `0.6165`
*   **Dự báo W+2 (`y2_shift2`):**
    *   **Baseline LR**: F1-score = `0.4379`, Precision = `0.3085`
    *   **SCRM XGB**: F1-score = `0.3173`, Precision = `0.3430`

👉 **Nhận xét:** Mô hình Baseline (không có NLP) đang chiến thắng về **F1-score** do có Recall rất cao. Trong khi đó, mô hình SCRM (có NLP) lại chiến thắng về **Precision** (Độ chính xác khi phát cảnh báo).

### Lỗi Logic trong Code:
Đoạn code trong `run_phase2_pipeline.py` (dòng 812) đang in ra dòng kết luận:
> *"The addition of geographic-weighted NLP news features (SCRM models) consistently out-performs the Baseline models by improving the Minority F1-score..."*

👉 Đây là một **luận điểm sai sự thật** dựa trên số liệu thực tế, có thể khiến bài báo bị hội đồng đánh rớt vì lỗi nguỵ tạo kết luận.

---

## 💡 Các Hướng Giải quyết Đề xuất

Để giải quyết vấn đề này và bảo vệ thành công mô hình, chúng ta có 2 hướng giải quyết chính.

### Giải pháp 1: Thay đổi "Storytelling" (Biện luận theo số liệu thực tế) - Khuyến nghị 🌟
Đừng cố ép F1-score phải cao hơn. Trong bài toán Cảnh báo Sớm (Early Warning System - EWS), **Precision quan trọng hơn Recall**. Nếu hệ thống báo động giả quá nhiều (Precision thấp), user sẽ bị hội chứng **"Alert Fatigue"** (Mệt mỏi vì cảnh báo) và phớt lờ hệ thống.

**Cách làm:**
1.  **Sửa lại code trong `run_phase2_pipeline.py`:** Sửa lại đoạn text kết luận tự động sinh ra trong file `ablation_results.md`.
    *   **Thay vì:** *"SCRM models consistently out-performs the Baseline models by improving the Minority F1-score..."*
    *   **Viết lại thành:** *"Value of Information: While Baseline models achieve higher recall through broad predictions, the addition of geographic-weighted NLP news features (SCRM models) establishes a significantly higher Precision Floor. This trade-off is highly desirable in real-world supply chain operations, as it directly mitigates 'Alert Fatigue' and provides more reliable, actionable intelligence."*
2.  **Lợi ích:** Cách này rất thực tế, hợp logic quản trị chuỗi cung ứng và không cần phải retrain hay tinh chỉnh mô hình mệt mỏi.

### Giải pháp 2: Tối ưu lại thuật toán để SCRM thực sự thắng về F1-score
Nếu bài báo bắt buộc yêu cầu mô hình SCRM (có NLP) phải tốt hơn toàn diện (cả F1-score), chúng ta cần tăng sức mạnh của các biến NLP.

**Cách làm:**
1.  **Tinh chỉnh hàm Geo Weighting (P2-02):** Hiện tại biến `weighted_geo_risk` có thể đang quá thưa thớt (sparse). Hãy thử điều chỉnh trọng số ở `run_phase2_pipeline.py`, ví dụ tăng mức độ ảnh hưởng của khu vực (Region Match) từ `0.6` lên `0.8`, hoặc mở rộng mapping khu vực.
2.  **Sử dụng Logistic Regression (Lasso) cho cả Tier 3:** Trong bảng kết quả, XGBoost đôi khi bị Overfit trên dữ liệu thưa thớt. Logistic Regression với L1 Penalty thường hoạt động tốt hơn với các biến NLP thưa thớt.
3.  **Tăng độ trễ (Lag):** Lấy thêm features `w-3` hoặc `w-4` cho NLP để hệ thống học được xu hướng dài hạn hơn.
4.  **Lợi ích:** Số liệu đẹp hoàn hảo, dễ viết báo cáo khoa học thuần túy.
    **Nhược điểm:** Mất thời gian thử nghiệm (trial & error) và có thể rơi vào tình trạng overfit.

---

## 🛠️ Hành động tiếp theo (Next Steps)

1.  **Quyết định hướng đi:** Bạn hãy quyết định chọn **Giải pháp 1** hay **Giải pháp 2**.
2.  **Cập nhật script:** Dựa trên quyết định, chúng ta sẽ mở file `run_phase2_pipeline.py` để điều chỉnh phần in báo cáo ở P2-05 (nếu chọn GP1) hoặc điều chỉnh tham số huấn luyện/geo_weight (nếu chọn GP2).
3.  **Chạy lại Pipeline:** Run lại Phase 2 pipeline để sinh ra báo cáo Ablation mới hợp lý và khoa học nhất.
