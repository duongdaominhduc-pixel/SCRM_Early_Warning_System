# P1-01 | Phân loại Danh mục Rủi ro (Risk Taxonomy Extraction)

## 📌 Tổng quan
**P1-01** là bước khởi đầu của Tầng Nhận thức NLP (Phase 1) trong Hệ thống Cảnh báo Sớm (EWS). Sau khi nhận tập dữ liệu gồm các tin tức mang tính rủi ro chung chung (từ màng lọc nhị phân P0-04), P1-01 có nhiệm vụ "chỉ mặt đặt tên", định tuyến các bài báo này vào các danh mục rủi ro cụ thể của chuỗi cung ứng (Ontology) như: Tắc nghẽn cảng, Đình công, Xung đột địa chính trị, v.v.

## 🎯 Các kỹ thuật cốt lõi & Kết quả Audit (Methodology)

### 1. Phân loại Zero-Shot Multi-label (Audited: PASS)
Hệ thống sử dụng sức mạnh của mô hình ngôn ngữ lớn (`facebook/bart-large-mnli`) kết hợp hàm kích hoạt Sigmoid để gán đa nhãn. Tuyệt vời nhất là hệ thống **không ép buộc 100% gán nhãn**. Nếu không có rủi ro nào đạt chuẩn, mô hình sẽ gán nhãn `GENERAL_DISRUPTION` (Unknown). Điều này giải quyết triệt để lỗi "Forced Categorization" thường gặp.

### 2. Định tuyến Danh mục tĩnh (Ontology Mapping)
Sử dụng kiến trúc Zero-Shot, hệ thống đối chiếu nội dung bài báo với Khung danh mục chuẩn (Static SCRM Ontology) đã được định nghĩa trước bởi chuyên gia (Domain Experts). Kết quả là mỗi bài báo được gán một loại sự kiện cụ thể (`final_event_type`) kèm theo Điểm tin cậy (`confidence_score`).

### 3. Cascading Guardrail (Audited: PASS - WITH FUTURE WORK)
- **Vấn đề:** Hiện tại, mã nguồn đang đặt ngưỡng cứng `score >= 0.5` cho việc chọn nhãn. Theo tiêu chuẩn Gold Standard, ngưỡng này khá nghiêm ngặt với các mô hình Zero-shot. Tuy nhiên, việc hạ ngưỡng xuống `0.35` đòi hỏi chi phí tính toán phần cứng khổng lồ (vượt quá 11 giờ trên Colab).
- **Giải pháp:** Quyết định duy trì mức `0.5` hiện tại để tối ưu hóa thời gian chạy. Việc hạ ngưỡng xuống `0.35` được đưa vào hạng mục **Future Work** cho phiên bản nâng cấp phần cứng trong tương lai.

## 📂 Các File Đầu ra
- `at_risk_with_taxonomy.csv`: Dữ liệu 5,762 bài báo được cấy thêm cột `final_event_type` và `confidence_score`.
- `risk_taxonomy_report.md`: Báo cáo chi tiết điểm độ tin cậy.
- `verdict.md`: Kết luận ML Audit, chỉ ra điểm cần refactor (Cascading Guardrail 0.35).

## 💡 Đóng góp Nghiệp vụ (Business Value)
Việc xuất ra được cột `confidence_score` là một thành công lớn của bước này. Thực tế cho thấy, những rủi ro hiện hữu rõ ràng như Đình công (*LABOR_DISPUTE*) có điểm tự tin rất cao, trong khi các rủi ro mập mờ có điểm thấp hơn. Sự khác biệt này là cơ sở để thiết lập hệ thống rào chắn (Cascading Guardrail) ở Phase tiếp theo.
