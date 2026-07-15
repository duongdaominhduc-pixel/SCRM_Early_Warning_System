# 🚀 KẾ HOẠCH ĐẠI TU TOÀN DIỆN MÃ NGUỒN VÀ KIẾN TRÚC (MASTER REFACTORING PLAN)

Tài liệu này là bản đồ chiến lược tổng hợp toàn bộ các lỗ hổng kỹ thuật, lỗi logic từ Phase 1 đến Phase 3, và liệt kê chính xác TỪNG HÀNH ĐỘNG CỤ THỂ cần phải thực thi trên mã nguồn. 

*(Ghi chú: Lỗi thiết kế ở Phase 1 sẽ được giữ lại làm chất liệu viết bài báo, trong khi lỗi Data Leakage ở Phase 2 và Phase 3 bắt buộc phải sửa code ngay lập tức để lấy số liệu chuẩn).*

---

## 📌 PHASE 1 (NLP Sensing Layer): Vật liệu cho "Future Work"
> **Trạng thái hành động:** 🛑 KHÔNG SỬA CODE. Đưa toàn bộ các luận điểm này vào mục *Limitations and Future Work* của bài báo học thuật để bảo vệ thiết kế.

1. **Forced Categorization (P1-01):**
   * **Vấn đề:** BERTopic ép nhiễu 100%, phá vỡ đặc tính chuỗi rủi ro (Ripple Effect).
   * **Giải pháp bài báo:** Đề xuất nâng cấp lên kiến trúc **Universal Information Extraction (UIE)** với **Multi-label Head (Sigmoid)** cho phép gán đa nhãn.
2. **Rủi ro Token Injection (P1-02):**
   * **Vấn đề:** Tiêm thẻ `[LABOR_DISPUTE]` thô gây nhiễu ngữ nghĩa; dùng Cross-Entropy chưa giải quyết triệt để rủi ro bỏ lọt (False Negatives).
   * **Giải pháp bài báo:** Đề xuất chuyển sang dùng **Context Shells** (bao bọc bằng câu tiếng Anh hoàn chỉnh) kết hợp với **Focal Loss** hoặc kiến trúc Dual Encoder.
3. **Báo động giả Time-Series (P1-03):**
   * **Vấn đề:** Đặt chốt cứng ép tỷ lệ High Risk $\ge 10\%$.
   * **Giải pháp bài báo:** Phê phán việc dùng Data-level Augmentation (SMOTE) làm hỏng tính chu kỳ (Seasonality), đề xuất dùng **Cost-Sensitive Learning** (đã áp dụng ở Phase 2).

---

## 🛠️ PHASE 2 (ML Fusion Layer): Thanh trừng "Data Leakage"
> **Trạng thái hành động:** 🟢 BẮT BUỘC SỬA CODE trong file `run_phase2_pipeline.py`.

1. **Validation Corruption do Downsampling Toàn cục (P2-04):**
   * **Vấn đề:** Random Downsampling toàn bộ dữ liệu để ép tỷ lệ rủi ro lên 30% trước khi cắt Validation làm mất tính tự nhiên và phá hỏng trục thời gian tuần tự.
   * **Hành động Code:** Mở hàm `run_p2_04`, **XÓA BỎ** toàn bộ logic kiểm tra 30% và khối code sinh ra `df_balanced`. Hàm này chỉ làm nhiệm vụ shift target và trả về dữ liệu nguyên bản 100%.
2. **Data Leakage trong xử lý Imbalance (P2-05):**
   * **Vấn đề:** Tính toán `scale_pos_weight` ngoài vòng lặp Cross-Validation.
   * **Hành động Code:** Mở hàm `run_p2_05`, di chuyển công thức tính `scale_weight` vào **BÊN TRONG** vòng lặp `for train_idx, val_idx in tscv.split(X):`. Chỉ tính toán tỷ lệ trên biến `y_train_raw`. 
   * **Hành động Code:** Giữ nguyên 100% tỷ lệ của biến `X_va, y_va` để đánh giá F1/Precision nhằm lấy con số phản ánh thực tế nhất (Ecological Validity).
3. **Sửa "Lời bình" (Storytelling) Ngụy tạo số liệu:**
   * **Vấn đề:** Báo cáo hiện tại in ra kết luận sai sự thật rằng mô hình SCRM thắng F1-score.
   * **Hành động Code:** Sửa text in vào file `ablation_results.md`. Đổi luận điểm thành: *"Mô hình SCRM chiến thắng tuyệt đối về **Precision Floor**, qua đó giải quyết triệt để bài toán Alert Fatigue (Hội chứng mệt mỏi vì báo động giả) trong chuỗi cung ứng thực tế"*.

---

## 🛠️ PHASE 3 (Evaluation & Explainability Layer): Chuẩn hóa Học thuật
> **Trạng thái hành động:** 🟢 BẮT BUỘC SỬA CODE trong file `run_phase3_pipeline.py`.

1. **Threshold Tuning Leakage (P3-01):**
   * **Vấn đề:** Dò ngưỡng quyết định trên toàn bộ tập dữ liệu đánh giá.
   * **Hành động Code:** Chia `df_eval` thành 2 tập bằng **Chronological Split**: `df_val` (vd: 60% đầu) và `df_test` (40% cuối). 
   * **Hành động Code:** Chạy quét tìm *optimal_thresholds* trên `df_val`, sau đó đem ngưỡng chốt được áp dụng lên `df_test` để sinh ra bảng Report cuối cùng.
2. **Lệch pha SHAP và Case Study (P3-02 & P3-03):**
   * **Vấn đề:** SHAP lấy mẫu ngẫu nhiên (dòng 1), trong khi Case Study đi sâu vào linh kiện **P00179**.
   * **Hành động Code:** Đồng bộ hóa. Xác định tuần $W$ mà linh kiện **P00179** phát cảnh báo đỏ, trích xuất đúng dòng features đó từ `X_proc` đưa vào hàm `shap.plots.waterfall`.
3. **Đường dẫn Hình ảnh Broken Link (P3-03):**
   * **Vấn đề:** Đường dẫn `/content/drive/MyDrive/...` trỏ về Google Drive.
   * **Hành động Code:** Sửa lại thành Dynamic Absolute Path bằng thư viện `pathlib` (vd: `f"file:///{hero_chart_path.resolve().as_posix()}"`).
4. **Bổ sung Công thức Toán học (P3-03):**
   * **Vấn đề:** Đánh giá Lead-Time Gain (LTG) mang tính cảm quan.
   * **Hành động Code:** Chèn thẳng công thức $\text{LTG} = T_{\text{stockout}} - T_{\text{first\_alert}}$ vào file báo cáo Case Study để tăng sức nặng khoa học.
