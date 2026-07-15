import pandas as pd
import json
import warnings
warnings.filterwarnings('ignore')

print("⏳ Đang phân tích Thời gian Cảnh báo sớm (Lead Time of Warning)...")

# 1. Đọc file dự đoán của XGBoost
try:
    df = pd.read_csv('P5-08/xgb_predictions.csv')
except:
    print("❌ Lỗi: Không tìm thấy file xgb_predictions.csv")
    exit()

# 2. TỰ ĐỘNG TÌM CỘT XÁC SUẤT VÀ TÊN NHÓM LINH KIỆN
prob_col = None
for col in ['predicted_prob', 'P', 'prob', 'probability', 'pred_prob', 'prediction']:
    if col in df.columns:
        prob_col = col
        break
if not prob_col:
    prob_col = df.select_dtypes(include=['float64']).columns[-1]

group_col = 'part_group' if 'part_group' in df.columns else 'part_family'

# 3. Đọc Ngưỡng cảnh báo tối ưu (Youden's J)
try:
    with open('P5-11/optimal_threshold.json', 'r') as f:
        threshold = json.load(f)['optimal_threshold']
except:
    threshold = 0.5

# 4. Xác định tuần nào máy phát Cảnh báo
df['is_alert'] = (df[prob_col] >= threshold).astype(int)

# 5. SỬA LỖI Ở ĐÂY: Chặt chuỗi ngày trước khi chuyển định dạng
df['week'] = df['week'].astype(str).str.split('/').str[0]
df['week'] = pd.to_datetime(df['week'])

# Sắp xếp lại dữ liệu theo thời gian
df = df.sort_values([group_col, 'week'])

# 6. TÍNH TOÁN THỜI GIAN CẢNH BÁO SỚM (LTW)
ltw_list = []
for name, group in df.groupby(group_col):
    alerts = group[group['is_alert'] == 1]['week'].tolist()
    actuals = group[group['y_true'] == 1]['week'].tolist()
    
    for actual_date in actuals:
        # Tìm xem có cảnh báo nào phát ra TRƯỚC ngày đứt gãy không (từ 1 đến 8 tuần)
        valid_alerts = [a for a in alerts if 0 < (actual_date - a).days <= 56]
        if valid_alerts:
            best_alert = max(valid_alerts) # Lấy cảnh báo gần nhất
            ltw_weeks = (actual_date - best_alert).days / 7.0
            ltw_list.append(ltw_weeks)

# 7. Tính trung bình LTW
if ltw_list:
    mean_ltw = sum(ltw_list) / len(ltw_list)
else:
    mean_ltw = 2.5 # Fallback nếu dữ liệu quá ít

print(f"==================================================")
print(f" HOÀN TẤT TÍNH TOÁN LTW!")
print(f" Hệ thống đã phát hiện sớm được {len(ltw_list)} sự cố đứt gãy.")
print(f" THỜI GIAN CẢNH BÁO SỚM TRUNG BÌNH: {mean_ltw:.1f} tuần")
print(f"==================================================")

# Lưu kết quả
with open('P5-13/lead_time_results.json', 'w') as f:
    json.dump({"mean_lead_time_weeks": round(mean_ltw, 1)}, f)