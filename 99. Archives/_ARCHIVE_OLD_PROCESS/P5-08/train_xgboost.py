"""
P5-08 | train_xgboost.py
XGBoost main model — trained on all 10 features (operational + NLP mock).

MOCK DATA NOTE:
  Features 8-10 (news_risk_score, disruption_event_flag, severity_score)
  are MOCK random values.  Replace with real outputs from P3-12 before
  running the final evaluation.

  If xgboost is not installed, this script attempts to install it via pip.
  If P5-01/feature_matrix.parquet does not exist, a 200-row synthetic
  DataFrame is generated.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess, importlib

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
        print(result.stderr)
        sys.exit(1)
    import xgboost as xgb
    print("[INFO] xgboost installed successfully.")

import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.metrics import (recall_score, precision_score, f1_score,
                             roc_auc_score)

# ---------------------------------------------------------------------------
BASE = Path(r'/Users/lelinh/Documents/BBKH')
FEATURE_MATRIX_PATH = BASE / 'P5-01' / 'feature_matrix.parquet'
MODEL_PATH   = BASE / 'P5-08' / 'xgb_model.json'
RESULTS_PATH = BASE / 'P5-08' / 'xgb_results.json'

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

TARGET   = 'y_true'
DATE_COL = 'week'


# ---------------------------------------------------------------------------
def generate_dummy_feature_matrix(n_rows: int = 200, seed: int = 42):
    rng = np.random.default_rng(seed)
    n_weeks = 40
    n_parts = max(1, n_rows // n_weeks)
    weeks = pd.date_range('2022-01-03', periods=n_weeks, freq='W-MON')
    rows = []
    for w in weeks:
        for p in range(n_parts):
            rows.append({
                DATE_COL: w,
                'part_group': f'PG-{p:03d}',
                'burn_rate_daily': rng.uniform(0.1, 5.0),
                'TTS_days': rng.uniform(0, 90),
                'avg_delivery_delay': rng.uniform(-2, 14),
                'pct_late_deliveries': rng.uniform(0, 1),
                'quality_incident_rate': rng.uniform(0, 0.5),
                'supplier_risk_class': rng.integers(0, 4),
                'criticality_class': rng.integers(0, 3),
                'news_risk_score': rng.uniform(0, 1),        # MOCK
                'disruption_event_flag': rng.integers(0, 2), # MOCK
                'severity_score': rng.uniform(0, 10),        # MOCK
                TARGET: int(rng.random() < 0.15),
            })
    df = pd.DataFrame(rows).head(n_rows)
    print(f"[MOCK] Generated dummy feature matrix: {df.shape}")
    return df


def load_feature_matrix():
    if FEATURE_MATRIX_PATH.exists():
        print(f"Loading feature matrix from {FEATURE_MATRIX_PATH}")
        df = pd.read_parquet(FEATURE_MATRIX_PATH)
        df = df.rename(columns={'pct_late': 'pct_late_deliveries',
                                'severity_score_nlp': 'severity_score'})
        y_path = BASE / 'P5-02' / 'y_true.parquet'
        if y_path.exists() and 'y_true' not in df.columns:
            y = pd.read_parquet(y_path)[['part_group','week','y_true']]
            df = df.merge(y, on=['part_group','week'], how='left')
            df['y_true'] = df['y_true'].fillna(0).astype(int)
            print(f"Merged y_true: positive rate = {df['y_true'].mean():.1%}")
        elif 'y_true' not in df.columns:
            import numpy as np
            df['y_true'] = (np.random.default_rng(42).random(len(df)) < 0.15).astype(int)
        return df
    else:
        print(f"[WARN] {FEATURE_MATRIX_PATH} not found — using dummy data.")
        return generate_dummy_feature_matrix()


# ---------------------------------------------------------------------------
def compute_scale_pos_weight(y: np.ndarray) -> float:
    """Return n_neg / n_pos for class-imbalance handling."""
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    if n_pos == 0:
        return 1.0
    return float(n_neg / n_pos)


def run_xgboost(df: pd.DataFrame) -> dict:
    # Load WalkForwardCV
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'walk_forward_cv',
        BASE / 'P5-06' / 'walk_forward_cv.py'
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    WalkForwardCV = mod.WalkForwardCV

    cv = WalkForwardCV(n_folds=5, fold_size_weeks=13)
    folds = cv.split(df, date_col=DATE_COL)

    fold_results = []
    best_auc = -1.0
    best_model = None

    for i, (tr_idx, te_idx) in enumerate(folds):
        train = df.iloc[tr_idx]
        test  = df.iloc[te_idx]

        X_train = train[ALL_FEATURES].values.astype(float)
        y_train = train[TARGET].values.astype(int)
        X_test  = test[ALL_FEATURES].values.astype(float)
        y_test  = test[TARGET].values.astype(int)

        if len(np.unique(y_train)) < 2:
            print(f"  Fold {i+1}: skipped (only one class in train)")
            continue

        spw = compute_scale_pos_weight(y_train)

        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            scale_pos_weight=spw,
            use_label_encoder=False,
            eval_metric='logloss',
            random_state=42,
            verbosity=0,
        )
        model.fit(X_train, y_train)
        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        if len(np.unique(y_test)) < 2:
            auc = float('nan')
        else:
            auc = roc_auc_score(y_test, y_proba)

        metrics = {
            'fold': i + 1,
            'recall':    round(recall_score(y_test, y_pred, zero_division=0), 4),
            'precision': round(precision_score(y_test, y_pred, zero_division=0), 4),
            'f1':        round(f1_score(y_test, y_pred, zero_division=0), 4),
            'auc':       round(auc, 4) if not np.isnan(auc) else None,
            'scale_pos_weight': round(spw, 2),
        }
        fold_results.append(metrics)
        print(f"  Fold {i+1}: Recall={metrics['recall']:.4f}  "
              f"Precision={metrics['precision']:.4f}  "
              f"F1={metrics['f1']:.4f}  AUC={metrics['auc']}  "
              f"SPW={spw:.1f}")

        if metrics['auc'] is not None and metrics['auc'] > best_auc:
            best_auc = metrics['auc']
            best_model = model

    # Averages
    valid = [r for r in fold_results if r['auc'] is not None]
    avg = {
        'recall':    round(np.mean([r['recall']    for r in fold_results]), 4),
        'precision': round(np.mean([r['precision'] for r in fold_results]), 4),
        'f1':        round(np.mean([r['f1']        for r in fold_results]), 4),
        'auc':       round(np.mean([r['auc']       for r in valid]), 4) if valid else None,
    }
    print(f"\n  AVG  : Recall={avg['recall']:.4f}  "
          f"Precision={avg['precision']:.4f}  "
          f"F1={avg['f1']:.4f}  AUC={avg['auc']}")

    # Save best model
    if best_model is not None:
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        best_model.save_model(str(MODEL_PATH))
        print(f"\nBest model (AUC={best_auc:.4f}) saved → {MODEL_PATH}")

    return {
        'model': 'XGBoost',
        'features': ALL_FEATURES,
        'nlp_features_mock': True,  # remove when P3-12 is integrated
        'folds': fold_results,
        'avg': avg,
    }


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-08 XGBoost Main Model ===\n")
    print("[NOTE] NLP features (8-10) are MOCK — replace with P3-12 output\n")

    df = load_feature_matrix()
    print(f"Dataset: {df.shape[0]} rows, {df[DATE_COL].nunique()} unique weeks\n")

    results = run_xgboost(df)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Results saved → {RESULTS_PATH}")

    # Export predictions from last fold for P5-11/12/13
    import importlib.util
    spec = importlib.util.spec_from_file_location('wf', BASE / 'P5-06' / 'walk_forward_cv.py')
    mod  = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    cv   = mod.WalkForwardCV(n_folds=5, fold_size_weeks=13)
    folds = cv.split(df, date_col=DATE_COL)
    last_tr, last_te = folds[-1]
    import xgboost as xgb
    from sklearn.preprocessing import LabelEncoder
    feat_cols = [c for c in ALL_FEATURES if c in df.columns]
    le = LabelEncoder()
    df2 = df.copy()
    for c in df2.columns:
        if str(df2[c].dtypes) == 'object':
            df2[c] = df2[c].astype(str)
    X_te = df2.iloc[last_te][feat_cols].values.astype(float)
    y_te = df2.iloc[last_te][TARGET].values
    best = xgb.XGBClassifier(); best.load_model(str(MODEL_PATH))
    probs = best.predict_proba(X_te)[:,1]
    pred_df = df.iloc[last_te][['part_group', DATE_COL]].copy()
    pred_df['y_true']    = y_te
    pred_df['risk_score'] = probs
    pred_df.to_csv(BASE / 'P5-08' / 'xgb_predictions.csv', index=False, encoding='utf-8-sig')
    print(f"Predictions exported → P5-08/xgb_predictions.csv ({len(pred_df)} rows)")
    print("\nP5-08 OK")
