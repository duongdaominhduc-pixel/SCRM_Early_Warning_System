"""
Extract exact stress-test (W-2 ops) metrics: Precision, Recall, F1
and compare with W-1 primary model and Tier1 baseline.
"""
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, precision_score, recall_score

ROOT = Path(__file__).resolve().parent.parent

# Load stress test feature matrix
stress_matrix_path = ROOT / "P2-03_Feature_Matrix" / "feature_matrix_w2_ops.parquet"
y2_path = ROOT / "P2-04_Derive_y2" / "y2_shifted.parquet"

df_stress = pd.read_parquet(stress_matrix_path)
df_y2 = pd.read_parquet(y2_path)

# Merge target
df_merged = pd.merge(df_stress, df_y2[['part_id', 'week', 'y2_shift1']], on=['part_id', 'week'], how='inner')

# Get stress features (same logic as pipeline)
stress_features = [c for c in df_merged.columns if (c.startswith('w2_') or c.endswith('_w1') or c.endswith('_w2'))
                   and c not in ['w2_stockout_flag'] and 'dominant_event_type' not in c]
print(f"Stress features ({len(stress_features)}): {stress_features}")

y = df_merged['y2_shift1'].values
X = df_merged[stress_features].values

# Walk-forward with TimeSeriesSplit (same as pipeline)
tscv = TimeSeriesSplit(n_splits=5, gap=2)

fold_metrics = []
for fold_idx, (train_idx, val_idx) in enumerate(tscv.split(X)):
    X_tr, X_va = X[train_idx], X[val_idx]
    y_tr, y_va = y[train_idx], y[val_idx]
    
    if len(y_va) == 0 or sum(y_va == 1.0) == 0:
        continue
    
    imputer = SimpleImputer(strategy='median')
    X_tr_p = imputer.fit_transform(X_tr)
    X_va_p = imputer.transform(X_va)
    
    # Compute scale_pos_weight in-fold
    n_neg = np.sum(y_tr == 0)
    n_pos = max(np.sum(y_tr == 1), 1)
    spw = n_neg / n_pos
    
    try:
        from xgboost import XGBClassifier
        clf = XGBClassifier(random_state=42, eval_metric='logloss', scale_pos_weight=spw)
    except ImportError:
        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(random_state=42)
    
    clf.fit(X_tr_p, y_tr)
    preds = clf.predict(X_va_p)
    
    f1 = f1_score(y_va, preds, zero_division=0)
    prec = precision_score(y_va, preds, zero_division=0)
    rec = recall_score(y_va, preds, zero_division=0)
    
    fold_metrics.append({'fold': fold_idx, 'precision': prec, 'recall': rec, 'f1': f1})
    print(f"  Fold {fold_idx}: Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}")

df_folds = pd.DataFrame(fold_metrics)
print("\n" + "=" * 60)
print("STRESS TEST (W-2 OPS) - AGGREGATE RESULTS:")
print("=" * 60)
mean_prec = df_folds['precision'].mean()
mean_rec = df_folds['recall'].mean()
mean_f1 = df_folds['f1'].mean()
print(f"  Mean Precision: {mean_prec:.4f}")
print(f"  Mean Recall:    {mean_rec:.4f}")
print(f"  Mean F1-score:  {mean_f1:.4f}")

# Compare with primary model (W-1)
primary_f1 = 0.2064   # from ablation_results.md Tier3_XGB_SCRM y2_shift1
primary_prec = 0.1654
tier1_f1 = 0.1076     # Tier1_RuleBased y2_shift1

pct_decline_vs_primary = (1 - mean_f1 / primary_f1) * 100
pct_advantage_vs_tier1 = ((mean_f1 / tier1_f1) - 1) * 100 if tier1_f1 > 0 else float('inf')

print(f"\n--- COMPARISON ---")
print(f"  Primary W-1 Tier3_XGB_SCRM F1: {primary_f1:.4f}")
print(f"  Stress W-2 F1:                  {mean_f1:.4f}")
print(f"  Decline vs primary:             {pct_decline_vs_primary:.1f}%")
print(f"")
print(f"  Tier1 RuleBased F1:             {tier1_f1:.4f}")
if mean_f1 > tier1_f1:
    print(f"  Stress W-2 advantage vs Tier1:  {pct_advantage_vs_tier1:.1f}% BETTER")
else:
    print(f"  Stress W-2 vs Tier1:            WORSE (stress model underperforms Tier1)")
