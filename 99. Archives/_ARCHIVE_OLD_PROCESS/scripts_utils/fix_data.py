import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("⏳ Đang ép dữ liệu NLP thật vào Bảng Đặc trưng (Bản hoàn hảo!)...")

fm = pd.read_csv('P5-01/feature_matrix.csv')
nlp = pd.read_parquet('P4-05/soft_join_real_output.parquet')

# Sửa tên cột cho khớp
if 'part_group' in fm.columns and 'part_family' in nlp.columns:
    nlp = nlp.rename(columns={'part_family': 'part_group'})
    merge_col = 'part_group'
else:
    merge_col = 'part_family'

# Xóa cột mock cũ
cols_nlp = ['news_risk_score', 'severity_score', 'disruption_event_flag']
fm = fm.drop(columns=[c for c in cols_nlp if c in fm.columns])

# CHIẾN THUẬT: Giấu cột week dạng chữ đi, tạo 1 cột week dạng ngày để ráp nối
fm['week_original'] = fm['week'] # Cất đi
fm['week_dt'] = fm['week'].astype(str).str.split('/').str[0]
fm['week_dt'] = pd.to_datetime(fm['week_dt'])

nlp['week_dt'] = pd.to_datetime(nlp['week'])
nlp = nlp.drop(columns=['week']) # Xóa week của nlp để khỏi đụng hàng

# Ráp nối bằng cột Ngày
fm = pd.merge(fm, nlp, on=['week_dt', merge_col], how='left')
fm[cols_nlp] = fm[cols_nlp].fillna(0)

# Dọn dẹp: Trả lại cột week dạng Chữ cho con AI nó đọc
fm['week'] = fm['week_original'].astype(str)
fm = fm.drop(columns=['week_original', 'week_dt'])

# Lưu đè lên cả 2 file
fm.to_csv('P5-01/feature_matrix.csv', index=False)
fm.to_parquet('P5-01/feature_matrix.parquet', index=False)

print("✅ Đã chèn DATA THẬT và XỬ LÝ LỖI ĐỊNH DẠNG! Giờ bạn có thể chạy AI.")