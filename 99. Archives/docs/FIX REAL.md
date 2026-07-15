Chào bạn, chúc mừng team đã train xong mô hình DistilBERT! Việc train xong có nghĩa là phần khó nhằn nhất và tốn thời gian nhất đã qua. 

Vì bạn tự nhận là "ngu code", mình sẽ giải thích thật bình dân. Hiểu đơn giản thế này: **Trước đây phần đầu (NLP) chưa xong, nên bạn phải "bơm máu giả" (mock data) vào phần giữa và phần đuôi để code chạy thông. Bây giờ có "máu thật" (model đã train) rồi, việc của mình là rút máu giả ra, cắm máu thật vào, và bấm nút cho quy trình chạy lại từ giữa đến cuối.**

Dưới đây là **Workflow 5 Bước** cực kỳ chi tiết, chỉ đích danh từng file cần sửa trong folder của bạn.

---

### GIẢI NGỐ: 4 file trong `best_model_c1` là cái gì?
Trước khi bắt đầu, giải thích nhanh về 4 file bạn thấy:
1. `model.safetensors`: Đây là "bộ não" đã học xong của AI (trọng số mô hình).
2. `config.json`: Cấu hình của bộ não (có bao nhiêu nơ-ron, phân mấy loại...).
3. `tokenizer.json` & `tokenizer_config.json`: "Từ điển" giúp máy tính dịch chữ tiếng Anh của bài báo thành các con số để đưa vào bộ não.
*(Bạn không cần mở hay sửa các file này, code Python sẽ tự động đọc chúng).*

---

### WORKFLOW THAY "MÁU GIẢ" BẰNG "MÁU THẬT"

#### BƯỚC 1: Lấy Model dự đoán trên toàn bộ bài báo (Tạo `structured_risk_events.csv`)
*Hiện tại, bạn mới chỉ train model, chứ chưa lấy model đó đi "đọc" 2.500 bài báo thực tế để xuất ra kết quả.*

*   **Vị trí:** Bạn cần tạo một folder mới tên `P3-10` (theo đúng thiết kế dự án nhưng mình thấy trong cây thư mục của bạn chưa có).
*   **Việc cần làm:** Bạn cần 1 script Python (gọi là `run_inference_all_news.py`) để làm 3 việc:
    1. Đọc file `0. news data/final_supplychain_news_2015_2018.jsonl`.
    2. Cho `best_model_c1` đọc từng bài báo để dự đoán rủi ro (0, 1, 2) và điểm xác suất (probability).
    3. Trích xuất địa điểm (NER bằng SpaCy) và gán loại rủi ro (dùng `disruption_type.py` ở P3-08).
    4. Xuất ra file **`structured_risk_events.csv`**.
*   **LƯU Ý:** Vì bạn không thạo code và folder bạn chưa có file này, **hãy bảo mình, mình sẽ viết sẵn 100% code file `run_inference_all_news.py` cho bạn copy vào là chạy.**

#### BƯỚC 2: Rút máu giả ở khâu Mapping (Soft Join)
*Bây giờ đã có sự kiện rủi ro thật (file csv ở Bước 1), ta cần map nó với nhà cung cấp.*

*   **Vị trí:** Thư mục `P4-05`
*   **File cần sửa:** `soft_join_3d.py`
*   **Việc cần làm:** Mở file này ra bằng trình soạn thảo code (VS Code/Cursor). 
    *   Tìm đoạn code nào đang ghi là tạo mock data, random data, hoặc lưu ra file `soft_join_mock_output.parquet`. **Xóa hoặc comment (thêm dấu `#`) đoạn đó đi.**
    *   Sửa code để nó **đọc file `structured_risk_events.csv`** (vừa tạo ở Bước 1).
    *   Sửa tên file output xuất ra từ `soft_join_mock_output.parquet` thành `soft_join_real_output.parquet`.
*   **Chạy file:** Chạy lại file `soft_join_3d.py` này.

#### BƯỚC 3: Tạo lại Ma trận Đặc trưng (Feature Matrix)
*Dữ liệu map đã là thật, giờ phải update bảng tổng hợp.*

