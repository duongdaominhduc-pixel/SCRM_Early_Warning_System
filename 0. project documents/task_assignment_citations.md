# BẢNG PHÂN CÔNG TÌM VÀ TRÍCH DẪN TÀI LIỆU (CITATIONS)

## 1. Mục tiêu Công việc
Hoàn thiện hệ thống tài liệu tham khảo cho bài báo nghiên cứu. Mọi luận điểm, số liệu, và phương pháp được đề cập trong bài viết đều phải được chứng minh bằng các tài liệu khoa học đáng tin cậy.

## 2. Tài nguyên Quan trọng
Tất cả các thành viên BẮT BUỘC ưu tiên sử dụng các tài liệu đã được nạp sẵn và tổng hợp trên hệ thống Notebook LM của nhóm trước khi tìm kiếm nguồn ngoài. Đồng thời, mọi code/phương pháp thực tế phải được đối chiếu với GitHub Repo.

* **Link Notebook LM (Nguồn tài liệu chính):** `[ĐIỀN LINK NOTEBOOK LM VÀO ĐÂY]`
* **Link GitHub Repo (Kiểm chứng Methodology/Code):** `[ĐIỀN LINK GITHUB REPO VÀO ĐÂY]`

---

## 3. Quy trình Thực hiện (Guideline)

Để đảm bảo tiến độ và sự đồng bộ, các bạn làm theo 3 bước sau:

**Bước 1: Đọc và hiểu văn cảnh**
- Truy cập vào file Google Docs của bài báo.
- Đọc kỹ đoạn văn bản thuộc phần (Section) bạn được phân công để hiểu ý chính cần trích nguồn (ví dụ: một khái niệm về SCRM, một chỉ số NLP, hoặc phương pháp Machine Learning).

**Bước 2: Tìm nguồn chứng minh**
- Lên **Notebook LM** (link ở trên), gõ từ khóa vào để hệ thống trích xuất các paper có liên quan.
- Đọc lướt qua paper đó để lấy thông tin tác giả, năm, và ý chính.
- **⚠️ Quy tắc Năm xuất bản:** Cố gắng đảm bảo 60-70% tài liệu được trích dẫn xuất bản từ năm **2020 trở đi** (đặc biệt là các bài về SCRM hậu đại dịch). **Ngoại lệ duy nhất:** Các bài báo gốc khai sinh ra thuật toán (như XGBoost năm 2016, SHAP năm 2017, DistilBERT năm 2019...) thì bắt buộc dùng bản gốc dù trước 2020.
- *(Chỉ khi Notebook LM không có nguồn phù hợp, bạn mới ra ngoài tìm bằng Google Scholar / Semantic Scholar).*

**Bước 3: Ghi chú (Comment) trên Google Docs**
- Ghi nguồn dạng In-text citation trực tiếp vào đoạn văn trên Google Docs (ví dụ: `(Cano-Marin et al., 2023)`).
- **Bôi đen nguyên đoạn cần trích dẫn + cái In-text citation đó**, rồi bấm **Add Comment (Thêm nhận xét)**.
- Trong khung Comment, bạn ghi rõ trích dẫn chi tiết sẽ đặt ở mục References cuối bài theo đúng **chuẩn APA 7**.

> **💡 Ví dụ về cách làm chuẩn trên Docs:**
> - Viết vào bài: `...đóng vai trò quan trọng trong chuỗi cung ứng (Cano-Marin et al., 2023).`
> - Comment vào đoạn bôi đen: `Ref: Cano-Marin, E. (2023). Supply chain disruption forecasting using machine learning. Journal of Supply Chain Management, 15(2), 112-130. https://doi.org/...`

---

## 4. Cách Kiểm chứng Thông tin (Fact-Checking) CỰC KỲ QUAN TRỌNG

Tuyệt đối KHÔNG trích dẫn "đại" cho có. Mọi thông tin phải được kiểm chứng chéo:

### A. Đối với phần Introduction & Literature Review
- Phải đảm bảo paper bạn trích dẫn có nói đúng ý đó. Khuyến khích copy 1 câu quote gốc trong paper dán kèm vào comment để Leader dễ kiểm tra.

### B. Đối với phần Methodology & Results (Nghiệp vụ thực tế)
- **BẮT BUỘC:** Phải vào **GitHub Repo** (link ở trên) để đối chiếu thông tin!
- **Lý do:** Những gì viết trong bài báo phải khớp 100% với những gì model code thực tế đã chạy. 
- **Cách làm:** Ví dụ bài báo ghi "Sử dụng DistilBERT và đạt Kappa = 0.635", bạn phải mở file code đánh giá trên GitHub ra xem kết quả in ra có đúng là 0.635 không. Nếu thấy khớp, mới được tìm các tài liệu về công thức tính Kappa để trích dẫn vào.

