"""
P5-12 | generate_alerts.py
Apply the optimal threshold to XGBoost risk scores and emit weekly alerts.

MOCK DATA NOTE:
  If prediction CSV or threshold JSON are absent, mock versions are used.
  NLP-derived risk scores are MOCK until P3-12 is integrated.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
PREDS_CSV       = BASE / 'P5-08' / 'xgb_predictions.csv'
THRESHOLD_JSON  = BASE / 'P5-11' / 'optimal_threshold.json'
ALERTS_CSV      = BASE / 'P5-12' / 'weekly_alerts.csv'

TARGET    = 'y_true'
SCORE_COL = 'risk_score'


# ---------------------------------------------------------------------------
def generate_mock_predictions(n: int = 200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n_weeks  = 20
    n_parts  = max(1, n // n_weeks)
    weeks    = pd.date_range('2023-01-02', periods=n_weeks, freq='W-MON')
    rows = []
    for w in weeks:
        for p in range(n_parts):
            y = int(rng.random() < 0.15)
            score = float(
                rng.beta(5, 2) if y == 1 else rng.beta(2, 5)
            )
            rows.append({
                'part_group':  f'PG-{p:03d}',
                'week':        w,
                TARGET:        y,
                SCORE_COL:     round(score, 6),
            })
    df = pd.DataFrame(rows).head(n)
    print(f"[MOCK] Generated {len(df)} prediction rows.")
    return df


def load_predictions() -> pd.DataFrame:
    if PREDS_CSV.exists():
        print(f"Loading predictions: {PREDS_CSV}")
        return pd.read_csv(PREDS_CSV, parse_dates=['week'])
    else:
        print(f"[WARN] {PREDS_CSV} not found — using mock predictions.")
        return generate_mock_predictions()


def load_threshold() -> float:
    if THRESHOLD_JSON.exists():
        with open(THRESHOLD_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        t = float(data['threshold'])
        print(f"Loaded optimal threshold: {t:.4f}  (Youden's J={data.get('youdens_j')})")
        return t
    else:
        fallback = 0.40
        print(f"[WARN] {THRESHOLD_JSON} not found — using fallback threshold {fallback}.")
        return fallback


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-12 Generate Weekly Alerts ===\n")

    df        = load_predictions()
    threshold = load_threshold()

    # Apply threshold
    df['alert_level']    = (df[SCORE_COL] >= threshold).astype(int)
    df['threshold_used'] = threshold

    # Select and order output columns
    out_cols = ['part_group', 'week', SCORE_COL, 'alert_level', 'threshold_used']
    # Add y_true if present (useful for evaluation)
    if TARGET in df.columns:
        out_cols.insert(3, TARGET)

    alerts_df = df[out_cols].copy()

    print(f"\nAlert summary:")
    print(f"  Total observations : {len(alerts_df)}")
    print(f"  Alerts raised (1)  : {alerts_df['alert_level'].sum()}")
    print(f"  No alert (0)       : {(alerts_df['alert_level']==0).sum()}")
    print(f"  Alert rate         : {alerts_df['alert_level'].mean():.3f}")

    ALERTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    alerts_df.to_csv(ALERTS_CSV, index=False, encoding='utf-8')
    print(f"\nWeekly alerts saved → {ALERTS_CSV}")
    print("\nP5-12 OK")
