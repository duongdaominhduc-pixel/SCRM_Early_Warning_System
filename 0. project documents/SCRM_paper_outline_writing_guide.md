# OUTLINE & WRITING GUIDE — Full Paper SCRM (NLP + ML Early Warning System)

> Tài liệu này được soạn sau khi khảo sát văn phong, cấu trúc và cách trình bày của các bài báo
> open-access cùng chủ đề (Supply Chain Risk Management + NLP + ML Early Warning), bao gồm:
> - Huang, S. (2025). *AI-Driven Early Warning Systems for Supply Chain Risk Detection: A Machine
>   Learning Approach.* Academic Journal of Computing & Information Science, 8(9), 92–107. (Francis
>   Academic Press, open access)
> - *Text-Driven Early Warning of Supply Chain Risks* (2026). International Journal of Advanced
>   Computer Science and Applications (IJACSA / TheSAI), Vol. 17, No. 1.
> - Various systematic literature reviews trên ScienceDirect, Emerald, Taylor & Francis về SCRM + AI/ML.
>
> Claude Code dùng file này làm khung sườn khi viết bản demo full paper. Mọi placeholder dạng
> `[FILL: ...]` cần được Claude Code điền dựa trên kết quả thực tế của pipeline (số liệu, dataset,
> kết quả model...) khi đã có. Trước khi có đủ số liệu thật, Claude Code có thể điền giá trị giả định
> hợp lý và ghi chú rõ `[PLACEHOLDER — cần thay bằng số liệu thật sau khi fine-tune/train xong]`.

---

## PHẦN A — NHẬN XÉT VỀ VĂN PHONG & CẤU TRÚC CỦA CÁC BÀI THAM KHẢO

### A.1 Cấu trúc tổng thể (IMRaD mở rộng)

Tất cả các bài đã khảo sát đều theo khung **IMRaD mở rộng**, không phải IMRaD thuần túy:

```
Title → Abstract (structured) → Keywords
  → 1. Introduction
  → 2. Literature Review / Related Work
  → 3. Methodology
  → 4. Experiments & Results
  → 5. Discussion (business value + limitations)
  → 6. Conclusion & Future Work
  → References
```

Điểm khác biệt so với IMRaD kinh điển: **Discussion tách biệt rõ với Results**, và phần Discussion luôn
có 1 sub-mục riêng nói về **giá trị thực tiễn/kinh doanh** (business value) — đặc trưng của paper ứng
dụng (applied research), không phải paper lý thuyết thuần.

### A.2 Văn phong (Style)

- **Abstract dạng structured, đậm số liệu**: Mọi abstract khảo sát đều nhồi số liệu cụ thể ngay trong
  đoạn tóm tắt — ví dụ "*92% accuracy, 94% AUC-ROC, 89% F1-score*", "*35% reduction in risk-related
  losses*". Không viết abstract chung chung kiểu "mô hình đạt hiệu suất tốt".
- **Câu mở đầu Introduction luôn là bối cảnh vĩ mô có dẫn chứng sự kiện thực tế** (COVID-19,
  Russia-Ukraine conflict, chip shortage...) rồi mới thu hẹp dần vào vấn đề nghiên cứu cụ thể — kỹ
  thuật "funnel" (rộng → hẹp).
- **Mỗi câu khẳng định gần như đều có citation [n]** ngay cả với câu mang tính hiển nhiên — thể hiện
  rigor học thuật, tránh unsupported claims.
- **Câu văn academic English chuẩn**: chủ yếu câu ghép phức (compound-complex), dùng nhiều danh động
  từ (nominalization: "implementation", "validation", "integration" thay vì động từ trực tiếp), giọng
  trung lập khách quan (third person, tránh "we believe", ưu tiên "this research demonstrates").
- **Bảng (Table) được dùng triệt để** để trình bày: data sources, model comparison, evaluation metrics,
  hyperparameters — không diễn giải bằng văn xuôi những gì có thể bảng hóa được.
- **Method luôn có sub-section riêng cho từng thành phần kỹ thuật** (data collection, preprocessing,
  model selection, validation strategy) — không gộp chung thành 1 đoạn dài.
- **Limitations được viết thẳng thắn, không né tránh** — thường nằm cuối Discussion hoặc đầu
  Conclusion, liệt kê rõ giới hạn về data, generalization, scope.

### A.3 Những điểm format có thể áp dụng trực tiếp cho paper của nhóm

