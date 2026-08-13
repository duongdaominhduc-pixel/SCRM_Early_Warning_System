# 🛡️ ML Audit Verdict: P2-03 Feature Matrix

- **Folder Path:** `P2-03_Feature_Matrix`
- **Audit Date:** 2026-07-13
- **Auditor:** Antigravity (Senior ML Auditor)

## 1. Audit Status
**[NEED REFACTOR]** - Vi phạm tính dừng (Stationarity) của các biến Vận hành Chuỗi cung ứng theo chuẩn Gold Standard.

## 2. Scientific Validity
- **Kiểm định ADF (Augmented Dickey-Fuller) & Biến Delta:** Gold Standard yêu cầu các biến chuỗi thời gian vận hành (như `w1_open_po_qty`, `w1_on_hand_inventory`) phải được kiểm định ADF. Nếu chuỗi không dừng, bắt buộc phải tính sai phân bậc 1 (Delta) để tránh hồi quy giả mạo (Spurious Regression). Hiện tại hệ thống truyền thẳng raw values vào ML model. **[FAIL]**
- **Chuẩn hóa Tên biến (Naming Convention):** Các biến rủi ro tổng hợp đã được tuân thủ đúng tiền tố/hậu tố thời gian (VD: suffix `_w1`, `_w2`). **[PASS]**

## 3. SHA256 Checksum Verification
- Không yêu cầu.

## 4. Action Items
- **[Code Fix]** Cập nhật `run_phase2_pipeline.py` ở hàm `run_p2_03`: Bổ sung kiểm định ADF cho các features ERP, tạo ra các cột Delta (ví dụ `delta_open_po_qty_w1`) thay vì sử dụng biến nguyên bản nếu dữ liệu không dừng.
