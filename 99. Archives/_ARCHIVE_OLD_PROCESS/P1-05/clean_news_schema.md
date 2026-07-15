# Schema: `final_supplychain_news_2015_2018.jsonl`

**File gốc:** `0. news data/final_supplychain_news_2015_2018.jsonl`
**Format:** JSONL (JSON Lines) — mỗi dòng là một JSON object độc lập
**Tổng số bài:** 2,554
**Khoảng thời gian:** 2015-01-05 → 2018-08-30

> ⚠️ **Lưu ý đặt tên:** PCCV ghi "clean_news.csv" nhưng file thực tế là `.jsonl`.
> Các task tiếp theo (P2-01 v.v.) đọc bằng `pd.read_json(..., lines=True)` hoặc vòng lặp `json.loads`.

---

## Data Dictionary (Schema thực tế)

| # | Tên cột | Kiểu dữ liệu | Null | Mô tả | Ghi chú |
|---|---|---|---|---|---|
| 1 | `url` | String | 0 | URL gốc của bài báo — dùng làm khóa dedup | Unique, dùng làm event_id seed |
| 2 | `source` | String | 0 | Nguồn báo: `joc.com` hoặc `supplychainbrain.com` | Khác với README (đã thêm `.com`) |
| 3 | `publish_date` | String | 0 | Ngày đăng dạng raw — **KHÔNG ĐỒNG NHẤT**: đa số là `"YYYY-MM-DD"`, một số dòng là Unix timestamp milliseconds (ví dụ: `"1420483810000"`) | ⚠️ Không dùng cột này trực tiếp |
| 4 | `publish_date_parsed` | datetime64 | 0 | Ngày đăng đã chuẩn hóa — **DÙNG CỘT NÀY** cho mọi xử lý time-based | Format: `YYYY-MM-DD HH:MM:SS`, giờ luôn = 00:00:00 |
| 5 | `title` | String | 0 | Tiêu đề bài báo gốc | Dùng kết hợp với `cleaned_content` để tokenize cho DistilBERT |
| 6 | `content` | String | 0 | Nội dung bài báo thô (raw HTML đã strip) — giữ để audit/trace | **Không dùng** để train model |
| 7 | `cleaned_content` | String | 0 | Nội dung sạch, sẵn sàng cho NLP — đã loại HTML, ads, boilerplate | **Trường chính** cho mọi NLP task |

**Lưu ý so với mô tả trong README gốc:**
- README mô tả 8 trường nhưng file thực tế chỉ có **7 trường**
- Các trường `author`, `word_count`, `language` **không tồn tại** trong file
- `source` dùng domain đầy đủ (`joc.com`, `supplychainbrain.com`), không phải tên ngắn

---

## Thống kê mô tả

| Chỉ số | Giá trị |
|---|---|
| Tổng bài | 2,554 |
| Nguồn joc.com | 874 bài (34.2%) |
| Nguồn supplychainbrain.com | 1,680 bài (65.8%) |
| Null bất kỳ cột nào | 0 |
| Ngày sớm nhất | 2015-01-05 |
| Ngày muộn nhất | 2018-08-30 |
| Word count (cleaned_content) — trung bình | 446 từ |
| Word count — min | 100 từ |
| Word count — median | 272 từ |
| Word count — max | 4,988 từ |

---

## Cách đọc file (chuẩn cho Phase 2 trở đi)

```python
import pandas as pd

df = pd.read_json(
    "0. news data/final_supplychain_news_2015_2018.jsonl",
    lines=True
)
df["publish_date_parsed"] = pd.to_datetime(df["publish_date_parsed"])

# Tính word_count nếu cần (không có sẵn trong file)
df["word_count"] = df["cleaned_content"].str.split().str.len()

# Cột dùng cho NLP training
# Input:   title + " [SEP] " + cleaned_content[:512 tokens]
# Không dùng: content, publish_date (raw)
```

---

## Ví dụ record

```json
{
  "url": "https://www.supplychainbrain.com/articles/20611-...",
  "source": "supplychainbrain.com",
  "publish_date": "2015-01-05",
  "publish_date_parsed": "2015-01-05T00:00:00",
  "title": "A Conversation With a Supply-Chain Millennial",
  "content": "Having racked up eight years of experience...",
  "cleaned_content": "Having racked up eight years of experience in supply chain to date..."
}
```

---

## Các điểm cần lưu ý khi handoff sang Phase 2 (Gán nhãn)

1. **Dùng `publish_date_parsed` làm trục thời gian**, không phải `publish_date` (raw format không nhất quán).
2. **700 bài gán nhãn phải lấy từ file này theo thứ tự chronological** (P2-06 yêu cầu Chronological Split — đã sort sẵn trong JSONL).
3. **Input cho annotator:** cột `title` + `cleaned_content` (không cần show `content` raw).
4. **event_id cho Phase 3:** dùng `hash(url)` hoặc `hash(url + publish_date_parsed)` để tạo ID duy nhất.
5. **Lệnh gán nhãn cụ thể:** export 100 bài đầu (theo thứ tự hiện tại trong file) sang Google Sheet cho pilot P2-01.