| Đặc điểm quan sát được | Áp dụng vào paper SCRM của nhóm |
|---|---|
| Abstract nhồi số liệu cụ thể | FRS đạt range nào, Macro F1 Classifier C1 bao nhiêu, AUC-ROC model chính bao nhiêu, cải thiện % so với Ablation/Baseline |
| Bối cảnh mở đầu bằng sự kiện thực tế | Mở đầu Introduction bằng chip shortage 2021, hoặc gián đoạn cảng biển — phù hợp scope Electronics |
| Bảng so sánh nghiên cứu liên quan (Related Work Table) | Nhóm đã có sẵn bảng "Tính mới" (NLP từ News / DL Vận hành / Multi-source Fusion / Entity-to-Ops Mapping / ML Risk Score) — dùng nguyên bảng này trong Literature Review |
| Sub-section riêng cho từng layer kỹ thuật | Giữ đúng cấu trúc 3 Lớp (NLP Layer / Mapping Layer / Intelligence Layer) làm 3 sub-section của Methodology |
| Business Value section riêng | Dùng TTS actionable thresholds (TTS<7 ngày → khẩn cấp...) làm nội dung chính cho mục Business Value |
| Limitations thẳng thắn | Ghi rõ: entity resolution tier-2 company limitation, dataset operational là gì, scope chỉ Electronics |

---

## PHẦN B — OUTLINE HOÀN CHỈNH CHO PAPER

