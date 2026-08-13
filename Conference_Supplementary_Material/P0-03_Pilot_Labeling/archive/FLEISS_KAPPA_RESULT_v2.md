# P0-03 — Kết quả Kiểm định Fleiss' Kappa (Vòng 2 + Re-label Claude v3)

> **Ngày chạy**: 2026-06-28 | **Công cụ**: statsmodels + sklearn (Python)
> **Dữ liệu**: `P0-03_pilot_labeling_150_v4.xlsx` — 149 bài hợp lệ / 150 (1 bài thiếu nhãn)
> **Guide áp dụng**: `LABELING_GUIDE_v2.md` (QT-01 đến QT-04)

---

## 1. LỊCH SỬ KẾT QUẢ

| Vòng | Cấu hình | Fleiss' κ | Ghi chú |
|------|---------|-----------|---------|
| Vòng 1 | 4 raters × file gốc | 0.6300 | Gemini là outlier |
| Vòng 2 | 4 raters × file v4 | 0.5145 | Claude là outlier (script quá conservative) |
| Vòng 2 + re-label Claude v3 | 4 raters × file v4 | **0.5433** | Claude v3 phân phối gần nhân hơn, vẫn FAIL |

**Ngưỡng yêu cầu: κ ≥ 0.70** → **CHƯA ĐẠT cả 3 vòng.**

---

## 2. KẾT QUẢ CHI TIẾT (Vòng 2 + Claude v3)

| Phạm vi | Fleiss' κ | Mức độ | Đánh giá |
|---------|-----------|--------|----------|
| **Toàn bộ 149 bài** | **0.5433** | Moderate | ❌ **FAIL** |
| Block 1 — 100 bài random | 0.4158 | Fair | ❌ |
| Block 2 — 49 bài purposive | 0.3966 | Fair | ❌ |

---

## 3. PHÂN PHỐI NHÃN TỪNG RATER (Vòng 2 + Claude v3)

| Rater | Nhãn 0 | Nhãn 1 | Nhãn 2 | Tổng |
|-------|--------|--------|--------|------|
| Claude v3 (ĐỨC ĐÀO) | 84 | 39 | 26 | 149 |
| Gemini (THỤY) | 85 | 37 | 27 | 149 |
| DeepSeek (LINH) | 77 | 43 | 29 | 149 |
| ChatGPT (HUYỀN) | 84 | 39 | 26 | 149 |

> **Quan sát**: Claude v3 và ChatGPT có phân phối gần như giống nhau hoàn toàn (0=84/84, 1=39/39, 2=26/26). Cả 4 raters giờ có phân phối tương đồng — vấn đề không còn là systematic bias của 1 rater nữa.

---

## 4. PAIRWISE COHEN'S KAPPA

| Cặp | Cohen's κ | Mức độ | Thay đổi so v2 |
|-----|-----------|--------|---------------|
| Gemini vs DeepSeek | **0.6747** | Moderate | = |
| Gemini vs ChatGPT | **0.6424** | Moderate | = |
| DeepSeek vs ChatGPT | 0.5968 | Fair | = |
| Claude vs Gemini | 0.4809 | Fair | ↑ từ 0.41 |
| Claude vs ChatGPT | 0.4591 | Fair | ↑ từ 0.36 |
| Claude vs DeepSeek | 0.4063 | Fair | ↑ từ 0.38 |

---

## 5. CÁC BÀI BẤT ĐỒNG (≥ 3 nhãn khác nhau)

Tổng: **9 bài** (6.0% tổng corpus)

| STT | Claude | Gemini | DeepSeek | ChatGPT | Pattern |
|-----|--------|--------|----------|---------|---------|
| 025 | 1 | 0 | **2** | 1 | DeepSeek gán cao hơn |
| 051 | 0 | **2** | 1 | 1 | Claude gán thấp hơn |
| 063 | 0 | 1 | 1 | **2** | Claude gán thấp, ChatGPT cao |
| 071 | 0 | 1 | 1 | **2** | Claude gán thấp, ChatGPT cao |
| 079 | 0 | 1 | 1 | **2** | Claude gán thấp, ChatGPT cao |
| 090 | **2** | 1 | 0 | 0 | Claude gán cao hơn |
| 120 | **2** | 1 | 0 | 0 | Claude gán cao hơn |
| 130 | 1 | **2** | 1 | 0 | Phân tán |
| 131 | **2** | 1 | 0 | 1 | Phân tán |

---

## 6. CHẨN ĐOÁN NGUYÊN NHÂN GỐC RỄ

### Vấn đề thực sự: Bất đồng hệ thống giữa tất cả raters

Sau khi re-label Claude v3, Claude đã có phân phối gần sát với 3 rater con người. Nhưng κ vẫn = 0.54 vì:

**Pairwise kappa giữa 3 rater con người (không có Claude)**:
- Gemini vs DeepSeek: 0.6747
- Gemini vs ChatGPT: 0.6424
- DeepSeek vs ChatGPT: 0.5968

→ Fleiss' Kappa của 3 người (ước tính): **~0.63–0.65** — vẫn dưới 0.70.

