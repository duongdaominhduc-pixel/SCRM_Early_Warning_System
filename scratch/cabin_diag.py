import pandas as pd
import sys

try:
    df = pd.read_parquet('P2-03_Feature_Matrix/feature_matrix.parquet')
    df_y2 = pd.read_parquet('P2-04_Derive_y2/y2_shifted.parquet')
    df_parts = pd.read_csv('0. internal data/parts_master.csv')
    
    if 'y2_shift1' in df_y2.columns:
        target_col = 'y2_shift1'
    else:
        target_col = df_y2.columns[-1]
        
    df_merged = pd.merge(df, df_y2[['part_id', 'week', target_col]], on=['part_id', 'week'], how='inner')
    df_merged = pd.merge(df_merged, df_parts[['part_id', 'part_family']], on='part_id', how='inner')
    df_merged = df_merged.rename(columns={target_col: 'y_true'})
    
    cabin_df = df_merged[df_merged['part_family'] == 'Cabin'].copy()
    print(f"--- BÁO CÁO CHẨN ĐOÁN NHÓM CABIN ---")
    print(f"Tổng số mẫu (tuần): {len(cabin_df)}")
    print(f"Số mẫu đứt gãy (y_true=1): {cabin_df['y_true'].sum()}")
    print(f"Số mẫu bình thường (y_true=0): {len(cabin_df) - cabin_df['y_true'].sum()}")
    
    if cabin_df['y_true'].sum() <= 3:
        print("⚠️ KẾT LUẬN: Nguyên nhân là do Sample Size quá nhỏ (Chỉ có <= 3 sự cố). Mô hình bị Overfit cục bộ.")
    else:
        correlations = cabin_df.corr(numeric_only=True)['y_true'].abs().sort_values(ascending=False)
        print("\n🔍 Top 5 features tương quan mạnh nhất với y_true:")
        print(correlations[1:6])
        if correlations.iloc[1] > 0.9:
            print(f"🚨 KẾT LUẬN: DATA LEAKAGE PHÁT HIỆN! Biến '{correlations.index[1]}' có tương quan {correlations.iloc[1]:.4f}. Hãy loại bỏ biến này khỏi X_train.")
except Exception as e:
    print(f"Error: {e}")