```
TITLE
[FILL: tên đề tài đã chốt — PHẢI phản ánh đúng bản chất inbound/inventory risk,
không dùng tên cũ nếu tên cũ còn neo theo hướng outbound/delivery delay]

ABSTRACT (200–250 từ, structured, có số liệu)
- Câu 1–2: Bối cảnh + vấn đề (supply chain ngày càng dễ tổn thương trước rủi ro thượng nguồn)
- Câu 3: Gap nghiên cứu (thiếu hệ thống tích hợp NLP + dữ liệu vận hành nội bộ cho inbound risk)
- Câu 4–5: Phương pháp (kiến trúc 3 lớp, Pseudo-labeling, 3D Soft Join, FRS)
- Câu 6–8: Kết quả chính kèm SỐ LIỆU CỤ THỂ (Macro F1, AUC-ROC, % cải thiện so với baseline/ablation)
- Câu cuối: Đóng góp + ứng dụng thực tiễn

KEYWORDS (5–8 từ khóa)
Supply Chain Risk Management; Natural Language Processing; Machine Learning; Early Warning System;
Inventory Risk; Named Entity Recognition; Pseudo-labeling; Composite Risk Score

────────────────────────────────────────
1. INTRODUCTION
────────────────────────────────────────
1.1 Bối cảnh (Background)
   - Mở bằng sự kiện thực tế: gián đoạn nguồn cung ngành Electronics (chip shortage, động đất Đài
     Loan, đình công cảng...) — có citation
   - Funnel: từ vĩ mô (global supply chain vulnerability) → cụ thể (inbound material risk cho
     Electronics manufacturing)

1.2 Vấn đề nghiên cứu (Problem Statement)
   - Doanh nghiệp thiếu khả năng phát hiện sớm rủi ro nguồn cung trước khi nó biểu hiện thành
     thiếu hụt tồn kho thực tế
   - Phương pháp truyền thống (rule-based, manual monitoring) phản ứng chậm, không tận dụng được
     tín hiệu sớm từ tin tức công khai

1.3 Khoảng trống nghiên cứu (Research Gap)
   - Dẫn bảng so sánh (NLP từ News / DL Vận hành / Multi-source Fusion / Entity-to-Ops Mapping /
     ML Risk Score) — nêu rõ chưa ai làm đủ cả 5 cột cùng lúc

1.4 Mục tiêu & Đóng góp nghiên cứu (Objectives & Contributions)
   - Liệt kê dạng số: (1) Multi-source data fusion..., (2) 3D Soft Join entity-to-ops mapping...,
     (3) Interpretable composite risk score...

1.5 Cấu trúc bài báo (Paper Organization)
   - 1 đoạn ngắn map từng phần còn lại

────────────────────────────────────────
2. LITERATURE REVIEW
────────────────────────────────────────
2.1 Supply Chain Risk Management: Khung lý thuyết
   - SCRM truyền thống vs khung hiện đại có AI hỗ trợ
   - Phân biệt risk identification / risk assessment / risk monitoring (theo các SLR đã đọc)

2.2 NLP trong phát hiện rủi ro từ văn bản phi cấu trúc
   - Text mining, event extraction, NER cho domain supply chain
   - Hạn chế của sentiment analysis trong domain này (dẫn lại lý do nhóm KHÔNG dùng sentiment model)

2.3 Machine Learning cho dự báo rủi ro chuỗi cung ứng
   - Các thuật toán phổ biến (XGBoost, Random Forest, LSTM) và ứng dụng trong các nghiên cứu trước
   - Vấn đề walk-forward validation / time-series leakage trong các nghiên cứu trước

2.4 Khoảng trống nghiên cứu & Định vị đóng góp
   - Bảng so sánh chi tiết (dùng lại bảng "Tính mới" đã có)
   - Khẳng định rõ 3 đóng góp cốt lõi của đề tài

────────────────────────────────────────
3. METHODOLOGY
────────────────────────────────────────
3.1 Tổng quan kiến trúc hệ thống (System Architecture Overview)
   - Sơ đồ kiến trúc 3 lớp tổng thể (mô tả bằng văn xuôi + tham chiếu Figure)
   - Bảng tổng hợp: Lớp | Nhiệm vụ | Output chính

3.2 Thu thập & Tiền xử lý dữ liệu (Data Collection & Preprocessing)
   3.2.1 Dữ liệu vận hành nội bộ — [FILL: tên dataset mới, nguồn, schema, granularity]
   3.2.2 Dữ liệu tin tức — whitelist nguồn, GDELT BigQuery / NewsAPI, tiêu chí CLEAN, dedup

3.3 Lớp 1 — NLP Layer
   3.3.1 Gán nhãn bán giám sát (Semi-supervised Labeling): Fleiss Kappa, Pseudo-labeling pipeline
   3.3.2 Fine-tuning DistilBERT Classifier C1 — kiến trúc, hyperparameters, lý do chọn DistilBERT
   3.3.3 Named Entity Recognition — model, post-processing, country normalization
   3.3.4 Disruption Type Classification — rule-based, lý do không dùng ML
   3.3.5 Initial Severity Score — công thức EV-Severity, lý do không dùng sentiment model

3.4 Lớp 2 — Mapping Layer
   3.4.1 Vấn đề Granularity Mismatch & giải pháp 3D Soft Join (T × G × C)
   3.4.2 Mô hình SWIP (Sawtooth Wave Inventory Pattern) — công thức burn_rate, TTS
   3.4.3 Nguyên tắc chống Data Leakage (shift(1), walk-forward)

3.5 Lớp 3 — Intelligence Layer
   3.5.1 Feature Matrix X — observation unit, 17 features, target variable definition
   3.5.2 Model Selection & Justification — tại sao chọn 4 mô hình test, Baseline vs Ablation vs Main
   3.5.3 Walk-forward Validation Strategy
   3.5.4 Final Risk Score (FRS) Formula — công thức, hyperparameter, sensitivity test

3.6 Đánh giá mô hình (Evaluation Metrics)
   - Bảng tổng hợp toàn bộ metric dùng ở từng layer (Macro F1, Fleiss/Cohen's Kappa, AUC-ROC,
     Precision/Recall, RMSE nếu có)

────────────────────────────────────────
4. EXPERIMENTS & RESULTS
────────────────────────────────────────
4.1 Mô tả dữ liệu thực nghiệm (Experimental Data Description)
   - Số liệu cụ thể: số bài báo, số đơn hàng/dòng dữ liệu vận hành, khoảng thời gian, % sau lọc

4.2 Kết quả Lớp 1 — NLP Layer
   - Bảng: Macro F1, Cohen's Kappa, confusion matrix, NER coverage rate
   - [PLACEHOLDER — điền sau khi fine-tune DistilBERT xong]

4.3 Kết quả Lớp 2 — Mapping Layer
   - Match rate (event-level, order-level), precision spot-check

4.4 Kết quả Lớp 3 — So sánh Baseline vs Ablation vs Main Model
   - Bảng so sánh đầy đủ AUC-ROC / Macro F1 / Precision / Recall qua 5 folds walk-forward
   - Biểu đồ/feature importance (SHAP) chứng minh đóng góp của NLP features

4.5 Phân tích Final Risk Score (FRS)
   - Phân phối FRS theo mức LOW/MEDIUM/HIGH/CRITICAL
   - Kết quả sensitivity test trọng số

────────────────────────────────────────
5. DISCUSSION
────────────────────────────────────────
5.1 Diễn giải kết quả chính (Interpretation of Key Findings)
   - NLP features đóng góp bao nhiêu % vào hiệu suất dự báo so với chỉ dùng dữ liệu vận hành

5.2 Giá trị thực tiễn (Business Value & Practical Implications)
   - TTS actionable: ngưỡng hành động cụ thể
   - Khả năng tích hợp vào dashboard doanh nghiệp mà không cần đổi hệ thống ERP

5.3 Khả năng mở rộng (Scalability & Generalizability)
   - Mở rộng sang category khác, thị trường khác

5.4 Giới hạn nghiên cứu (Limitations)
   - Entity resolution tier-2 company (không map được tên công ty cụ thể)
   - Quy mô dữ liệu, khoảng thời gian giới hạn
   - Reverse-engineered inventory proxy (SWIP) thay vì dữ liệu tồn kho thực

────────────────────────────────────────
6. CONCLUSION & FUTURE WORK
────────────────────────────────────────
- Tóm tắt đóng góp cốt lõi (không lặp lại y nguyên Abstract, diễn đạt lại)
- Future Work: mở rộng entity resolution bằng LLM function calling, thêm dữ liệu thời tiết/vĩ mô,
  tích hợp dashboard thời gian thực

────────────────────────────────────────
REFERENCES
────────────────────────────────────────
[FILL: theo format chuẩn của journal mục tiêu — APA hoặc IEEE tùy nơi nộp]
```