*   **Vị trí:** Thư mục `P5-01`
*   **File cần sửa:** `build_feature_matrix.py`
*   **Việc cần làm:** Mở file này ra, tìm chỗ nó đang đọc file `P4-05/soft_join_mock_output.parquet`, sửa chữ `mock` thành `real` (`P4-05/soft_join_real_output.parquet`).
*   **Chạy file:** Chạy lại `build_feature_matrix.py`. Nó sẽ đè lên file `feature_matrix.csv` cũ. Bảng dữ liệu của bạn lúc này 10 cột đã là data thật 100%.

#### BƯỚC 4: Chạy lại toàn bộ Model Machine Learning (Layer 3)
*Data thật đã sẵn sàng, giờ chỉ việc bấm nút cho các script chạy lại theo thứ tự để ra kết quả mới.*

Bạn vào từng folder và chạy các file sau (không cần sửa code, chỉ cần chạy lại để nó ăn data mới):
1.  **Vị trí `P5-08`:** Chạy `train_xgboost.py`. 
    *   *Hiệu ứng:* XGBoost sẽ học trên đặc trưng NLP thật. Bạn sẽ thấy file `xgb_results.json` cập nhật chỉ số AUC/F1 mới (chắc chắn sẽ cao hơn bản mock).
2.  **Vị trí `P5-09`:** Chạy `compare_models.py`. 
    *   *Hiệu ứng:* So sánh lại xem XGBoost xịn hơn Logistic Regression (Baseline) bao nhiêu phần trăm.
3.  **Vị trí `P5-10`:** Chạy `shap_analysis.py`.
    *   *Hiệu ứng:* Cập nhật file hình và csv. Lúc này bạn sẽ thấy đặc trưng NLP (như `news_risk_score`) trồi lên đóng góp vào model, chứ không nằm ở bét bảng (bằng 0) như bản mock nữa.
4.  **Vị trí `P5-11`:** Chạy `find_threshold.py`.
    *   *Hiệu ứng:* Tính lại ngưỡng cảnh báo tối ưu (Youden's J) dựa trên xác suất thật.
5.  **Vị trí `P5-12`:** Chạy `generate_alerts.py`.
    *   *Hiệu ứng:* Xuất ra danh sách cảnh báo hàng tuần thật.
6.  **Vị trí `P5-13`:** Chạy `lead_time_warning.py`.
    *   *Hiệu ứng:* Tính lại xem mô hình cảnh báo sớm được bao nhiêu tuần (LTW). Đây là con số quan trọng nhất để đi khè giám khảo.

#### BƯỚC 5: Lấp chỗ trống (Placeholder) trong Paper
*Mọi kết quả đã có, việc cuối cùng là viết báo cáo.*

*   **Vị trí:** Thư mục `P7-00_demo_paper`
*   **File cần mở:** `demo_full_paper_v1.md` và `paper_notes.md`
*   **Việc cần làm:** Mở file demo paper lên, `Ctrl + F` tìm chữ `<!-- PLACEHOLDER`. Bạn xem kết quả từ các file json vừa sinh ra ở Bước 4, thấy số nào thì gõ thay thế vào chỗ placeholder đó. Đoạn giải thích (thảo luận) tại sao XGBoost mock lại thấp hơn giờ có thể thêm dòng "Khi đưa data thật vào, AUC tăng lên X%, chứng tỏ tin tức có giá trị dự báo...".

---

### TÓM LẠI BẠN CẦN LÀM GÌ NGAY BÂY GIỜ?
Vì bạn "ngu code", mình khuyên bạn **ĐỪNG tự đụng vào code vội**. 
Hãy trả lời mình câu này: **Bạn đã có code để chạy Bước 1 chưa?** (Script gom model DistilBERT + SpaCy + Disruption type để chạy 2500 bài báo).

Nếu chưa có, hãy bảo mình: *"Viết cho tui code Bước 1 (P3-10) đi"* -> Mình sẽ viết sẵn cho bạn 1 file `.py`, bạn chỉ việc lưu vào máy và bấm "Run". Sau khi Bước 1 chạy xong ra file CSV, mình sẽ hướng dẫn tiếp Bước 2. Cứ đi từng bước một cho chắc ăn nhé!