"""
P5-13 | lead_time_warning.py
Lead Time of Warning (LTW) metric.

For each true positive (alert raised AND actual disruption confirmed), compute
the number of weeks between the alert week and the actual disruption week.

MOCK DATA NOTE:
  If weekly_alerts.csv does not exist, a mock dataset is generated that
  simulates true positives with randomly distributed lead times.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import json
import numpy as np
import pandas as pd
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
ALERTS_CSV   = BASE / 'P5-12' / 'weekly_alerts.csv'
OUTPUT_JSON  = BASE / 'P5-13' / 'lead_time_results.json'


# ---------------------------------------------------------------------------
def generate_mock_alerts(n_parts: int = 10, n_weeks: int = 30,
                         seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic alert + disruption data.

    Each part_group has at most one 'disruption week'.  Alerts may fire
    1-4 weeks before the disruption (true positives) or randomly (false
    positives/negatives).
    """
    rng = np.random.default_rng(seed)
    weeks = pd.date_range('2023-01-02', periods=n_weeks, freq='W-MON')
    rows = []
    for p in range(n_parts):
        # Pick a disruption week for this part (or None)
        has_disruption = rng.random() < 0.7
        if has_disruption:
            disrupt_idx = rng.integers(5, n_weeks)
        else:
            disrupt_idx = -1

        for wi, w in enumerate(weeks):
            y_true = 1 if wi == disrupt_idx else 0
            # True positive: alert fires 1-4 weeks before disruption
            if has_disruption and disrupt_idx - 4 <= wi < disrupt_idx:
                alert = 1
                score = float(rng.beta(5, 2))
            elif y_true == 1:
                alert = int(rng.random() < 0.6)  # might miss
                score = float(rng.beta(4, 2))
            else:
                alert = int(rng.random() < 0.08)  # FP rate
                score = float(rng.beta(2, 5))
            rows.append({
                'part_group':       f'PG-{p:03d}',
                'week':             w,
                'risk_score':       round(score, 6),
                'y_true':           y_true,
                'alert_level':      alert,
                'threshold_used':   0.40,
                'disruption_week':  weeks[disrupt_idx] if has_disruption else pd.NaT,
            })
    print(f"[MOCK] Generated {len(rows)} alert rows across {n_parts} part groups.")
    return pd.DataFrame(rows)


def load_alerts() -> pd.DataFrame:
    if ALERTS_CSV.exists():
        df = pd.read_csv(ALERTS_CSV)
        # week column is "YYYY-MM-DD/YYYY-MM-DD" period format — extract start date
        df['week'] = df['week'].str.split('/').str[0]
        df['week'] = pd.to_datetime(df['week'], errors='coerce')
        print(f"Loaded alerts: {ALERTS_CSV}  ({len(df)} rows)")
        # If disruption_week column is absent, infer from y_true
        if 'disruption_week' not in df.columns:
            # Map each part_group to its actual disruption week(s)
            disrupt_map = (
                df[df['y_true'] == 1]
                .groupby('part_group')['week']
                .min()
                .to_dict()
            )
            df['disruption_week'] = df['part_group'].map(disrupt_map)
        return df
    else:
        print(f"[WARN] {ALERTS_CSV} not found — using mock alerts.")
        return generate_mock_alerts()


# ---------------------------------------------------------------------------
def compute_lead_time(df: pd.DataFrame) -> dict:
    """
    For each row where alert_level==1 AND y_true eventually becomes 1
    (i.e., there is a disruption week for that part), compute the lead
    time in weeks = (disruption_week - alert_week).

    Only positive lead times are counted (alert must fire *before* the
    disruption to be meaningful).
    """
    # Ensure datetime
    df['week'] = pd.to_datetime(df['week'])
    if 'disruption_week' in df.columns:
        df['disruption_week'] = pd.to_datetime(df['disruption_week'])

    # True positives: alert raised AND there is a disruption for this part
    if 'disruption_week' not in df.columns:
        print("[WARN] No disruption_week column — using y_true==1 as disruption proxy.")
        # Fallback: only compute for rows where alert==1 and y_true==1 (same week)
        tp_df = df[(df['alert_level'] == 1) & (df['y_true'] == 1)].copy()
        tp_df['lead_time_weeks'] = 0
    else:
        alerted = df[(df['alert_level'] == 1) &
                     (df['disruption_week'].notna())].copy()
        alerted['lead_time_weeks'] = (
            (alerted['disruption_week'] - alerted['week'])
            .dt.days / 7
        ).round(1)
        # Only forward-looking alerts
        tp_df = alerted[alerted['lead_time_weeks'] > 0].copy()

    if tp_df.empty:
        print("[WARN] No true positives with positive lead time found.")
        return {
            'n_true_positives': 0,
            'mean_lead_time_weeks':   None,
            'median_lead_time_weeks': None,
            'min_lead_time_weeks':    None,
            'max_lead_time_weeks':    None,
        }

    lt = tp_df['lead_time_weeks']
    result = {
        'n_true_positives':       int(len(tp_df)),
        'mean_lead_time_weeks':   round(float(lt.mean()),   2),
        'median_lead_time_weeks': round(float(lt.median()), 2),
        'min_lead_time_weeks':    round(float(lt.min()),    2),
        'max_lead_time_weeks':    round(float(lt.max()),    2),
    }
    return result


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-13 Lead Time of Warning (LTW) ===\n")

    df = load_alerts()
    result = compute_lead_time(df)

    print("\nLead Time of Warning Results:")
    print(f"  True positives with positive LTW : {result['n_true_positives']}")
    print(f"  Mean LTW (weeks)                 : {result['mean_lead_time_weeks']}")
    print(f"  Median LTW (weeks)               : {result['median_lead_time_weeks']}")
    print(f"  Min LTW (weeks)                  : {result['min_lead_time_weeks']}")
    print(f"  Max LTW (weeks)                  : {result['max_lead_time_weeks']}")

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)
    print(f"\nLead time results saved → {OUTPUT_JSON}")
    print("\nP5-13 OK")