---

## PHẦN C — WRITING GUIDE CHI TIẾT (Hướng dẫn diễn giải cho Claude Code)

### C.1 Nguyên tắc viết Abstract

- Bắt buộc có **ít nhất 3 con số cụ thể** trong abstract (không được viết "kết quả tốt", "hiệu suất cao").
- Câu cuối abstract phải nêu rõ **đóng góp + use-case thực tế**, không kết bằng câu chung chung.
- Độ dài 200–250 từ, 1 đoạn duy nhất (không xuống dòng).

### C.2 Nguyên tắc viết Introduction

- Đoạn mở đầu **không được bắt đầu bằng định nghĩa khô khan** ("Supply chain risk management is..."),
  mà bắt đầu bằng 1 sự kiện/số liệu thực tế gây ấn tượng.
- Mỗi đoạn Introduction nên có **độ dài 4–7 câu**, không quá ngắn (rời rạc) hay quá dài (khó theo dõi).
- Research Gap phải được trình bày bằng **bảng so sánh**, không chỉ bằng văn xuôi.
- Contribution list nên đánh số **(1), (2), (3)** rõ ràng, mỗi đóng góp 1–2 câu.

### C.3 Nguyên tắc viết Methodology

- **Mỗi formula phải có giải thích từng biến ngay sau công thức** — không để công thức trơ trọi.
- Khi nêu một quyết định thiết kế (ví dụ: "không dùng sentiment model", "chọn DistilBERT thay BERT"),
  **luôn phải có đoạn justify ngắn** theo cấu trúc: vấn đề → tại sao cách khác không phù hợp → giải
  pháp được chọn → lý do (tối thiểu 2 lý do).
- Pseudocode hoặc sơ đồ luồng (flow) nên được mô tả bằng **văn xuôi tuần tự kết hợp Figure reference**,
  không dán nguyên code Python vào paper.
- Bất kỳ ngưỡng/hyperparameter nào (κ ≥ 0.70, confidence ≥ 0.80...) đều phải có **cơ sở lựa chọn**
  (citation hoặc lý giải domain-specific), không để con số "từ trên trời rơi xuống".

### C.4 Nguyên tắc viết Results

- **Không diễn giải lại số liệu đã có trong bảng bằng văn xuôi dài dòng** — chỉ nêu insight chính từ
  bảng, để bảng tự nói phần chi tiết.
- Khi so sánh Baseline vs Ablation vs Main, câu kết luận phải định lượng: *"Main model cải thiện X%
  AUC-ROC so với Ablation, chứng minh đóng góp của NLP features là Y điểm phần trăm."*
- Nếu dùng giá trị PLACEHOLDER (chưa có số liệu thật), **bắt buộc đánh dấu rõ** bằng comment
  `<!-- PLACEHOLDER: cần thay bằng kết quả thật từ P3-04/P3-08/P5-09 -->` ngay cạnh bảng/số liệu đó.

### C.5 Nguyên tắc viết Discussion & Limitations

