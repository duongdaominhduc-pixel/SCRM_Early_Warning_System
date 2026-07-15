"""
P5-07 | train_baseline.py
Logistic Regression baseline — trained on operational features only (1-7).

MOCK DATA NOTE:
  If P5-01/feature_matrix.parquet does not exist, a 200-row synthetic
  DataFrame is generated with the correct 10-feature schema.
  Features 8-10 (news_risk_score, disruption_event_flag, severity_score)
  are generated as random numbers for schema completeness but are NOT
  used in this baseline model.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (recall_score, precision_score, f1_score,
                             roc_auc_score)
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
BASE = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')
FEATURE_MATRIX_PATH = BASE / 'P5-01' / 'feature_matrix.parquet'
RESULTS_PATH = BASE / 'P5-07' / 'baseline_results.json'

# Operational features only (indices 0-6 in the feature list below)
OPERATIONAL_FEATURES = [
    'burn_rate_daily',
    'TTS_days',
    'avg_delivery_delay',
    'pct_late_deliveries',
    'quality_incident_rate',
    'supplier_risk_class',
    'criticality_class',
]

ALL_FEATURES = OPERATIONAL_FEATURES + [
    'news_risk_score',        # MOCK — replace with P3-12 output
    'disruption_event_flag',  # MOCK — replace with P3-12 output
    'severity_score',         # MOCK — replace with P3-12 output
]

TARGET = 'y_true'
DATE_COL = 'week'


# ---------------------------------------------------------------------------
def generate_dummy_feature_matrix(n_rows: int = 200,
                                  seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic feature matrix with correct schema."""
    rng = np.random.default_rng(seed)
    n_weeks = 40
    n_parts = n_rows // n_weeks + 1
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


def load_feature_matrix() -> pd.DataFrame:
    if FEATURE_MATRIX_PATH.exists():
        print(f"Loading feature matrix from {FEATURE_MATRIX_PATH}")
        df = pd.read_parquet(FEATURE_MATRIX_PATH)
        df = df.rename(columns={'pct_late': 'pct_late_deliveries',
                                'severity_score_nlp': 'severity_score'})
        # Merge y_true from P5-02 if available
        y_path = BASE / 'P5-02' / 'y_true.parquet'
        if y_path.exists() and 'y_true' not in df.columns:
            y = pd.read_parquet(y_path)[['part_group','week','y_true']]
            y.columns = ['part_group','week','y_true']
            df = df.merge(y, on=['part_group','week'], how='left')
            df['y_true'] = df['y_true'].fillna(0).astype(int)
            print(f"Merged y_true: positive rate = {df['y_true'].mean():.1%}")
        elif 'y_true' not in df.columns:
            import numpy as np
            df['y_true'] = (np.random.default_rng(42).random(len(df)) < 0.15).astype(int)
            print("[WARN] y_true not found — using random mock labels")
        return df
    else:
        print(f"[WARN] {FEATURE_MATRIX_PATH} not found — using dummy data.")
        return generate_dummy_feature_matrix()


# ---------------------------------------------------------------------------
def run_baseline(df: pd.DataFrame) -> dict:
    """Run walk-forward CV with Logistic Regression on operational features."""
    # Import WalkForwardCV from sibling folder
    import importlib.util, sys as _sys
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
    for i, (tr_idx, te_idx) in enumerate(folds):
        train = df.iloc[tr_idx]
        test  = df.iloc[te_idx]

        X_train = train[OPERATIONAL_FEATURES].values
        y_train = train[TARGET].values
        X_test  = test[OPERATIONAL_FEATURES].values
        y_test  = test[TARGET].values

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test  = scaler.transform(X_test)

        # Handle edge case: only one class in train
        if len(np.unique(y_train)) < 2:
            print(f"  Fold {i+1}: skipped (only one class in train)")
            continue

        model = LogisticRegression(class_weight='balanced', max_iter=1000,
                                   random_state=42)
        model.fit(X_train, y_train)
        y_pred  = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]

        # Guard: AUC requires both classes in test
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
        }
        fold_results.append(metrics)
        print(f"  Fold {i+1}: Recall={metrics['recall']:.4f}  "
              f"Precision={metrics['precision']:.4f}  "
              f"F1={metrics['f1']:.4f}  AUC={metrics['auc']}")

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

    return {'model': 'LogisticRegression_baseline',
            'features': OPERATIONAL_FEATURES,
            'folds': fold_results,
            'avg': avg}


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-07 Baseline (Logistic Regression) ===\n")
    df = load_feature_matrix()
    print(f"Dataset: {df.shape[0]} rows, {df[DATE_COL].nunique()} unique weeks\n")

    results = run_baseline(df)

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved → {RESULTS_PATH}")
    print("\nP5-07 OK")
