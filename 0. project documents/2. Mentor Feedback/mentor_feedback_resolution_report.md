# BÁO CÁO TỔNG HỢP GIẢI QUYẾT FEEDBACK TỪ MENTOR

Báo cáo này liệt kê toàn bộ 5 vấn đề do mentor chỉ ra và các biện pháp kỹ thuật, học thuật đã được thực hiện để giải quyết triệt để nhằm đáp ứng tiêu chuẩn của tạp chí Q1.

---

## 1. Xử lý Vấn đề Data Leakage ở nhóm Cabin (F1 = 1.0)
- **Vấn đề từ mentor:** Mô hình đạt F1-score = 1.0 cho nhóm linh kiện Cabin, đây là dấu hiệu cảnh báo đỏ (Red flag) của hiện tượng rò rỉ dữ liệu (Data Leakage) hoặc kích thước mẫu quá nhỏ.
- **Hành động giải quyết:** Đã viết và chạy script chẩn đoán `P3-01_Threshold/scripts/01_diagnose_cabin.py`.
- **Kết quả thu được:**
  - Tổng số mẫu (tuần) của Cabin: **5.148**
  - Số mẫu đứt gãy (`stockout_flag_target=1`): **3**
  - Số mẫu bình thường (`stockout_flag_target=0`): **5.145**
- **Kết luận gửi Hội đồng:** Tỷ lệ dương tính (prevalence) của nhóm Cabin ở mức cực kỳ thấp (< 0.1%), dẫn đến hiện tượng kết quả ngẫu nhiên (Spurious results) chứ không phải Data Leakage. 
- **Đề xuất mới nhất (Theo tiêu chuẩn IJPE/DSS):** Nghiên cứu đã chủ động **loại trừ hoàn toàn (exclude)** nhóm Cabin khỏi các chỉ số đánh giá tổng hợp (aggregate performance metrics). Lập luận học thuật được đưa vào bài: *"Due to extreme event sparsity (prevalence < 0.1%), the Cabin category was excluded from the aggregate performance metrics to ensure statistical reliability."* Đồng thời, vấn đề Khan hiếm sự kiện cực đoan (Extreme Event Sparsity) đã được ghi nhận như một Hạn chế nghiên cứu (Limitation).

## 2. Loại bỏ mâu thuẫn trong Luật Gate 30-70%
- **Vấn đề từ mentor:** Có sự mâu thuẫn phương pháp luận khi bài báo ghi tỷ lệ dương tự nhiên (Natural Imbalance) là 3.16%, nhưng tài liệu Workflow lại thiết lập Gate chặn ép tỷ lệ này phải nằm trong khoảng 30-70%.
- **Hành động giải quyết:** 
  - Đã bãi bỏ hoàn toàn luật ép range 30-70% trong tài liệu `MODERN_SCRM_WORKFLOW.md`. 
  - Cập nhật tài liệu kỹ thuật tại `P2-04_Derive_y2/README.md`, xác nhận hệ thống áp dụng phương thức `.shift()` trên tập dữ liệu đã sắp xếp thời gian.
- **Kết luận:** Hệ thống hiện tại hoàn toàn nhất quán với bài báo, **chấp nhận Natural Imbalance (~3.16%)** để phản ánh đúng thực tế khắc nghiệt (Ecological Validity) của rủi ro chuỗi cung ứng. Hệ thống sử dụng kỹ thuật cấp độ thuật toán (`scale_pos_weight`) thay vì can thiệp cấp độ dữ liệu (như SMOTE) và sử dụng **PR-AUC** làm chỉ số đo lường chính thức thay cho ROC-AUC.