- Limitations phải viết **thẳng thắn, cụ thể**, không né tránh bằng ngôn ngữ mơ hồ. Ví dụ đúng:
  *"The system cannot resolve tier-2 supplier entities (e.g., component-level manufacturers) due to
  the absence of such granularity in the operational dataset, representing a scope limitation rather
  than a methodological flaw."*
- Business Value section nên có **ít nhất 1 bảng hành động cụ thể** (ví dụ bảng ngưỡng TTS → hành
  động đề xuất).

### C.6 Quy tắc văn phong chung

| Quy tắc | Ví dụ SAI | Ví dụ ĐÚNG |
|---|---|---|
| Tránh first-person số ít | "I think the model performs well" | "The model demonstrates strong performance" |
| Định lượng thay vì định tính mơ hồ | "significantly better" | "improves AUC-ROC by 8.3 percentage points" |
| Câu chủ động vừa phải, không lạm dụng passive | "It was decided that..." | "The research team selected... because..." |
| Mỗi claim cần citation hoặc số liệu | "NLP improves SCRM" | "NLP-derived severity signals improve SCRM forecasting accuracy by X% [citation]" |
| Thuật ngữ kỹ thuật giữ tiếng Anh, không dịch nửa vời | "mô hình BERT đã được fine-tune" trong bản tiếng Anh | giữ nguyên "fine-tuned BERT model" |

### C.7 Quy trình điền Placeholder khi paper được viết TRƯỚC khi có kết quả thật

1. Viết toàn bộ cấu trúc, văn phong, bảng biểu HOÀN CHỈNH như outline trên.
2. Với mọi con số thực nghiệm chưa có (do đang fine-tune), điền giá trị **giả định hợp lý** dựa trên
   range mục tiêu đã đặt ra trong PCCV (ví dụ Macro F1 mục tiêu ≥ 0.72 → điền 0.74 làm demo).
3. Đánh dấu rõ bằng `<!-- PLACEHOLDER -->` ngay sau mỗi con số/bảng dùng giá trị giả định.
4. Khi có kết quả thật (sau khi fine-tune xong, sau khi chạy walk-forward xong...), chỉ cần search
   các comment PLACEHOLDER và thay số liệu — không cần viết lại cấu trúc câu.

---

## PHẦN D — DANH SÁCH FIGURE/TABLE CẦN CÓ (để Claude Code chuẩn bị sườn)

| # | Loại | Tên | Vị trí |
|---|---|---|---|
| Table 1 | Bảng | Related Work Comparison (Tính mới) | Section 2.4 |
| Figure 1 | Sơ đồ | System Architecture Overview (3 lớp) | Section 3.1 |
| Table 2 | Bảng | Layer Summary (Lớp / Nhiệm vụ / Output) | Section 3.1 |
| Table 3 | Bảng | Feature Matrix X Schema (17 features, 5 nhóm) | Section 3.5.1 |
| Table 4 | Bảng | Evaluation Metrics Summary toàn hệ thống | Section 3.6 |
| Table 5 | Bảng | Classifier C1 Results (Macro F1, Kappa, Confusion Matrix) | Section 4.2 |
| Table 6 | Bảng | Mapping Layer QA Results (match rate, precision) | Section 4.3 |
| Table 7 | Bảng | Baseline vs Ablation vs Main Comparison | Section 4.4 |
| Figure 2 | Biểu đồ | SHAP Feature Importance | Section 4.4 |
| Figure 3 | Biểu đồ | FRS Distribution by Risk Level | Section 4.5 |
| Table 8 | Bảng | TTS Action Threshold Table | Section 5.2 |

---

## PHẦN E — GHI CHÚ QUAN TRỌNG VỀ HƯỚNG ĐỀ TÀI

> Khi viết paper, KHÔNG bám cứng vào tên đề tài/mô tả cũ nếu nó còn phản ánh hướng **outbound logistics
> / delivery delay** (kiểu DataCo, Late_delivery_risk). Bản chất đúng của đề tài là **inbound risk /
> inventory stockout risk** — rủi ro từ phía nhà cung cấp/nguyên vật liệu đầu vào. Toàn bộ phần
> Introduction, Problem Statement, và bất kỳ chỗ nào mô tả "vấn đề nghiên cứu" đều phải nhất quán theo
> hướng inbound này. Nếu phát hiện mâu thuẫn giữa file dữ liệu/code thực tế và outline này, ưu tiên
> theo dữ liệu/code thực tế và ghi chú lại sai lệch đó.
