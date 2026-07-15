# CÁC VẤN ĐỀ LOGIC TRONG PHASE 3 & HƯỚNG GIẢI QUYẾT CHI TIẾT

Tài liệu này tổng hợp toàn bộ các vấn đề học thuật và lỗi kỹ thuật phát hiện được trong **Phase 3 (Evaluation & Explainability)** và cung cấp hướng giải quyết chi tiết (kèm code sửa đổi) để hoàn thiện đồ án đạt chuẩn tạp chí khoa học Q1.

---

## 1. VẤN ĐỀ 1: RÒ RỈ DỮ LIỆU KHI TỐI ƯU HÓA NGƯỠNG (THRESHOLD TUNING LEAKAGE)

### 🔴 Mô tả vấn đề:
Trong hàm `run_p3_01` của file `run_phase3_pipeline.py`, việc quét tìm ngưỡng quyết định tối ưu (Threshold Sweep) dựa trên điểm số $F_{0.5}$ đang được thực hiện trên **toàn bộ tập dữ liệu đánh giá** (`df_eval`). 
*   **Hậu quả:** Điều này vi phạm nguyên tắc phân tách dữ liệu nghiêm ngặt trong học máy. Việc sử dụng thông tin từ tập kiểm định (Test Set) để tinh chỉnh siêu tham số (ngưỡng quyết định) sẽ dẫn đến hiện tượng **rò rỉ dữ liệu**. Kết quả Precision/Recall báo cáo trong bảng sẽ bị "quá lạc quan" (Optimistic Bias) và không phản ánh đúng hiệu năng thực tế của mô hình khi tiếp nhận dữ liệu hoàn toàn mới.

### 🟢 Hướng giải quyết:
Áp dụng **Chronological Split** (Chia dữ liệu theo trục thời gian thực tế):
1. Chia tập `df_eval` thành hai phần:
   * **Tập Validation (Ví dụ: 60% thời gian đầu):** Dùng để chạy quét tìm ngưỡng tối ưu cho từng nhóm linh kiện (`part_family`).
   * **Tập Test độc lập (Ví dụ: 40% thời gian cuối):** Dùng để đánh giá hiệu năng cuối cùng (Precision, Recall, F0.5) với ngưỡng đã được cố định từ tập Validation.
2. Báo cáo kết quả hiệu năng trên tập Test độc lập này trong bài báo khoa học.

### 💻 Code gợi ý sửa đổi:
```python
# Chia dữ liệu theo thời gian
weeks_sorted = sorted(df_eval['week'].unique())
split_idx = int(len(weeks_sorted) * 0.6)
val_weeks = weeks_sorted[:split_idx]
test_weeks = weeks_sorted[split_idx:]

df_val = df_eval[df_eval['week'].isin(val_weeks)].copy()
df_test = df_eval[df_eval['week'].isin(test_weeks)].copy()

# Bước 1: Tìm optimal_thresholds trên df_val
# (Giữ nguyên logic sweep như hiện tại nhưng chạy trên df_val)

# Bước 2: Áp dụng optimal_thresholds đã tìm được lên df_test để tính Precision/Recall cuối cùng
```

---

## 2. VẤN ĐỀ 2: THIẾU TÍNH ĐỒNG BỘ GIỮA SHAP VÀ CASE STUDY

### 🔴 Mô tả vấn đề:
*   Trong Task P3-02 (SHAP), mô hình đang lấy ngẫu nhiên mẫu đầu tiên của dữ liệu kiểm định (`X_proc[:1]`) để vẽ biểu đồ giải thích cục bộ (SHAP Waterfall Plot).
*   Trong Task P3-03 (Case Study), chúng ta lại mô phỏng chi tiết trên linh kiện **P00179** (nhóm Electrical).
*   **Hậu quả:** Hai phần này đang bị tách rời độc lập, làm giảm tính thuyết phục của phần Case Study. Người đọc không thấy được cơ chế giải thích của SHAP hoạt động ra sao trên chính linh kiện được làm Case Study.

