# Báo cáo Đánh giá Kiến trúc: Lỗ hổng và Giải pháp tối ưu cho Tầng NLP Sensing (Phase 1)

## 📌 Tổng quan Triết lý Thiết kế
Hệ thống Cảnh báo Sớm Rủi ro Chuỗi cung ứng (SCRM - EWS) được thiết kế tuân thủ nghiêm ngặt nguyên tắc **Tính Giải trình (Accountability)** và **Tính Xác định (Determinism)**. Thay vì sử dụng các Generative LLM (như GPT-4) vốn tiềm ẩn rủi ro "ảo giác" (hallucinations) trong các quyết định vận hành, dự án sử dụng các Mô hình Ngôn ngữ Nhỏ (Encoder-only như DistilBERT) kết hợp với Machine Learning truyền thống.

Quá trình kiểm toán nội bộ (Self-auditing) Tầng NLP (Phase 1) đã phát hiện ra 3 điểm hạn chế (Limitations) về mặt thiết kế. Dưới đây là phân tích chi tiết các vấn đề, cách hệ thống hiện tại bù trừ, và các định hướng nâng cấp SOTA (State-of-the-Art) cho các nghiên cứu trong tương lai.

---

## 🚨 VẤN ĐỀ 1: Phân loại Cưỡng ép (Forced Categorization) và Sự biến mất của Đặc tính Đa nhãn

### 📍 Bản chất vấn đề (Tại P1-01)
Kỹ thuật **Outlier Reduction** của BERTopic đang ép 100% dữ liệu nhiễu vào Ontology (Khung danh mục tĩnh) thông qua Cosine Similarity. Đây là một phương pháp "cưỡng ép" (Hard-clustering) chỉ cho phép một bài báo mang DUY NHẤT một nhãn. 
Trong SCRM, rủi ro mang tính dây chuyền (Ripple Effect): Một trận bão có thể làm sập điện và gây kẹt cảng. Việc ép bài báo đa rủi ro vào một nhóm duy nhất làm mất đi tính toàn vẹn của chuỗi sự kiện.

### 💡 Giải pháp SOTA đề xuất (Cho Future Work)
- **Kiến trúc Universal Information Extraction (UIE):** Chuyển dịch từ việc gom cụm đơn thuần sang trích xuất thông tin cấu trúc (Structured Extraction Language) bằng các mô hình mạnh hơn như DeBERTa.
- **Multi-label Head (Sigmoid):** Ở lớp đầu ra của mô hình phân loại, thay vì dùng hàm `Softmax` (tổng các xác suất = 1, buộc phải chọn 1 nhãn), hãy chuyển sang dùng `Sigmoid` cho từng nhãn riêng biệt. Điều này cho phép một bản tin nhận đồng thời nhiều nhãn (ví dụ: Vừa là `WEATHER_DISASTER` vừa là `PORT_CONGESTION`).
- **Lớp "UNKNOWN":** Cho phép mô hình từ chối phân loại (gán nhãn NONE) nếu độ tự tin quá thấp, thay vì ép vào Ontology có sẵn.

---

## 🚨 VẤN ĐỀ 2: Báo động giả (False Alarms) và Phá vỡ Tính chu kỳ (Seasonality)

### 📍 Bản chất vấn đề (Tại P1-03)
Tại chốt chặn P1-03, dự án đặt ra luật cứng (Hard Gate): Tỷ lệ High Risk phải $\ge 10\%$, nếu không hệ thống sẽ tự động kích hoạt kỹ thuật sinh dữ liệu giả (SMOTE / Downsampling). 
Tuy nhiên, EWS là một bài toán chuỗi thời gian (Time-series). Việc dùng Data-level Augmentation (SMOTE) để "nhồi nhét" rủi ro vào những khoảng thời gian bình yên tự nhiên sẽ làm ô nhiễm tính chu kỳ (Seasonality), dẫn đến hàng loạt cảnh báo giả.

