"""
FAIR STRESS TEST: W-1 vs W-2 Latency Sensitivity Analysis

Methodology (Apples-to-Apples):
- Uses the SAME pre-trained Tier3_XGB_SCRM model from Phase 2
- Uses the SAME fixed chronological test set (last 40% by time)
- Uses the SAME imputer/scaler from the saved model wrapper
- Uses the SAME per-family optimal thresholds from P3-01 (matching Table 4 methodology)
- W-1 primary: evaluates using original W-1 ERP features (as in main pipeline)
- W-2 stress:  evaluates using W-2 ERP features (substituting w1_* ERP cols -> w2_* ERP cols)
               NLP features remain the same (sourced from near-real-time feeds)
- W-1 result should reproduce Table 4 numbers exactly.
"""
import pickle
import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import precision_score, recall_score, f1_score

ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH     = ROOT / "P2-05_ML_Ablation" / "models" / "Tier3_XGB_SCRM_y2_shift1.pkl"
MATRIX_W1_PATH = ROOT / "P2-03_Feature_Matrix" / "feature_matrix.parquet"
MATRIX_W2_PATH = ROOT / "P2-03_Feature_Matrix" / "feature_matrix_w2_ops.parquet"
Y2_PATH        = ROOT / "P2-04_Derive_y2" / "y2_shifted.parquet"
THRESHOLD_PATH = ROOT / "P3-01_Threshold" / "optimal_threshold.json"
PARTS_PATH     = ROOT / "0. internal data" / "parts_master.csv"

# Load model
print("Loading pre-trained model...")
with open(MODEL_PATH, "rb") as f:
    model_obj, imputer, scaler, features = pickle.load(f)
print(f"  Model: {model_obj.__class__.__name__}")
print(f"  Features ({len(features)}): {features}")

# Load optimal thresholds (per-family, from P3-01)
print("\nLoading optimal thresholds (per-family)...")
if not THRESHOLD_PATH.exists():
    raise FileNotFoundError(f"Run run_phase3_pipeline.py first: {THRESHOLD_PATH}")
with open(THRESHOLD_PATH, "r") as f:
    optimal_thresholds = json.load(f)
print(f"  Loaded: {optimal_thresholds}")

# Load data
print("\nLoading feature matrices...")
df_w1    = pd.read_parquet(MATRIX_W1_PATH)
df_w2    = pd.read_parquet(MATRIX_W2_PATH)
df_y2    = pd.read_parquet(Y2_PATH)
df_parts = pd.read_csv(PARTS_PATH)
part_to_family = dict(zip(df_parts['part_id'], df_parts['part_family']))

# Primary: W-1 matrix + target
df_primary = pd.merge(df_w1, df_y2[['part_id', 'week', 'y2_shift1']],
                      on=['part_id', 'week'], how='inner')
df_primary['part_family'] = df_primary['part_id'].map(part_to_family)
df_primary = df_primary.sort_values('week').reset_index(drop=True)

# Build W-2 stress: replace w1_ ERP cols with w2_ equivalents, keep NLP cols
ERP_W1_COLS = [c for c in features if c.startswith('w1_')]
ERP_W2_MAP  = {c: c.replace('w1_', 'w2_') for c in ERP_W1_COLS}

print("\nSubstituting ERP cols (W-1 -> W-2):")
for k, v in ERP_W2_MAP.items():
    print(f"  {k} -> {v}")

df_stress_raw = pd.merge(df_w2, df_y2[['part_id', 'week', 'y2_shift1']],
                         on=['part_id', 'week'], how='inner')
df_stress = df_primary.copy()
for w1_col, w2_col in ERP_W2_MAP.items():
    if w2_col in df_stress_raw.columns:
        mapping = df_stress_raw.set_index(['part_id', 'week'])[w2_col]
        df_stress[w1_col] = df_stress.set_index(['part_id', 'week']).index.map(mapping)
    else:
        print(f"  [WARN] {w2_col} not found in W-2 matrix, keeping W-1 value")

n_before = len(df_stress)
df_stress = df_stress.dropna(subset=ERP_W1_COLS)
n_after = len(df_stress)
print(f"\n  Rows after W-2 NaN drop: {n_after} (dropped {n_before - n_after})")

