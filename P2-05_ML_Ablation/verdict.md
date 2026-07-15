# 🛡️ ML Audit Verdict: P2-05 ML Ablation

- **Folder Path:** `P2-05_ML_Ablation`
- **Audit Date:** 2026-07-13
- **Auditor:** Antigravity (Senior ML Auditor)

## 1. Audit Status
**[PASS]** - Đạt tiêu chuẩn tối cao về kiểm soát rò rỉ dữ liệu và Cross-Validation cho dữ liệu chuỗi thời gian (Q1 Journal Gold Standard).

## 2. Scientific Validity
- **Chống Leakage Tầng Validation:** Đã triệt tiêu hoàn toàn kỹ thuật Downsampling toàn cục (Global Downsampling). Dữ liệu được đưa vào TimeSeriesSplit nguyên bản.
- **Cân bằng dữ liệu (In-Fold Balancing):** Biến `scale_weight` được tính toán *độc quyền* trên tập Training của mỗi fold (`y_tr`) và truyền thẳng vào tham số `scale_pos_weight` của XGBoost. Tập Validation (`y_va`) được bảo toàn 100% phân phối tự nhiên hiếm gặp (<5%). 
- Tính khoa học của các con số PR-AUC và Minority F1-score từ đó là tuyệt đối đáng tin cậy.

## 3. SHA256 Checksum Verification
- Không yêu cầu.

## 4. Action Items
- Kỹ thuật In-Fold Balancing là một thành tựu đáng kể. Chấp nhận hoàn toàn để viết báo cáo khoa học.