### 🛠️ Cách dự án đang giải quyết (Tại Phase 2)
May mắn thay, mô hình XGBoost ở P2-05 **không dùng SMOTE** mà dùng tham số `scale_pos_weight` của thư viện XGBoost. Đây chính là phương pháp **Cost-sensitive Learning**, phạt nặng khi đoán sai các mẫu thiểu số mà không cần tạo thêm data giả.

### 💡 Giải pháp SOTA đề xuất (Cho Future Work)
- **Ngưỡng Động (Dynamic Thresholding - AID-RAS):** Thay vì dùng con số 10% cố định (Hard Gate), ngưỡng cảnh báo rủi ro sẽ tự động co giãn dựa trên trạng thái của hệ thống ERP. Nếu chỉ số Lead-time đang rất ổn định, hệ thống tự động đòi hỏi một lượng tin xấu lớn hơn mới kích hoạt báo động.

---

## 🚨 VẤN ĐỀ 3: Rủi ro nhiễu từ Token Injection và Điểm mù False Negatives

### 📍 Bản chất vấn đề (Tại P1-02)
- **Token Injection thô:** Việc chèn trực tiếp các special token như `[LABOR_DISPUTE]` vào mô hình DistilBERT pre-trained (vốn chỉ hiểu ngôn ngữ tự nhiên) mà không train kỹ lớp Embedding sẽ biến token này thành "nhiễu ngữ nghĩa" (Semantic Noise) hơn là tri thức. (Nó dẫn đến hiện tượng Shortcut Learning đã thấy ở biểu đồ SHAP).
- **Điểm mù Recall:** Trong EWS, bỏ lọt một rủi ro (False Negative) nguy hiểm hơn rất nhiều so với báo động giả (False Positive). Hàm Loss hiện tại (`Weighted Cross-Entropy`) chỉ mới cân bằng dựa trên số lượng (Inverse Frequency), chưa trực tiếp nhắm vào độ khó của mẫu.

### 💡 Giải pháp SOTA đề xuất (Cho Future Work)
- **Context Shells (Lớp vỏ Ngữ cảnh):** Thay vì tiêm token thô `[LABOR_DISPUTE]`, hãy bọc văn bản bằng câu tiếng Anh chuẩn: *"This news describes a LABOR DISPUTE event at a key port facility: {Text}"*. DistilBERT sẽ lập tức hiểu ngữ cảnh này mà không cần học lại Embedding.
- **Focal Loss (Hàm Loss Tiêu điểm):** Thay thế Cross-Entropy bằng Focal Loss. Hàm này tự động hạ thấp trọng số của các mẫu dễ đoán (tin kinh tế bình thường) và dồn toàn lực tối ưu hóa độ nhạy (Recall) cho các tín hiệu rủi ro thưa thớt, cực khó.
- **Dual Encoder (Kiến trúc Two-Tower):** Mã hóa mô tả của Taxonomy và nội dung bài báo vào cùng một không gian vector. Độ đo Cosine giữa 2 tháp sẽ cung cấp chỉ số tương đồng có tính giải trình cao (Explainable Similarity) thay vì một lớp Classifier Hộp đen.

---

## 🏆 KẾT LUẬN: BÙ LỖI PHÂN TẦNG (Hierarchical Error Compensation)
Mặc dù Tầng NLP (Phase 1) mang những khiếm khuyết nội tại về mặt thuật toán, nhưng toàn bộ kiến trúc EWS này không sụp đổ. Nó ứng dụng triết lý **Hierarchical Error Compensation** (Bù lỗi phân tầng):
- Thiên kiến từ vựng của NLP được sửa chữa bằng **Trọng số Không gian (Spatial Risk Sensitivity Calibration)** tại Lớp 2.
- Hiện tượng học vẹt (Shortcut Learning) của NLP được vô hiệu hóa bằng **Nút thắt cổ chai thông tin (Agnostic Feature Fusion)** tại Lớp 3 (ML XGBoost).

Cấu trúc Self-correcting này chính là điểm sáng giá nhất của nghiên cứu, chứng minh khả năng quản trị dữ liệu (Data-centric AI) và mô phỏng chính xác luồng nhận thức của Chuyên gia Chuỗi cung ứng (Expert Cognitive Simulation).
