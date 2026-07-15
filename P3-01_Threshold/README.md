# P3-01 | Tối ưu hóa Ngưỡng Cảnh báo (Threshold Optimization)

## 📌 Tổng quan
Thay vì dùng ngưỡng cố định 0.5 để kích hoạt cảnh báo, hệ thống tự động tìm ra ngưỡng tối ưu cho từng họ linh kiện (Part Family) để tránh hiện tượng báo động giả quá nhiều (Alert Fatigue).

## 🎯 Kết quả Thực nghiệm & ML Audit (Audited)
- Hệ thống áp dụng **Chronological Split 60/40** (chia cắt theo trình tự thời gian) để học ngưỡng trên quá khứ và đo lường trên tương lai, đảm bảo không Data Leakage. **(Audited: PASS)**
- Sử dụng **F0.5-score** thay vì F1-score để ép hệ thống ưu tiên Precision (Độ chính xác) gấp đôi Recall.
- Output: `threshold_optimization_report.md` chứa bảng ngưỡng lý tưởng cho từng họ linh kiện, cùng biểu đồ `global_threshold_sweep.png`.