# Align to same rows
keys     = df_stress[['part_id', 'week']]
df_primary = pd.merge(df_primary, keys, on=['part_id', 'week'], how='inner')
df_primary = df_primary.sort_values('week').reset_index(drop=True)
df_stress  = df_stress.sort_values('week').reset_index(drop=True)

# Chronological 60/40 split (mirrors run_phase3_pipeline.py)
split_idx       = int(len(df_primary) * 0.6)
df_test_primary = df_primary.iloc[split_idx:].copy()
df_test_stress  = df_stress.iloc[split_idx:].copy()
print(f"Test set size: {len(df_test_primary)}")


def evaluate_per_family(df, label):
    """Apply per-family optimal threshold, same logic as run_phase3_pipeline.py P3-01."""
    X_raw  = df[features].values
    X_proc = imputer.transform(X_raw)
    if scaler is not None:
        X_proc = scaler.transform(X_proc)
    y_prob = model_obj.predict_proba(X_proc)[:, 1]
    df = df.copy()
    df['y_prob'] = y_prob

    y_pred_list, y_true_list = [], []
    for fam, grp in df.groupby('part_family'):
        th = optimal_thresholds.get(fam, 0.50)
        y_pred_list.extend((grp['y_prob'] >= th).astype(int).tolist())
        y_true_list.extend(grp['y2_shift1'].fillna(0).astype(int).tolist())

    y_pred = np.array(y_pred_list)
    y_true = np.array(y_true_list)

    prec = precision_score(y_true, y_pred, zero_division=0)
    rec  = recall_score(y_true, y_pred, zero_division=0)
    f1   = f1_score(y_true, y_pred, zero_division=0)
    print(f"\n  [{label}]")
    print(f"    Positives:  {int(y_true.sum())} / {len(y_true)}")
    print(f"    Precision:  {prec:.4f}")
    print(f"    Recall:     {rec:.4f}")
    print(f"    F1-score:   {f1:.4f}")
    return prec, rec, f1


print("\n" + "="*60)
print("FAIR COMPARISON: SAME MODEL + SAME TEST SET + SAME PER-FAMILY THRESHOLDS")
print("="*60)

prec_w1, rec_w1, f1_w1 = evaluate_per_family(df_test_primary, "W-1 Primary (ERP fresh)")
prec_w2, rec_w2, f1_w2 = evaluate_per_family(df_test_stress,  "W-2 Stress  (ERP stale, 1-week lag)")

print("\n" + "="*60)
print("DELTA (W-2 vs W-1)")
print("="*60)
delta_prec = (prec_w2 - prec_w1) / max(prec_w1, 1e-9) * 100
delta_rec  = (rec_w2  - rec_w1)  / max(rec_w1,  1e-9) * 100
delta_f1   = (f1_w2   - f1_w1)   / max(f1_w1,   1e-9) * 100
print(f"  Delta Precision: {delta_prec:+.1f}%")
print(f"  Delta Recall:    {delta_rec:+.1f}%")
print(f"  Delta F1-score:  {delta_f1:+.1f}%")

tier1_f1 = 0.1076
adv_w2   = (f1_w2 - tier1_f1) / tier1_f1 * 100
print(f"\n  Tier1 Rule-Based F1 (reference): {tier1_f1:.4f}")
print(f"  W-2 Stress advantage vs Tier1:   {adv_w2:+.1f}%")

print("\n" + "="*60)
print("SUMMARY FOR PAPER (Table 6)")
print("="*60)
print(f"  W-1 Primary  -> Prec={prec_w1:.4f}, Rec={rec_w1:.4f}, F1={f1_w1:.4f}")
print(f"  W-2 Stress   -> Prec={prec_w2:.4f}, Rec={rec_w2:.4f}, F1={f1_w2:.4f}")
print(f"  Delta F1     = {delta_f1:+.2f}%")
print(f"  W-2 vs Tier1 = {adv_w2:+.1f}% advantage")
print(f"\n  SANITY CHECK: W-1 should match Table 4 Tier3_XGB_SCRM (Prec=0.1654, Rec=0.3026, F1=0.2064)")
if abs(f1_w1 - 0.2064) < 0.005:
    print(f"  [PASS] W-1 F1={f1_w1:.4f} matches Table 4 within tolerance.")
else:
    print(f"  [WARN] W-1 F1={f1_w1:.4f} differs from Table 4 F1=0.2064 — check split/threshold consistency.")
