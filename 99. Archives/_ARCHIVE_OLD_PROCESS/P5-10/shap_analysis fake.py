"""
P5-10 | shap_analysis.py
SHAP feature importance analysis for the XGBoost model.

MOCK DATA NOTE:
  NLP features (news_risk_score, disruption_event_flag, severity_score)
  currently use MOCK random values.
  --> Replace with real values from P3-12 before final evaluation.

  If the XGBoost model (P5-08/xgb_model.json) does not exist, a small
  in-memory model is trained on dummy data for demonstration.

  shap is auto-installed if missing.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess

# --- Graceful shap install check ---
try:
    import shap
except ImportError:
    print("[INFO] shap not found — attempting pip install ...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'shap', '--quiet'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("[ERROR] Could not install shap automatically.")
        print(result.stderr)
        sys.exit(1)
    import shap
    print("[INFO] shap installed successfully.")

# --- Graceful xgboost install check ---
try:
    import xgboost as xgb
except ImportError:
    print("[INFO] xgboost not found — attempting pip install ...")
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'xgboost', '--quiet'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("[ERROR] Could not install xgboost automatically.")
        sys.exit(1)
    import xgboost as xgb

import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
MODEL_PATH  = BASE / 'P5-08' / 'xgb_model.json'
FEATURE_MATRIX_PATH = BASE / 'P5-01' / 'feature_matrix.parquet'
SHAP_CSV    = BASE / 'P5-10' / 'shap_values.csv'

ALL_FEATURES = [
    'burn_rate_daily',
    'TTS_days',
    'avg_delivery_delay',
    'pct_late_deliveries',
    'quality_incident_rate',
    'supplier_risk_class',
    'criticality_class',
    'news_risk_score',        # MOCK — replace with P3-12 output
    'disruption_event_flag',  # MOCK — replace with P3-12 output
    'severity_score',         # MOCK — replace with P3-12 output
]

NLP_FEATURES = ['news_risk_score', 'disruption_event_flag', 'severity_score']

TARGET   = 'y_true'
DATE_COL = 'week'


# ---------------------------------------------------------------------------
def generate_dummy_data(n_rows: int = 100, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        'burn_rate_daily':        rng.uniform(0.1, 5.0, n_rows),
        'TTS_days':               rng.uniform(0, 90, n_rows),
        'avg_delivery_delay':     rng.uniform(-2, 14, n_rows),
        'pct_late_deliveries':    rng.uniform(0, 1, n_rows),
        'quality_incident_rate':  rng.uniform(0, 0.5, n_rows),
        'supplier_risk_class':    rng.integers(0, 4, n_rows).astype(float),
        'criticality_class':      rng.integers(0, 3, n_rows).astype(float),
        'news_risk_score':        rng.uniform(0, 1, n_rows),        # MOCK
        'disruption_event_flag':  rng.integers(0, 2, n_rows).astype(float),  # MOCK
        'severity_score':         rng.uniform(0, 10, n_rows),       # MOCK
        TARGET:                   rng.integers(0, 2, n_rows),
    })


def load_or_train_model(X_train: np.ndarray, y_train: np.ndarray):
    """Load existing model or train a fresh one."""
    model = xgb.XGBClassifier(
        n_estimators=100, max_depth=4, learning_rate=0.1,
        use_label_encoder=False, eval_metric='logloss',
        random_state=42, verbosity=0,
    )
    if MODEL_PATH.exists():
        print(f"Loading model from {MODEL_PATH}")
        model.load_model(str(MODEL_PATH))
    else:
        print(f"[WARN] Model not found at {MODEL_PATH} — training on dummy data.")
        model.fit(X_train, y_train)
    return model


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-10 SHAP Feature Importance ===\n")
    print("[NOTE] NLP features (news_risk_score, disruption_event_flag, severity_score)")
    print("       are currently MOCK — replace with real values from P3-12\n")

    # Load or generate data (use last fold as test proxy)
    if FEATURE_MATRIX_PATH.exists():
        df = pd.read_parquet(FEATURE_MATRIX_PATH)
        df = df.rename(columns={'pct_late': 'pct_late_deliveries',
                                'severity_score_nlp': 'severity_score'})
        # Merge y_true
        y_path = BASE / 'P5-02' / 'y_true.parquet'
        if y_path.exists() and TARGET not in df.columns:
            y_df = pd.read_parquet(y_path)[['part_group','week','y_true']]
            df = df.merge(y_df, on=['part_group','week'], how='left')
            df[TARGET] = df[TARGET].fillna(0).astype(int)
        print(f"Loaded feature matrix: {df.shape}")
    else:
        print("[MOCK] Using dummy feature matrix.")
        df = generate_dummy_data(200)

    feat_cols = [c for c in ALL_FEATURES if c in df.columns]
    X = df[feat_cols].values.astype(float)
    y = df[TARGET].values.astype(int) if TARGET in df.columns else np.zeros(len(df), dtype=int)

    # Simple train/test split (last 20% as test)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = load_or_train_model(X_train, y_train)

    # SHAP analysis on test set
    print("Computing SHAP values ...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # If binary classification returns list, take the positive class
    if isinstance(shap_values, list):
        sv = shap_values[1]
    else:
        sv = shap_values

    mean_abs_shap = np.abs(sv).mean(axis=0)
    
        # Lấy đúng tên các cột mà X_df đang chứa (trừ cột target)
    actual_features = X_df.columns.tolist()

    importance_df = pd.DataFrame({
        'feature':        actual_features,
        'mean_abs_shap':  mean_abs_shap,
        'is_nlp_mock':    [f in NLP_FEATURES for f in actual_features],
    }).sort_values('mean_abs_shap', ascending=False).reset_index(drop=True)
    print("\nMean |SHAP| per feature (descending):")
    print("-" * 55)
    for _, row in importance_df.iterrows():
        mock_tag = "  [MOCK NLP]" if row['is_nlp_mock'] else ""
        print(f"  {row['feature']:<30} {row['mean_abs_shap']:.6f}{mock_tag}")
    print("-" * 55)

    # Save SHAP values per observation
    shap_df = pd.DataFrame(sv, columns=ALL_FEATURES)
    shap_df.insert(0, 'obs_index', range(len(shap_df)))

    SHAP_CSV.parent.mkdir(parents=True, exist_ok=True)
    shap_df.to_csv(SHAP_CSV, index=False, encoding='utf-8')
    print(f"\nSHAP values saved → {SHAP_CSV}")

    # Also save summary
    summary_path = BASE / 'P5-10' / 'shap_importance_summary.csv'
    importance_df.to_csv(summary_path, index=False, encoding='utf-8')
    print(f"SHAP importance summary saved → {summary_path}")
    print("\nP5-10 OK")