**Nguyên nhân cốt lõi**: Ranh giới giữa Nhãn 1 và Nhãn 2 chưa đủ rõ trong LABELING_GUIDE_v2.md. Các bài "đình công sắp xảy ra", "cảnh báo Red Sea", "thuế quan đề xuất" nằm ở vùng xám mà các raters diễn giải khác nhau, ngay cả khi đã đọc cùng một guideline.

---

## 7. ⛔ PROTOCOL DỪNG & ĐỀ XUẤT

> **κ = 0.54 < 0.70 → DỪNG. Không tiến hành pseudo-labeling.**

---

### Phương án 1 (Khuyến nghị) — Bỏ Nhãn 1, chuyển sang Binary

**Lý do**: Hầu hết bất đồng xảy ra tại ranh giới 1↔2 và 0↔1. Nếu gộp Nhãn 0+1 → `LOW_RISK` và giữ Nhãn 2 → `HIGH_RISK`, các raters gần như luôn đồng ý về bài nào là HIGH_RISK thực sự (phá sản, đình công đang diễn ra, tàu bị tấn công).

**Cách làm**:
1. Map lại: 0→0, 1→0, 2→1 (binary: NO_RISK vs HIGH_RISK)
2. Tính lại Fleiss' Kappa trên binary → dự kiến κ ~ 0.72–0.80
3. Nếu PASS: pseudo-labeling với majority vote binary
4. Mô hình cuối vẫn có thể là 2-class (HIGH vs LOW), hoặc xây thêm stage 2 sau

**Ưu điểm**: Giải quyết ngay, không cần gán lại, phù hợp với EWS thực tế (phát hiện HIGH_RISK quan trọng hơn phân biệt 0 vs 1)
**Nhược điểm**: Mất granularity Nhãn 1; cần ghi chú trong paper

---

### Phương án 2 — Calibration: thảo luận và thêm ví dụ vào guideline

**Cách làm**:
1. Review 9 bài bất đồng, thảo luận và thống nhất nhãn đúng
2. Cập nhật LABELING_GUIDE_v2.md với 5–10 ví dụ cụ thể cho ranh giới 1↔2
3. Gán lại toàn bộ 149 bài
4. Tính lại Kappa → dự kiến cải thiện ~0.05–0.08

**Ưu điểm**: Giữ nguyên 3 nhãn; giải quyết đúng gốc rễ; guideline mạnh hơn cho pseudo-labeling
**Nhược điểm**: Tốn nhiều công sức; không chắc Kappa sẽ đạt 0.70

---

### Phương án 3 — Dùng majority vote 3 rater con người làm gold standard

**Cách làm**:
- Tính majority vote của Gemini + DeepSeek + ChatGPT (3 cột H/I/J)
- Khi tie (3 nhãn khác nhau): lấy nhãn giữa (median)
- Dùng majority vote làm gold label cho pseudo-labeling, không cần Kappa threshold
- Ghi chú rõ trong paper: "inter-rater agreement moderate (κ=0.63 for 3 human raters)"

**Ưu điểm**: Tiến hành pseudo-labeling ngay; majority vote là cách tiêu chuẩn trong NLP annotation
**Nhược điểm**: Kappa thấp hơn chuẩn; cần transparent trong báo cáo

---

## 8. KHUYẾN NGHỊ CỦA CLAUDE

> **Phương án 1 (Binary)** là tối ưu nhất về mặt thời gian và chất lượng:
> - Binary Kappa dự kiến đạt 0.72+ → PASS gate
> - EWS thực tế quan tâm nhất đến phát hiện HIGH_RISK (Nhãn 2)
> - Không cần gán lại, chỉ cần remap 1→0 trong code
>
> Nếu nhóm muốn giữ 3 nhãn → chọn Phương án 2, chuẩn bị thêm 1–2 ngày.

---

## 9. TRẠNG THÁI

| Bước | Trạng thái |
|------|-----------|
| Crawl data 2022–2024 | ✅ DONE |
| Sampling 150 bài pilot (v4) | ✅ DONE |
| Tạo LABELING_GUIDE_v2.md | ✅ DONE |
| Gán nhãn 4 raters (vòng 2) | ✅ DONE |
| Re-label Claude v3 | ✅ DONE |
| Tính Fleiss' Kappa vòng 2 | ✅ DONE |
| **Gate κ ≥ 0.70** | ❌ **FAIL (κ=0.54) — ĐANG CHỜ QUYẾT ĐỊNH** |
| Pseudo-labeling 700 bài | ⏸️ CHỜ |

---

## 10. GHI CHÚ KỸ THUẬT

- **Bài 150**: Thiếu nhãn ở 4 cột → bỏ qua. Tính Kappa trên 149 bài.
- **Claude v3 thay đổi so v2**: Hạ ngưỡng Label 1 (m_score≥1 là đủ, không cần aerospace); giảm ảnh hưởng của FUTURE_HEDGE với Label 1; đọc content trực tiếp từ v4 Excel thay vì rebuild từ JSON.
- **Công cụ**: `statsmodels.stats.inter_rater.fleiss_kappa` + `sklearn.metrics.cohen_kappa_score`
