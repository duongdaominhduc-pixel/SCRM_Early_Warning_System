import pandas as pd
import xgboost as xgb
import shap
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=== Phân tích SHAP (Feature Importance) - DỮ LIỆU THỰC TẾ ===")

# 1. Đọc dữ liệu
try:
    df = pd.read_parquet('P5-01/feature_matrix.parquet')
except:
    df = pd.read_csv('P5-01/feature_matrix.csv')

# 2. Dọn dẹp: Vứt bỏ các cột chữ/không phải đặc trưng để AI khỏi bị nghẹn
cols_to_drop = ['week', 'part_family', 'part_group', 'y_true', 'publish_date', 'event_id']
X = df.drop(columns=[c for c in cols_to_drop if c in df.columns])

# Ép toàn bộ các cột còn lại thành SỐ (đảm bảo 100% an toàn)
for col in X.columns:
    X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

# 3. Load Mô hình AI
model = xgb.XGBClassifier()
model.load_model('P5-08/xgb_model.json')

# 4. Tính toán SHAP
print("⏳ Đang tính toán mức độ quan trọng của từng yếu tố...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# 5. Lưu kết quả
mean_abs_shap = np.abs(shap_values).mean(axis=0)

importance_df = pd.DataFrame({
    'feature': X.columns,
    'mean_abs_shap': mean_abs_shap
}).sort_values('mean_abs_shap', ascending=False).reset_index(drop=True)

importance_df.to_csv('P5-10/shap_importance_summary.csv', index=False)

print("\n✅ KẾT QUẢ SHAP THẬT SỰ (Top 10 Đặc trưng):")
print("-" * 50)
print(importance_df.head(10).to_string(index=False))
print("-" * 50)
print("🎉 HOÀN TẤT! File đã được lưu tại P5-10/shap_importance_summary.csv")