---

## 5. Bảng Phân công Chi tiết

Bảng dưới đây chia việc cụ thể cho từng thành viên đảm nhận việc tìm và chèn trích dẫn cho từng Section:

| Mục (Section) cần tìm trích dẫn | Thành viên phụ trách | Hạn chót (Deadline) | Trạng thái | Ghi chú thêm |
| :--- | :--- | :--- | :--- | :--- |
| **1. Introduction** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Tìm nguồn củng cố các case study (Suez Canal, Covid-19...) |
| **2. Literature Review** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Bám sát các paper trên Notebook LM. |
| **3. Methodology (Phase 0 & 1)** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Check code DistilBERT, BART-large trên Repo. |
| **3. Methodology (Phase 2 & 3)** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Check code XGBoost, Time-Series split trên Repo. |
| **4. Results & Discussion** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Check bảng log kết quả (PR-AUC, F1...) trên Repo. |
| **5. Conclusion** | `[Tên thành viên]` | `[DD/MM/YYYY]` | ⏳ Đang làm | **BẮT BUỘC TRÍCH NGUỒN ĐẦY ĐỦ.** Check lại các Lead-Time Gain. |

*Lưu ý: Bạn nào hoàn thành xong phần của mình thì đổi "Trạng thái" thành `✅ Hoàn thành` để cả nhóm cùng theo dõi nhé!*

---

## 6. Chiến lược Trích nguồn (Citation Strategy) chi tiết

Dựa trên nội dung của bản draft bài báo, các bạn phụ trách từng phần cần bám sát các từ khóa và luận điểm sau để tìm tài liệu tham khảo:

### 1. Introduction
- **Case studies:** Tìm các báo cáo thực tế/bài báo uy tín về thiệt hại của vụ mắc cạn tàu *Ever Given* ở kênh đào Suez (2021), Khủng hoảng thiếu hụt chip/bán dẫn (2021-2023), và Vụ chuyển hướng tàu biển ở Biển Đỏ (2024).
- **Số liệu:** Tìm trích dẫn gốc hoặc báo cáo tương đương cho số liệu "87% doanh nghiệp sản xuất gặp gián đoạn chuỗi cung ứng (Gartner, 2023)".

### 2. Literature Review
- **SCRM Framework:** Tìm nguồn cho mô hình 4 bước kinh điển (Risk Identification, Assessment, Mitigation, Monitoring).
- **NLP trong SCRM:** Tìm các paper dùng Sentiment Analysis trong chuỗi cung ứng và các paper chỉ ra hạn chế của phương pháp này (sự nhập nhằng về ngữ nghĩa - semantic ambiguity).
- **Machine Learning Pitfalls:** **Bắt buộc** tìm các bài báo cảnh báo về lỗi rò rỉ dữ liệu thời gian (**Temporal Leakage**) và hồi quy giả mạo (**Spurious Regression** do dữ liệu non-stationary) trong dự báo rủi ro chuỗi cung ứng.

### 3. Methodology
- **Phase 0 & 1 (NLP):** Tìm các bài báo gốc của mô hình **DistilBERT** (Sanh et al., 2019) và **BART-large-MNLI** (Zero-shot learning). Tìm trích dẫn học thuật giải thích cho Label Smoothing và hàm CrossEntropyLoss.
- **Phase 2 & 3 (ML & Fusion):** Tìm nguồn giải thích về hàm suy giảm theo khoảng cách/trọng số địa lý (**Geographic Weighting**). Tìm trích dẫn cho kiểm định **Augmented Dickey-Fuller (ADF)**, mô hình **XGBoost** (Chen & Guestrin, 2016), và kỹ thuật Walk-forward validation (`TimeSeriesSplit`).
- **Data Governance:** Tìm nguồn tài liệu về việc ứng dụng chuẩn băm **SHA-256 Checksum** trong bảo mật và bảo toàn tính nguyên vẹn của dữ liệu.

### 4. Results & Discussion
- **Metrics (Chỉ số đánh giá):** Tìm các paper ủng hộ việc dùng **PR-AUC** và **F0.5-Score** thay vì ROC-AUC đối với bài toán dữ liệu mất cân bằng (imbalanced data). Trích dẫn cho **Expected Calibration Error (ECE)**.
- **Explainable AI:** Bắt buộc trích dẫn paper gốc của thuật toán **SHAP** (Lundberg & Lee, 2017) khi giải thích mô hình.

### 5. Conclusion
- Tập trung tìm các tài liệu/nghiên cứu đánh giá tầm quan trọng của **Lead-Time Gain** (Thời gian cảnh báo sớm) đối với hiệu quả quản trị hàng tồn kho dự phòng và tính kiên cường (resilience) của chuỗi cung ứng.