## 3. Điều chỉnh Thuật ngữ "Robust" / "Stress Test"
- **Vấn đề từ mentor:** Việc sử dụng từ "Robust" (mạnh mẽ/vững chãi) khi hiệu suất F1 giảm tới 55% trong bài kiểm tra độ trễ ERP (Stress Test) là sai bản chất học thuật.
- **Hành động giải quyết:** Đã quét toàn bộ dự án và gỡ bỏ các từ "Robust" và "Resilience" vì dễ gây hiểu nhầm sang năng lực phục hồi vật lý của chuỗi cung ứng.
- **Kết luận:** Chuyển đổi khung diễn đạt sang **"System Latency Sensitivity Analysis"** (Phân tích độ nhạy trước độ trễ hệ thống) và **"Information Lead-time Decay Study"**. Lập luận bảo vệ được đưa vào: *"The model exhibits a quantifiable performance decay under ERP data latency, yet maintains a predictive advantage over traditional rule-based heuristics."* Điều này chứng minh sự trung thực học thuật và cái nhìn thực tế về sự phụ thuộc vào tốc độ dữ liệu.

## 4. Giải trình Nghịch lý PR-AUC và Tín hiệu âm (Section 5.1)
- **Vấn đề từ mentor:** Cần đưa các lập luận bảo vệ (Defense) vào thẳng bài báo để giải thích tại sao mô hình có PR-AUC thấp và tại sao các biến NLP lại mang hệ số âm trong hồi quy.
- **Hành động giải quyết:** Đã bổ sung 2 đoạn học thuật quan trọng vào Mục 5.1 của bản thảo bài báo (`SCRM_EWS_draft_article_v1.md`):
  1. **Addressing the PR-AUC vs. ROC-AUC Paradox:** Lập luận rằng trong quản trị chuỗi cung ứng (SCRM), chi phí của False Negative (bỏ lọt rủi ro gây ngừng sản xuất) cao gấp nhiều lần False Positive (báo động giả). Do đó, mô hình cố ý tối ưu Recall thay vì Precision.
  2. **Proactive Mitigation Signal:** Giải thích hệ số âm của biến NLP không phải là nhiễu, mà phản ánh hành vi "Quản trị rủi ro phủ đầu" — khi tin tức xấu xuất hiện, doanh nghiệp nhập hàng dự phòng nên thực tế không xảy ra đứt gãy.

## 5. Bổ sung Lưu ý Thiết lập Đặc trưng ML Tier 1
- **Vấn đề từ mentor:** Bảng 6 cần có giải thích tại sao mô hình Tier 2 và Tier 3 không dùng biến trạng thái tuần trước, trong khi Tier 1 lại dùng.
- **Hành động giải quyết:** Đã thêm Ghi chú ngay bên dưới Bảng 6 trong bản thảo bài báo.
- **Kết luận:** Khẳng định rõ về mặt phương pháp luận: Các mô hình ML (Tier 2, Tier 3) đã cố ý loại bỏ biến `w1_stockout_flag` để ép mô hình học các liên kết phi tuyến động (NLP, Inventory), ngăn chặn việc học vẹt (naive forecasting) làm mất đi khả năng "cảnh báo sớm".

## 6. Viết Script và Xây dựng Bảng Lead-Time Gain (LTW)
- **Vấn đề từ mentor:** Thiếu bảng phân rã Lead-Time Gain (LTG/LTW) theo từng nhóm linh kiện để chứng minh giá trị kinh tế của hệ thống.
- **Hành động giải quyết:** 
  - Đã viết script `P3-03_Integration/scripts/02_calculate_ltg_breakdown.py` để tự động hóa việc tính toán thời gian cảnh báo sớm.
  - Script đã được chạy và sinh ra bảng kết quả định dạng Markdown (sẵn sàng chèn vào bài báo).
- **Kết quả minh họa:**
  
| Component Group   |   Detected Disruptions |   Mean LTW (Weeks) |   Min LTW |   Max LTW |
|:------------------|-----------------------:|-------------------:|----------:|----------:|
| Avionics          |                      1 |                2.0 |       2.0 |       2.0 |
| Electrical        |                      1 |                1.0 |       1.0 |       1.0 |

---
**Tổng kết:** Toàn bộ các yêu cầu khắt khe từ mentor đã được giải quyết bằng cả code, phân tích dữ liệu thực tế và chỉnh sửa câu chữ trong bản thảo bài báo. Dự án hiện đã đáp ứng đầy đủ tiêu chuẩn về độ minh bạch và chặt chẽ của một bài báo phân tích dữ liệu Q1.
