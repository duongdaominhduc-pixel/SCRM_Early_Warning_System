# P1-05 — Schema & Handoff: News Data

## Task này làm gì

Định nghĩa schema chính thức của file news data (`final_supplychain_news_2015_2018.jsonl`) và viết tài liệu bàn giao cho Phase 2 (gán nhãn thủ công). Đây là "hợp đồng giao diện" giữa Phase 1 và Phase 2.

## Đã làm như thế nào

1. Đọc file JSONL bằng `pandas.read_json(..., lines=True)`
2. Kiểm tra schema thực tế: tên cột, kiểu dữ liệu, null count
3. So sánh với README gốc để phát hiện chênh lệch
4. Tính thống kê mô tả: word count, source distribution, date range
5. Viết `clean_news_schema.md` mô tả chính xác theo file thực tế

## Output

| File | Mô tả |
|---|---|
| `clean_news_schema.md` | Schema đầy đủ: data dictionary, thống kê, cách đọc file, ví dụ record, lưu ý handoff |

## Vấn đề / Giới hạn cần nhóm lưu ý

### ⚠️ 1. Schema thực tế khác README gốc
README mô tả 8 cột (`author`, `word_count`, `language` có mặt), nhưng file thực tế chỉ có **7 cột**. Ba trường đó không tồn tại:
- `author` → không có
- `word_count` → không có sẵn, phải tự tính: `df["cleaned_content"].str.split().str.len()`
- `language` → không có (không cần thiết vì toàn bộ EN)

### ⚠️ 2. Cột `publish_date` không đồng nhất
Cột `publish_date` (raw) có format hỗn hợp: hầu hết là `"YYYY-MM-DD"`, nhưng một số dòng là Unix timestamp milliseconds (ví dụ: `"1420483810000"`). **Luôn dùng `publish_date_parsed`** cho mọi thao tác time-based.

### ℹ️ 3. Tên file khác PCCV
PCCV ghi "clean_news.csv" nhưng file thực tế là `.jsonl`. Không cần đổi tên — chỉ cần đọc đúng cách.

### ℹ️ 4. Đã sort chronological sẵn
JSONL đã được sort theo `publish_date_parsed` ascending từ bước xử lý trước. Phase 2 có thể lấy 700 bài đầu tiên (oldest) làm tập gán nhãn mà không cần sort lại.
