# Báo Cáo Đánh Giá & Định Dạng Sơ Đồ (Verdict & Formatting Report)
**Đối tượng:** 2 sơ đồ chính (Phương pháp Nghiên cứu & Kiến trúc Hệ thống)
**Đánh giá viên:** Senior AI Architect / Expert Reviewer

## 1. Phát hiện Bất đồng bộ Phương pháp luận (Methodological Inconsistency)
Quá trình kiểm toán toàn diện mã nguồn và tài liệu (`MODERN_SCRM_WORKFLOW.md`) phát hiện một độ vênh nghiêm trọng giữa **khung khái niệm cũ (V1.0)** và **hệ thống mã nguồn hiện hành (V2.0)** đã được tối ưu hóa sau khi nhận phản hồi từ Mentor. Cụ thể:

- **Khái niệm đã lỗi thời (Deprecated V1.0):** Mô hình toán SWIP, biến `tts_days` (Time-to-Survive), 10 trường DistilBERT cố định, và công thức chốt chặn `FRS (S,P,I,R)` thủ công.
- **Tại sao bị loại bỏ?** Các Reviewer (đặc biệt Reviewer Q1) thường rất dị ứng với các mô hình heuristic pha trộn máy học mà không rõ nguồn gốc (như công thức FRS thủ công) hoặc các chỉ số có nguy cơ Data Leakage cao (như tính toán SWIP tĩnh trên chuỗi thời gian biến động).
- **Trạng thái thực tế (SOTA V2.0):** 
  - Hệ thống sử dụng **Geographic Weighting** (`weighted_geo_risk_w1`) để tính "Ripple Effect" (Hiệu ứng gợn sóng).
  - Tích hợp **Universal Information Extraction (UIE)** thay vì NLP truyền thống.
  - Xử lý Data Leakage bằng **Delta features** (`delta_avg_actual_lead_time`) và **Target Shift** (`w1_lead_time_ratio`).
  - Giao toàn quyền chốt chặn cuối cùng cho XGBoost xuất ra **Alert Probability**.

## 2. Phán quyết về Định dạng (Formatting Verdict)

Để 2 sơ đồ đạt chuẩn **"Strong Accept"** trên các tạp chí Q1 (IJPE, DSS), sơ đồ phải tuân thủ nghiêm ngặt nguyên lý thiết kế **"Information Bottlenecking & Data Integrity"**. 

### Yêu cầu "Rigor" cho Sơ đồ Phương pháp (Methodology Framework):
- Phải thể hiện được dòng chảy dữ liệu từ thô đến tinh.
- Bắt buộc phải có **Quality Gates** (như Fleiss' Kappa >= 0.70) ở khâu tiền xử lý, thể hiện sự khắt khe về chất lượng nhãn.
- Cần làm rõ cấu trúc đánh giá 2 chiều: **Walk-forward CV** (bảo vệ chuỗi thời gian) và **Ablation Study** (chứng minh giá trị của NLP).
- **Verdict:** Sơ đồ chỉ mạnh khi nó chứng minh được "Không có Look-ahead bias".

### Yêu cầu "Rigor" cho Sơ đồ Kiến trúc (System Architecture):
- Phải xóa bỏ khái niệm "Hộp đen" (Black-box). Thay vì vẽ mũi tên chung chung từ NLP vào XGBoost, phải trực quan hóa **Taxonomy-Conditioned AI** và **Context Shells**.
- Chèn thẳng các tham số chống rò rỉ như **Shift -1/-2** vào hình vẽ.
- Đóng dấu **SHA256 Checksum Data Integrity** vào một góc của khối Feature Matrix.
- **Verdict:** Nếu sơ đồ trực quan hóa được cách `Geographic Weighting` xử lý rủi ro lan truyền không gian (Spatial Propagation), bài báo sẽ ghi điểm tuyệt đối.

---
*Kết luận: Bản vẽ 2 sơ đồ sẽ được tái cấu trúc dựa trên thực tiễn của V2.0 nhằm vượt qua mọi bài kiểm tra khắt khe nhất của Q1 Reviewer.*
