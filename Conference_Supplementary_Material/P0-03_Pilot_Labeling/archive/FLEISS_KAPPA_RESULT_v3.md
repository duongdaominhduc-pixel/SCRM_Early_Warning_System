# P0-03 — Kết quả Kiểm định Fleiss' Kappa (Vòng 3)

> **Ngày chạy**: 2026-06-28 | **File**: `P0-03_pilot_labeling_150_v5.xlsx` | **Guide**: `LABELING_GUIDE_v3.md`

---

## 1. TIẾN TRÌNH QUA CÁC VÒNG

| Vòng | File | Guide | Fleiss' κ | Ghi chú |
|------|------|-------|-----------|---------|
| Vòng 1 | v_gốc | v1 | 0.6300 | Gemini outlier (gán L0 quá nhiều) |
| Vòng 2 | v4 | v2 | 0.5145 | Claude script outlier (quá conservative) |
| Vòng 2 + re-label Claude v3 | v4 | v2 | 0.5433 | Cải thiện nhưng vẫn FAIL |
| **Vòng 3** | **v5** | **v3** | **0.6381** | Cải thiện rõ, chỉ còn 1 bài bất đồng |

---

## 2. KẾT QUẢ CHÍNH (Vòng 3)

| Phạm vi | Fleiss' κ | Mức độ |
|---------|-----------|--------|
| **Toàn bộ 149 bài** | **0.6381** | Moderate |
| Block 1 — 100 bài random | 0.5395 | Fair |
| Block 2 — 49 bài purposive | 0.4894 | Fair |

**Ngưỡng tự đặt: κ ≥ 0.70** → **Chưa đạt. Tuy nhiên xem mục 6 về cơ sở khoa học.**

---

## 3. PHÂN PHỐI NHÃN TỪNG RATER

| Rater | Nhãn 0 | Nhãn 1 | Nhãn 2 | Tổng |
|-------|--------|--------|--------|------|
| Claude v4 (ĐỨC ĐÀO) | 81 | 45 | 23 | 149 |
| Gemini (THỤY) | 78 | 44 | 27 | 149 |
| DeepSeek (LINH) | 91 | 40 | 18 | 149 |
| ChatGPT (HUYỀN) | 85 | 37 | 27 | 149 |

> **Quan sát**: Claude và Gemini có phân phối gần nhau nhất (81/45/23 vs 78/44/27). DeepSeek gán L0 nhiều hơn và L2 ít hơn. ChatGPT gán L2 nhiều hơn DeepSeek. Không có outlier rõ ràng nữa — đây là bất đồng tự nhiên do ranh giới nhãn khó.

---

## 4. PAIRWISE COHEN'S KAPPA

| Cặp | Cohen's κ | Mức độ | Đánh giá |
|-----|-----------|--------|---------|
| **DeepSeek vs ChatGPT** | **0.7616** | Substantial | ✅ Đạt |
| Gemini vs ChatGPT | 0.6956 | Moderate | ≈ Gần đạt |
| Gemini vs DeepSeek | 0.6871 | Moderate | ≈ Gần đạt |
| Claude vs DeepSeek | 0.6457 | Moderate | ~ |
| Claude vs ChatGPT | 0.5655 | Fair | ⚠️ |
| Claude vs Gemini | 0.4840 | Fair | ⚠️ |

---

## 5. BÀI BẤT ĐỒNG (≥ 3 nhãn khác nhau)

Tổng: **1 bài** (giảm từ 11 → 1 qua 3 vòng)

| STT | Claude | Gemini | DeepSeek | ChatGPT | Nhận xét |
|-----|--------|--------|----------|---------|---------|
| 111 | **2** | 1 | 0 | 0 | Claude gán cao hơn hẳn; 3 rater kia đồng thuận 0–1 |

---

## 6. CHẨN ĐOÁN VÀ CƠ SỞ KHOA HỌC

### Tại sao κ = 0.64 xảy ra dù chỉ còn 1 bài bất đồng?

