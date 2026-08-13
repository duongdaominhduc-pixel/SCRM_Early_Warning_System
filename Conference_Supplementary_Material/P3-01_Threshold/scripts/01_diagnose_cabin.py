import pandas as pd
import os

print("--- BÁO CÁO CHẨN ĐOÁN NHÓM CABIN ---")
file_path = '../../P2-03_Feature_Matrix/feature_matrix.parquet'

if not os.path.exists(file_path):
    print(f"Không tìm thấy file: {file_path}")
    exit(1)

print("Đang đọc dữ liệu Parts Master...")
parts_df = pd.read_csv('../../0. internal data/parts_master.csv')
cabin_parts = parts_df[parts_df['part_family'] == 'Cabin']['part_id'].tolist()

if not cabin_parts:
    print("Không tìm thấy linh kiện nào thuộc nhóm Cabin trong parts_master.csv!")
    exit(1)

print("Đang đọc dữ liệu Feature Matrix (chỉ nạp nhóm Cabin để tiết kiệm RAM)...")
try:
    cabin_df = pd.read_parquet(file_path, engine='pyarrow', filters=[('part_id', 'in', cabin_parts)])
except Exception as e:
    print(f"Lỗi khi đọc file parquet (có thể không dùng được filter in): {e}")
    # Fallback đọc toàn bộ và lọc
    print("Đang đọc toàn bộ dữ liệu...")
    df = pd.read_parquet(file_path)
    cabin_df = df[df['part_id'].isin(cabin_parts)].copy()
    del df # Xóa khỏi RAM

print(f"Tổng số mẫu (tuần) của Cabin: {len(cabin_df)}")
pos_samples = cabin_df['stockout_flag_target'].sum()
print(f"Số mẫu đứt gãy (stockout_flag_target=1): {pos_samples}")
print(f"Số mẫu bình thường (stockout_flag_target=0): {len(cabin_df) - pos_samples}")

if pos_samples <= 3:
    print("\n⚠️ KẾT LUẬN: Nguyên nhân F1 = 1.0 là do Sample Size quá nhỏ (Chỉ có <= 3 sự cố). Mô hình bị Overfit cục bộ.")
    print("-> Khuyến nghị: Báo cáo trong giới hạn nghiên cứu (Limitations) hoặc loại bỏ nhóm này khi tính trung bình (Macro-average).")
else:
    print("\nQuét Data Leakage (Tính tương quan tuyệt đối với stockout_flag_target)...")
    correlations = cabin_df.corr(numeric_only=True)['stockout_flag_target'].abs().sort_values(ascending=False)
    print("\n🔍 Top 5 features tương quan mạnh nhất với stockout_flag_target:")
    print(correlations[1:6])
    
    if correlations.iloc[1] > 0.9:
        print(f"\n🚨 KẾT LUẬN: DATA LEAKAGE PHÁT HIỆN! Biến '{correlations.index[1]}' có tương quan {correlations.iloc[1]:.4f}.")
        print("-> Khuyến nghị: Hãy loại bỏ biến này khỏi X_train trước khi huấn luyện mô hình.")
    else:
        print("\n✅ KẾT LUẬN: Không phát hiện rò rỉ dữ liệu rõ rệt từ các biến hiện tại (Correlation < 0.9).")
