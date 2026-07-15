# P0-04: Gán nhãn Bán giám sát (Pseudo-Labeling) & Hậu kiểm Đa tầng

## Mục tiêu
Nhiệm vụ này áp dụng học bán giám sát (semi-supervised learning) để giải quyết vấn đề thiếu hụt dữ liệu gán nhãn trong lĩnh vực SCRM. Chúng tôi sử dụng một mô hình DistilBERT đã được tinh chỉnh (fine-tuned) để mở rộng các nhãn "Tiêu chuẩn Vàng" lên một kho dữ liệu lớn chưa gán nhãn (khoảng 5.000 bài báo), theo sau là một quá trình lọc và hậu kiểm (refinement) cực kỳ nghiêm ngặt.

## Phương pháp luận & Tính Khoa học
*   **Kiến trúc Mô hình:** Mô hình `distilbert-base-uncased` được tinh chỉnh trên tập dữ liệu Gold bằng chiến lược **Thích ứng Miền Bảo thủ** (Conservative Domain Adaptation).
*   **Hệ thống Lọc nhiễu (Noise-Reduction Gateway):** Để ngăn chặn hiện tượng lan truyền sai số (error propagation) và thiên kiến xác nhận, chúng tôi áp dụng **Chiến lược Hậu kiểm Đa tầng**:
    *   **Ngưỡng Tin cậy (Threshold) Độc lập:** Tối ưu hóa bằng thuật toán Grid Search để tìm ra ngưỡng vàng: **0.87 (Nhãn 1)** và **0.88 (Nhãn 2)**.
    *   **Lọc Heuristic:** Áp dụng các luật về ngữ cảnh và thời gian để loại bỏ các bản tin cũ, lỗi thời (không còn mang tính cảnh báo rủi ro).
    *   **Xác minh Thực thể (Entity Verification):** Sử dụng **spaCy NER** để đảm bảo các sự kiện rủi ro phải được gắn liền với một thực thể công nghiệp thực tế.
*   **Kiểm định Chất lượng:** Chúng tôi đạt được **Cohen’s Kappa là 0.6553** khi đối chiếu ngẫu nhiên nhãn của Máy với Chuyên gia, thỏa mãn hoàn toàn tiêu chuẩn "Sự đồng thuận từ Khá đến Đáng kể" cho các tác vụ tăng cường dữ liệu quy mô lớn.
*   **Tập Dữ liệu Cuối cùng:** Kho dữ liệu kết quả là sự kết hợp của **2.309 bài gán nhãn tay (Gold)** và **3.004 bài máy gán đã qua hậu kiểm (Refined Pseudo-labels)** (Tổng N = 5.313 bài).

## Cấu trúc Thư mục
- `output/`: Chứa tập dữ liệu tăng cường cuối cùng (`pseudo_labeled_refined.csv`), tập dữ liệu chuẩn con người gán (`manual_combined_2309.csv`), các báo cáo kiểm định Cohen's Kappa, hình ảnh minh chứng quá trình huấn luyện mô hình, và trọng số của mô hình DistilBERT tốt nhất (`distilbert-scrm-risk/`).
- `pipeline_data/`: Chứa kho tin tức khổng lồ chưa gán nhãn (`unlabeled_news_5040.csv`), kết quả gán thô ban đầu (`pseudo_labeled_5040.csv`) và các file chia task cho thành viên.
- `scripts/`: Chứa notebook huấn luyện chính (`*.ipynb`), code trích xuất dữ liệu thô (`extract_unlabeled.py`) và code gộp nhãn tay (`merge_labels.py`).
- `archive/`: Chứa các bản nháp, các lần thử nghiệm gán nhãn với ngưỡng (threshold) thấp, và code bỏ đi.
- `COLAB_DISTILBERT_GUIDE.md`: Tài liệu cốt lõi hướng dẫn chi tiết các bước huấn luyện và dự đoán của mô hình trên Google Colab.

## Hướng dẫn Chạy lại (Reproduction)
1.  Chạy file `scripts/extract_unlabeled.py` để chuẩn bị kho dữ liệu thô chưa gán nhãn.
2.  Làm theo hướng dẫn trong `COLAB_DISTILBERT_GUIDE.md` để tinh chỉnh mô hình, chạy suy luận (inference), và áp dụng luật lọc nhiễu + Threshold tối ưu trên Colab.
3.  Tải file CSV tinh khiết và Mô hình DistilBERT thu được bỏ vào thư mục `output/`.
4.  Chạy file `scripts/merge_labels.py` để hợp nhất với các nhãn gán tay.
