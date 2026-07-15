import pandas as pd
from pathlib import Path
import os
import re

P0_04_DIR = Path(r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH\P0-04_Pseudo_Labeling")
P0_03_DIR = Path(r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH\P0-03_Pilot_Labeling")

batch_file = P0_04_DIR / "P0-04_manual_batch_2160.xlsx"
pilot_file = P0_03_DIR / "P0-03_pilot_labeling_150_v6.xlsx"
out_combined = P0_04_DIR / "manual_combined_2309.csv"

def is_valid_stt(val):
    try:
        int(float(str(val).strip()))
        return True
    except (ValueError, TypeError):
        return False

# Cột chuẩn mong muốn cho toàn bộ file
DESIRED_COLS = ['Nguồn', 'Ngày đăng', 'Tiêu đề', 'URL', 'Nội dung (đầy đủ)', 'Nhãn (0/1/2)']
FINAL_COLS = ['source', 'date', 'title', 'url', 'content', 'label']

# 1. Process Batch file
print("Processing P0-04_manual_batch_2160.xlsx...")
xls = pd.ExcelFile(batch_file)
batch_dfs = []

# Loại bỏ các sheet tổng quan, bất kể cách viết
valid_sheets = [s for s in xls.sheet_names if not any(x in s.lower().replace(" ", "") for x in ["tongquan", "tổngquan"])]

for sheet in valid_sheets:
    df = pd.read_excel(batch_file, sheet_name=sheet, header=2)
    
    col_mapping = {}
    for c in df.columns:
        c_str = str(c).strip()
        if 'STT' in c_str: col_mapping[c] = 'STT'
        elif 'Nguồn' in c_str: col_mapping[c] = 'Nguồn'
        elif 'Ngày đăng' in c_str: col_mapping[c] = 'Ngày đăng'
        elif 'Tiêu đề' in c_str: col_mapping[c] = 'Tiêu đề'
        elif 'URL' in c_str: col_mapping[c] = 'URL'
        elif 'Nội dung' in c_str: col_mapping[c] = 'Nội dung (đầy đủ)'
        elif 'Nhãn' in c_str: col_mapping[c] = 'Nhãn (0/1/2)'
        
    df = df.rename(columns=col_mapping)
    
    if 'STT' in df.columns:
        df_filtered = df[df['STT'].apply(is_valid_stt)].copy()
    else:
        df_filtered = df.copy()
        
    # Drop columns that are not in DESIRED_COLS
    df_filtered = df_filtered[[c for c in DESIRED_COLS if c in df_filtered.columns]]
    
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '', sheet)
    out_name = P0_04_DIR / f"manual_batch_{safe_name}_540.csv"
    
    for c in df_filtered.columns:
        if df_filtered[c].dtype == 'object':
            df_filtered[c] = df_filtered[c].astype(str).apply(lambda x: x.replace('\r\n', '\n').replace('\r', '\n') if str(x).lower() != 'nan' else '')
            
    df_filtered.to_csv(out_name, index=False, encoding='utf-8-sig', lineterminator='\n')
    print(f" - Sheet '{sheet}': extracted {len(df_filtered)} rows")
    batch_dfs.append(df_filtered)

df_batch_combined = pd.concat(batch_dfs, ignore_index=True)
print(f"Total Batch items: {len(df_batch_combined)} (Expected: 2160)")

# 2. Process Pilot file
print("\nProcessing P0-03_pilot_labeling_150_v6.xlsx...")
df_pilot = pd.read_excel(pilot_file, header=1)
first_col_pilot = df_pilot.columns[0]
df_pilot = df_pilot[df_pilot[first_col_pilot].apply(is_valid_stt)].copy()

pilot_cols = df_pilot.columns.tolist()
label_col_name = pilot_cols[6]

df_pilot = df_pilot.dropna(subset=[label_col_name])
print(f"Total Pilot items after dropping NA labels: {len(df_pilot)} (Expected: 149)")

rename_map = {
    'Ngay dang': 'Ngày đăng',
    'Nguon': 'Nguồn',
    'Tieu de bai bao': 'Tiêu đề',
    'Noi dung day du': 'Nội dung (đầy đủ)',
    label_col_name: 'Nhãn (0/1/2)'
}
df_pilot = df_pilot.rename(columns=rename_map)

for c in DESIRED_COLS:
    if c not in df_pilot.columns:
        df_pilot[c] = None

df_pilot_clean = df_pilot[DESIRED_COLS].copy()

# 3. Combine and Save
print("\nCombining data...")
df_combined = pd.concat([df_batch_combined, df_pilot_clean], ignore_index=True)
print(f"Total combined items: {len(df_combined)} (Expected: 2309)")

for c in DESIRED_COLS:
    if c not in df_combined.columns:
        continue
    if df_combined[c].dtype == 'object':
        df_combined[c] = df_combined[c].astype(str).apply(lambda x: x.replace('\r\n', '\n').replace('\r', '\n') if str(x).lower() != 'nan' else '')

df_combined = df_combined.dropna(how='all', axis=1)

# Rename to English
df_combined.columns = FINAL_COLS

df_combined.to_csv(out_combined, index=False, encoding='utf-8-sig', lineterminator='\n')
print(f"Successfully saved to {out_combined.name}")
