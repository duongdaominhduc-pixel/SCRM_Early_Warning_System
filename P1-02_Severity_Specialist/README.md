# P1-02 | Chuyên gia Phân loại Mức độ Nghiêm trọng (Severity Specialist)

## 📌 Tổng quan
P1-02 là module cốt lõi của Tầng Nhận thức, nơi dữ liệu "rủi ro chung" được phân giải thành các cấp độ nghiêm trọng. Hệ thống được thiết kế để phân tách các vụ đứt gãy lớn (High-Risk) khỏi các sự cố vận hành thông thường (Medium-Risk).

## 🎯 Các kỹ thuật cốt lõi & Kết quả Audit (Methodology)

### 1. Kỹ thuật Context Shells
Thay vì dùng "Token Injection" thô sơ (`[LABOR_DISPUTE]`), hệ thống sử dụng cấu trúc **Context Shells**: 
`Context: This event involves {taxonomy}. Document: {text}`
Kỹ thuật này giúp mô hình (DistilBERT) được cung cấp bối cảnh ngữ nghĩa đầy đủ, nâng cao đáng kể độ chuẩn xác khi dự báo Severity.

### 2. Tránh bẫy Double Regularization (Audited: PASS)
Theo Gold Standard, việc kết hợp đồng thời **Focal Loss** và **Label Smoothing** trên một bộ dữ liệu quá nhỏ sẽ dẫn tới hiện tượng "Sụp đổ dải đầu ra" (Output Range Collapse), khiến mô hình trở nên underconfident và đoán mọi mẫu ở loanh quanh 0.5. 
Module P1-02 đã khéo léo lập trình lại `FocalLossTrainer` để loại bỏ `label_smoothing`, chỉ dùng duy nhất Focal Loss. Nhờ đó, nó xuất sắc duy trì được khả năng phát hiện các lớp High-Risk cực hiếm.

### 3. Cascading Guardrail (Audited: PASS - WITH FUTURE WORK)
- **Vấn đề:** Mã nguồn đang đặt ngưỡng cứng `score >= 0.5` cho việc chọn nhãn Zero-shot. Tương tự P1-01, việc hạ ngưỡng xuống `0.35` theo Gold Standard gây ra hiện tượng quá tải phần cứng khi huấn luyện (chạy hơn 11 tiếng).
- **Giải pháp:** Chấp nhận mức `0.5` cho đợt triển khai hiện tại để đảm bảo tiến độ. Việc nâng cấp hạ tầng để chạy mức `0.35` sẽ được ghi nhận là **Future Work** trong bài báo.

## 📂 Các File Đầu ra
- `pseudo_labeled_final.csv`: File output cuối cùng chứa nhãn gán giả (pseudo labels).
- `distilbert-severity/` & `severity_specialist_model/`: Thư mục chứa trọng số mô hình.
- `verdict.md`: Kết luận ML Audit, chỉ ra điểm cần refactor.
