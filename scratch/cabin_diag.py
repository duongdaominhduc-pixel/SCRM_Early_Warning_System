import pandas as pd
df = pd.read_parquet('P2-03_Feature_Matrix/feature_matrix.parquet')
cabin_df = df[df['part_group'] == 'Cabin'].copy()
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
       print(f"🚨 KẾT LUẬN: DATA LEAKAGE PHÁT HIỆN! Biến '{correlations.index[1]}' có tương quan {correlations.iloc[1]:.4f}.")