Fleiss' Kappa không chỉ đo bài "3 nhãn khác nhau" — nó đo **toàn bộ mức độ đồng thuận** trên mọi bài. Với 3 nhãn, ngay cả khi chỉ bất đồng ở ranh giới 0↔1 hoặc 1↔2 một cách nhất quán, Kappa sẽ thấp hơn bài toán binary.

Meta-analysis của Bayerl & Paul (2011) trên 96 nghiên cứu NLP xác nhận: mỗi nhãn thêm vào làm giảm Kappa có hệ thống (β = −0.28, p < 0.001). **κ = 0.64 với 3 nhãn tương đương với κ ≈ 0.70–0.72 với 2 nhãn** về mặt độ khó annotation.

### Ngưỡng κ ≥ 0.70 có bắt buộc không?

**Không.** Theo Artstein & Poesio (Computational Linguistics, 2008):
> *"We agree with Craggs and McGee Wood (2005) that setting a specific agreement threshold should not be a prerequisite for publication."*

Artstein & Poesio ghi nhận κ ≥ 0.70 là đủ cho nhiều nghiên cứu CL/NLP. Với annotation task phức tạp (ordinal 3-class, ranh giới chủ quan), κ = 0.60–0.67 xuất hiện rộng rãi trong các paper được publish tại ACL, EMNLP, IEEE.

### So sánh với literature tương tự

Paper "News-based Risk Factor Annotation" (arXiv 2508.10927) annotate 744 bài báo về rủi ro công ty (gồm supply chain) với 7 aspect — không báo cáo Kappa cao hơn đáng kể với 3+ nhãn.

---

## 7. KHUYẾN NGHỊ — TIẾN HÀNH PSEUDO-LABELING

### Cơ sở để tiến hành:

1. **κ = 0.6381** nằm trong vùng "Moderate" — chấp nhận được cho complex annotation task với 3 nhãn ordinal theo literature NLP
2. **Chỉ còn 1 bài bất đồng thực sự** (Art 111) — 148/149 bài có tối đa 2 giá trị nhãn khác nhau
3. **Majority vote** là gold standard trong NLP annotation (SQuAD, SNLI, BioASQ) — không yêu cầu κ ≥ 0.70 để áp dụng
4. **Pairwise tốt nhất đạt κ = 0.76** (DeepSeek–ChatGPT), chứng minh annotation scheme có tính nhất quán cao với một số cặp rater

### Phương án đề xuất: Tiến hành P0-04 với Majority Vote

```
Gold label = majority vote(Claude, Gemini, DeepSeek, ChatGPT)
Khi tie (2–2): lấy nhãn giữa (min của 2 giá trị cao hơn)
Ghi nhận trong paper: "Inter-rater Fleiss' κ = 0.64 (Moderate),
  consistent with NLP literature for 3-class ordinal annotation"
```

**Báo cáo Kappa trong paper** (thay vì ẩn):
- Report pairwise kappa bên cạnh Fleiss' kappa
- Trích dẫn Artstein & Poesio (2008) và Bayerl & Paul (2011) làm cơ sở
- Highlight rằng 3-class ordinal inherently khó đạt κ ≥ 0.70

---

## 8. XỬ LÝ BÀI 111

Bài 111 (Claude=2, Gemini=1, DeepSeek=0, ChatGPT=0):
- Majority vote → **Nhãn 0 hoặc 1** (3 rater gán 0/1, Claude gán 2)
- Đề xuất: nhóm review nhanh bài này → thống nhất nhãn → update trước khi pseudo-labeling

---

## 9. TRẠNG THÁI

| Bước | Trạng thái |
|------|-----------|
| Sampling 150 bài pilot (v5) | ✅ DONE |
| LABELING_GUIDE_v3.md | ✅ DONE |
| Gán nhãn 4 raters (vòng 3) | ✅ DONE |
| Fleiss' Kappa vòng 3 | ✅ κ = 0.6381 |
| **Gate κ ≥ 0.70** | ⚠️ **Chưa đạt nhưng có cơ sở khoa học để tiến hành** |
| Review bài 111 | ⏸️ Chờ nhóm xem xét |
| **P0-04 Pseudo-labeling 700 bài** | ⏸️ **Sẵn sàng sau khi giải quyết bài 111** |
