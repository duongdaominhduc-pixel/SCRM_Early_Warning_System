import pandas as pd

print("--- TÍNH TOÁN LEAD-TIME GAIN (LTG) THEO NHÓM LINH KIỆN ---")

# Bạn cập nhật đường dẫn tới file kết quả cảnh báo (alerts) của Pipeline V2 vào đây nhé
file_path = 'weekly_alerts.csv'

try:
    df = pd.read_csv(file_path)
    # The week format is like "2022-W01". Add '-1' for Monday to parse it properly.
    df['week'] = pd.to_datetime(df['week'] + '-1', format="%G-W%V-%u")
except FileNotFoundError:
    print(f"⚠️ Không tìm thấy file: {file_path}")
    print("Tiến hành tạo dữ liệu giả lập (Mock Data) để minh họa bảng kết quả LTG...\n")
    # Tạo dữ liệu giả lập cho 3 nhóm linh kiện
    mock_data = []
    dates = pd.date_range(start="2024-01-01", periods=10, freq="W")
    for group, act_idx, alert_idx in [
        ('Electrical', [4], [2, 3]), 
        ('Avionics', [8], [6]), 
        ('Cabin', [5], [5])
    ]:
        for i, d in enumerate(dates):
            mock_data.append({
                'part_family': group,
                'week': d,
                'is_alert': 1 if i in alert_idx else 0,
                'y_true': 1 if i in act_idx else 0
            })
    df = pd.DataFrame(mock_data)
except Exception as e:
    print(f"Lỗi khi đọc dữ liệu: {e}")
    exit(1)

# Kiểm tra tên cột nhóm
group_col = 'part_family' if 'part_family' in df.columns else 'part_group' if 'part_group' in df.columns else None
if not group_col:
    print("Không tìm thấy cột part_family hoặc part_group. Vui lòng kiểm tra lại dữ liệu.")
    exit(1)

ltw_records = []
for name, group in df.groupby(group_col):
    # Lấy danh sách các tuần có báo động và các tuần đứt gãy thực tế
    alerts = group[group['is_alert'] == 1]['week'].tolist()
    actuals = group[group['y_true'] == 1]['week'].tolist()
    
    group_ltw = []
    for actual_date in actuals:
        # Lọc các cảnh báo hợp lệ: Xảy ra trước ngày đứt gãy (0 ngày < khoảng cách <= 56 ngày tức 8 tuần)
        valid_alerts = [a for a in alerts if 0 < (actual_date - a).days <= 56]
        if valid_alerts:
            # Chọn cảnh báo sớm nhất (hoặc gần nhất, tùy chiến lược, ở đây chọn gần nhất = max)
            best_alert = max(valid_alerts)
            group_ltw.append((actual_date - best_alert).days / 7.0)
            
    if group_ltw:
        ltw_records.append({
            'Component Group': name,
            'Detected Disruptions': len(group_ltw),
            'Mean LTW (Weeks)': sum(group_ltw) / len(group_ltw),
            'Min LTW': min(group_ltw),
            'Max LTW': max(group_ltw)
        })

if not ltw_records:
    print("Không tính toán được LTW nào (có thể do chưa có cảnh báo nào khớp với đứt gãy trong vòng 8 tuần).")
else:
    results_df = pd.DataFrame(ltw_records)
    print("\n✅ BẢNG KẾT QUẢ LEAD-TIME WARNING (LTW) DÀNH CHO BÀI BÁO:")
    print(results_df.to_markdown(index=False, floatfmt=".1f"))
    print("\n(Bạn có thể copy bảng này và chèn vào bài báo)")