### 🟢 Hướng giải quyết:
**Đồng bộ hóa Case Study:**
1. Xác định thời điểm hệ thống bắt đầu phát cảnh báo sớm cho linh kiện **P00179** (ví dụ: tuần $W$ mà tại đó Risk Score vượt ngưỡng $0.9$).
2. Trích xuất đúng dòng dữ liệu (features) của linh kiện **P00179** tại tuần $W$ đó.
3. Đưa dòng dữ liệu này vào hàm vẽ `shap.plots.waterfall` để giải thích cục bộ.
4. **Kết quả đạt được:** Tạo nên một kịch bản phân tích logic tuyệt đối cho bài báo: *"Hệ thống phát cảnh báo tại tuần W cho linh kiện P00179 và biểu đồ SHAP Waterfall dưới đây giải thích chính xác nguyên nhân là do điểm tin tức địa lý tăng vọt kết hợp tồn kho sụt giảm"*.

### 💻 Code gợi ý sửa đổi:
```python
# Lọc dòng dữ liệu của linh kiện P00179 tại tuần phát cảnh báo W
case_study_idx = df_eval[(df_eval['part_id'] == 'P00179') & (df_eval['week'] == '2024-W15')].index[0]
X_case_study = X_proc[case_study_idx]

# Vẽ SHAP Waterfall cho chính mẫu này
shap.plots.waterfall(explainer(X_case_study.reshape(1, -1))[0], show=False)
```

---

## 3. VẤN ĐỀ 3: GHI CỨNG ĐƯỜNG DẪN TUYỆT ĐỐI TRONG BÁO CÁO (HARDCODED PATH)

### 🔴 Mô tả vấn đề:
Trong file báo cáo kết quả [integration_test_report.md](file:///d:/Downloads/BBKH-20260712T164424Z-2-001/BBKH/BBKH-20260711T164903Z-2-001/BBKH/P3-03_Integration/integration_test_report.md) dòng 8, đường dẫn ảnh Hero Chart bị ghi cứng là:
`/content/drive/MyDrive/BBKH/BBKH/BBKH-20260711T164903Z-2-001/BBKH/P3-03_Integration/case_study_hero_chart.png`
*   **Hậu quả:** Đây là đường dẫn trên Google Drive cá nhân của tác giả. Khi chạy trên các máy tính khác (hoặc khi nộp bài), liên kết này sẽ bị hỏng (Broken Link) và không hiển thị được ảnh.

### 🟢 Hướng giải quyết:
Sử dụng **đường dẫn động** (Dynamic Absolute Path) tự động nhận diện thư mục làm việc hiện hành của máy đang chạy pipeline bằng thư viện `pathlib` của Python.

### 💻 Code gợi ý sửa đổi:
Sửa đổi dòng 388-389 trong file `run_phase3_pipeline.py`:
```python
# Thay vì ghi cứng đường dẫn tĩnh:
f.write("The 3-panel Hero Chart has been generated successfully and saved at:\n")
f.write(f"- [case_study_hero_chart.png](file:///{hero_chart_path.resolve().as_posix()})\n\n")
```

---

## 4. VẤN ĐỀ 4: ĐỊNH NGHĨA TOÁN HỌC CỦA "LEAD-TIME GAIN" CHƯA RÕ RÀNG

### 🔴 Mô tả vấn đề:
Báo cáo Case Study ghi nhận mô hình đạt Lead-Time Gain từ 1 đến 2 tuần, nhưng chưa có định nghĩa và công thức toán học rõ ràng để chứng minh tính khoa học trước Hội đồng phản biện.

### 🟢 Hướng giải quyết:
Định nghĩa công thức toán học chính thức cho chỉ số **Lead-Time Gain (LTG)**:
$$\text{LTG} = T_{\text{stockout}} - T_{\text{first\_alert}}$$
*   **Trong đó:**
    *   $T_{\text{stockout}}$: Tuần thực tế xảy ra sự cố tồn kho cạn kiệt ($on\_hand\_qty \le 0$) hoặc đơn hàng về trễ.
    *   $T_{\text{first\_alert}}$: Tuần đầu tiên Risk Score do mô hình XGBoost SCRM dự báo vượt qua ngưỡng quyết định tối ưu đã thiết lập ($P(y_2 \ge \text{threshold})$) và duy trì trạng thái cảnh báo liên tục cho đến khi xảy ra sự cố.
*   Trình bày công thức này vào phần Phương pháp luận của bài báo.

---
*Tài liệu hướng dẫn được tạo bởi Antigravity phục vụ nâng cấp chất lượng nghiên cứu khoa học đề tài SCRM-EWS.*
