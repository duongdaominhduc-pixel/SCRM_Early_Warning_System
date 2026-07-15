# Quyết định Thiết kế: Thứ tự Ngẫu nhiên trong Gán nhãn Thủ công (P0-04)

> **Tài liệu**: Design Decision #01 — P0-04 Batch Labeling Order  
> **Ngày**: 2026-06-30  
> **Kết luận**: Dùng **random shuffle** thay vì chronological order  

---

## 1. Bối cảnh

Trong task P0-04, mỗi thành viên gán nhãn độc lập **540 bài báo khác nhau** (không overlap) từ tập tin tức 2022–2024 do nhóm tự crawl. Câu hỏi đặt ra: nên sắp xếp 540 bài đó **theo thứ tự ngẫu nhiên** hay **theo thứ tự thời gian (chronological)**?

---

## 2. So sánh hai phương án

### Phương án A — Chronological Order (sắp xếp theo ngày đăng)

**Ưu điểm:**
- Annotator hiểu được bối cảnh thời sự của từng giai đoạn → phán đoán tự nhiên hơn
- Dễ phát hiện bài trùng ý về cùng sự kiện (các bài gần nhau về thời gian)
- Quy trình gán nhãn trực quan hơn

**Nhược điểm:**
- **Temporal Context Bias**: Annotator biết mình đang đọc bài từ giai đoạn "COVID logistics shock Q1/2022" hoặc "Ukraine war Q2/2022" → xu hướng gán HIGH_RISK nhiều hơn mức nội dung thực sự của bài đó thể hiện. Nhãn bị phụ thuộc vào *context bên ngoài bài* thay vì *nội dung của bài*.
- **Sequential Streak Bias**: Khi các bài từ cùng một giai đoạn rủi ro cao cụm lại, annotator đọc 10–15 bài HIGH_RISK liên tiếp → bài kế tiếp có xu hướng bị gán nhãn cao hơn thực tế do quán tính tâm lý (*anchoring effect*).
- **Không phát hiện được bias**: Trong P0-04, mỗi người gán bộ bài riêng, không có cơ chế Kappa check chéo giữa các annotators. Nếu một thành viên bị temporal bias suốt 540 bài của mình, không có cách nào phát hiện ra.

---

### Phương án B — Random Shuffle ✅ (được chọn)

**Ưu điểm:**
- **Loại trừ temporal context bias**: Annotator chỉ dựa vào nội dung bài để gán nhãn, không bị ảnh hưởng bởi "đây là giai đoạn nào". Đây là nguyên tắc cốt lõi trong annotation: *nhãn phải xuất phát từ text, không phải từ metadata*.
- **Loại trừ sequential streak bias**: Phân bố nhãn 0/1/2 trải đều hơn trong luồng đọc → annotator không bị kéo theo một pattern liên tiếp.
- **Chuẩn mực NLP annotation**: SQuAD (Rajpurkar et al., 2016), SNLI (Bowman et al., 2015), CoNLL-2003 đều dùng random order khi thu thập nhãn từ human annotators.
- **Consistency với Pilot (P0-03)**: Pilot 149 bài cũng dùng random order → đảm bảo cùng methodology xuyên suốt.

**Nhược điểm:**
- Annotator mất ngữ cảnh thời sự → phải tự phán đoán từ nội dung bài
- Khó phát hiện bài trùng ý về cùng sự kiện

---

## 3. Tại sao nhược điểm của Random không đáng lo trong dự án này

### 3.1 — Tập tin tức đã dedup, bài trùng ý gần như không còn

Pipeline làm sạch đã áp dụng **semantic deduplication** (TF-IDF cosine ≥ 0.85), loại bỏ toàn bộ bài viết lại cùng nội dung. Lợi thế lớn nhất của chronological — dễ phát hiện bài trùng — **đã không còn tác dụng**.

### 3.2 — Annotators đã calibrate tốt, không cần context để phán đoán

Sau 4 vòng pilot với κ = 0.785 (Substantial agreement) và bộ **LABELING_GUIDE_v3.md** (9 quy tắc QT-01..QT-09), các thành viên đã được chuẩn hóa khả năng phán đoán từ **nội dung bài**. Cụ thể, guide yêu cầu:
> *"Gán nhãn dựa trên những gì bài báo NÓI, không phải những gì bạn BIẾT đã xảy ra trong giai đoạn đó."*

Đây chính xác là lý do random order phát huy tác dụng: buộc annotator bám vào text.

### 3.3 — Không có cơ chế phát hiện bias trong batch labeling

Khác với pilot (tất cả 4 người gán cùng 149 bài → có thể tính Kappa), trong batch mỗi người gán 540 bài riêng. **Không có cross-check giữa các annotators.** Điều này có nghĩa: nếu temporal bias xuất hiện ở một người, nó sẽ lan vào toàn bộ 540 nhãn của người đó mà không ai phát hiện được. Random order là biện pháp phòng ngừa duy nhất khả dụng.

---

## 4. Cơ sở học thuật

| Tài liệu | Phương pháp | Kết luận liên quan |
|---|---|---|
| Artstein & Poesio (2008) — *Inter-Coder Agreement for Computational Linguistics* | Random order trong annotation | Random order reduces systematic order effects in human annotation |
| Bayerl & Paul (2011) — *What Determines Inter-Coder Agreement?* | Meta-analysis 93 annotation studies | Sequential bias là mối đe dọa có tài liệu với annotation chất lượng |
| Rajpurkar et al. (2016) — SQuAD | Random order | Standard practice: articles presented in random order to crowd workers |
| FinNLP 2024 — Financial NLP Shared Task | Random order | Risk classification tasks use random order to prevent temporal anchoring |

---

## 5. Kết luận

**Random shuffle được chọn** vì:

1. Loại trừ temporal context bias và sequential streak bias — hai rủi ro thực tế với tập tin tức có tính thời sự cao
2. Tập tin tức đã dedup → lợi thế của chronological không còn
3. Annotators đã calibrate tốt qua pilot → không cần context thời sự để phán đoán
4. Không có cơ chế cross-check trong batch → random là biện pháp phòng ngừa duy nhất
5. Đúng chuẩn NLP annotation (SQuAD, SNLI, FinNLP 2024)

**Đoạn viết sẵn cho paper (P7-02 — Methodology):**
> *"To prevent temporal context bias and sequential anchoring effects — both documented threats in time-sensitive news annotation (Artstein & Poesio, 2008; Bayerl & Paul, 2011) — articles within each annotator's batch were presented in random order (seed=42), consistent with standard NLP annotation practice (Rajpurkar et al., 2016; FinNLP 2024)."*

---

*Design Decision #01 | P0-04 | 2026-06-30*
