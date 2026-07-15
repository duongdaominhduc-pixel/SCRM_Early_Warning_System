"""
P4-05 — 3D Soft Join: Time × Geography × Category
Links structured_risk_events (NLP Layer) to operational Feature Matrix.

Dimensions:
  T (Time):       event_week overlaps with [feature_week - WINDOW_WEEKS, feature_week]
  G (Geography):  event_country matches supplier_country for that part_id
  C (Category):   event_disruption_type relevant to part_family (via CATEGORY_MAP)

Output: event_match_flags per (part_id, week) row in Feature Matrix
  - news_risk_score: max severity_score of matched events (0 if no match)
  - disruption_event_flag: 1 if any event matched, else 0
  - severity_score: max severity_score matched (same as news_risk_score for now)

NOTE: structured_risk_events.csv is NOT yet available (waiting for P3-10 / DistilBERT).
      This script uses MOCK events with correct schema to validate join logic.
      Replace MOCK_EVENTS_PATH with real path when P3-12 handoff is done.
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')
P4_DIR = BASE / 'P4-05'
P4_DIR.mkdir(exist_ok=True)

# ── Config ────────────────────────────────────────────────────────────────────
WINDOW_WEEKS = 4   # look-back window: match events up to 4 weeks before feature week

# Category relevance map: disruption_type → part_families that are affected
CATEGORY_MAP = {
    'PORT_CONGESTION':      ['AEROSTRUCTURES', 'LANDING_GEAR', 'AVIONICS', 'HYDRAULICS', 'PROPULSION'],
    'GEOPOLITICAL':         ['AVIONICS', 'PROPULSION', 'ELECTRICAL'],
    'WEATHER_DISASTER':     ['AEROSTRUCTURES', 'LANDING_GEAR', 'AVIONICS', 'HYDRAULICS', 'PROPULSION', 'ELECTRICAL'],
    'LABOR_DISPUTE':        ['AEROSTRUCTURES', 'LANDING_GEAR', 'PROPULSION'],
    'SUPPLIER_FINANCIAL':   ['AVIONICS', 'HYDRAULICS', 'ELECTRICAL'],
    'GENERAL_DISRUPTION':   ['AEROSTRUCTURES', 'LANDING_GEAR', 'AVIONICS', 'HYDRAULICS', 'PROPULSION', 'ELECTRICAL'],
}

# ── Schema for structured_risk_events.csv (from P3-10) ───────────────────────
# Columns: event_id, publish_date, event_week (Period W), country (ISO alpha-2),
#          disruption_type, severity_score (0-10), predicted_label (1 or 2)

def load_events(events_path=None):
    """Load structured_risk_events.csv. If not found, return mock events."""
    if events_path and Path(events_path).exists():
        df = pd.read_csv(events_path)
        df['event_week'] = pd.PeriodIndex(df['event_week'], freq='W')
        print(f"Loaded real events: {len(df)} rows")
    else:
        print("WARNING: structured_risk_events.csv not found. Using MOCK events.")
        print("Replace with real data from P3-12 when DistilBERT training is complete.")
        np.random.seed(42)
        n = 50
        weeks = pd.period_range('2015-01', periods=52*3, freq='W')
        df = pd.DataFrame({
            'event_id':        range(n),
            'publish_date':    pd.date_range('2015-01-01', periods=n, freq='2W'),
            'event_week':      np.random.choice(weeks, n),
            'country':         np.random.choice(['US','CN','DE','FR','GB','JP','KR'], n),
            'disruption_type': np.random.choice(list(CATEGORY_MAP.keys()), n),
            'severity_score':  np.random.uniform(1, 10, n).round(2),
            'predicted_label': np.random.choice([1, 2], n, p=[0.7, 0.3]),
        })
    return df


def load_operational(base=BASE):
    """Load parts_master and supplier_locations for join keys."""
    parts_path   = base / 'P4-01' / 'parts_master.parquet'
    suppl_path   = base / 'P4-01' / 'supplier_locations.parquet'

    if parts_path.exists():
        parts = pd.read_parquet(parts_path)
    else:
        print("WARNING: parts_master.parquet not found. Using mock parts.")
        parts = pd.DataFrame({
            'part_id':              [f'P{i:03d}' for i in range(1, 11)],
            'part_family':          ['AVIONICS','AEROSTRUCTURES','HYDRAULICS','LANDING_GEAR',
                                     'PROPULSION','ELECTRICAL','AVIONICS','AEROSTRUCTURES',
                                     'HYDRAULICS','PROPULSION'],
            'supplier_id_primary':  [f'S{i:02d}' for i in range(1, 11)],
        })

    if suppl_path.exists():
        suppl = pd.read_parquet(suppl_path)
    else:
        print("WARNING: supplier_locations.parquet not found. Using mock suppliers.")
        suppl = pd.DataFrame({
            'supplier_id': [f'S{i:02d}' for i in range(1, 11)],
            'country':     ['US','CN','DE','FR','GB','JP','KR','US','CN','DE'],
        })

    return parts, suppl


def build_part_lookup(parts, suppl):
    """Build mapping: part_id → (part_family, supplier_country)."""
    merged = parts.merge(
        suppl[['supplier_id','country']],
        left_on='supplier_id_primary', right_on='supplier_id', how='left'
    )
    return merged.set_index('part_id')[['part_family','country']].rename(
        columns={'country': 'supplier_country'}
    )


def soft_join_3d(feature_rows: pd.DataFrame, events: pd.DataFrame,
                 part_lookup: pd.DataFrame) -> pd.DataFrame:
    """
    Perform 3D Soft Join for each (part_id, week) in feature_rows.

    Args:
        feature_rows: DataFrame with columns [part_id, week (Period W), ...]
        events: DataFrame with columns [event_week, country, disruption_type, severity_score]
        part_lookup: index=part_id, cols=[part_family, supplier_country]

    Returns:
        feature_rows with added columns: news_risk_score, disruption_event_flag, severity_score_nlp
    """
    results = []
    for _, row in feature_rows.iterrows():
        part_id = row['part_id']
        feat_week = row['week']

        if part_id not in part_lookup.index:
            results.append({'news_risk_score': 0.0, 'disruption_event_flag': 0, 'severity_score_nlp': 0.0})
            continue

        part_family      = part_lookup.loc[part_id, 'part_family']
        supplier_country = part_lookup.loc[part_id, 'supplier_country']

        # T: time window filter
        week_start = feat_week - WINDOW_WEEKS
        time_mask  = (events['event_week'] >= week_start) & (events['event_week'] <= feat_week)

        # G: geography filter
        geo_mask = events['country'] == supplier_country

        # C: category relevance filter
        def cat_relevant(dtype):
            relevant_families = CATEGORY_MAP.get(dtype, [])
            return part_family in relevant_families

        cat_mask = events['disruption_type'].apply(cat_relevant)

        matched = events[time_mask & geo_mask & cat_mask]

        if len(matched) == 0:
            results.append({'news_risk_score': 0.0, 'disruption_event_flag': 0, 'severity_score_nlp': 0.0})
        else:
            max_sev = matched['severity_score'].max()
            results.append({
                'news_risk_score':      float(max_sev),
                'disruption_event_flag': 1,
                'severity_score_nlp':   float(max_sev),
            })

    result_df = pd.DataFrame(results, index=feature_rows.index)
    return pd.concat([feature_rows, result_df], axis=1)


def main():
    print("=== P4-05: 3D Soft Join ===\n")

    # Load
    events      = load_events()   # mock until P3-12
    parts, suppl = load_operational()
    part_lookup  = build_part_lookup(parts, suppl)

    print(f"Events: {len(events)} | Parts: {len(parts)} | Suppliers: {len(suppl)}")
    print(f"Part lookup sample:\n{part_lookup.head()}\n")

    # Build dummy feature_rows (will be replaced by real Feature Matrix from P5-01)
    np.random.seed(42)
    weeks   = pd.period_range('2015-01', periods=52*3, freq='W')
    part_ids = list(part_lookup.index)[:min(5, len(part_lookup))]
    feature_rows = pd.DataFrame([
        {'part_id': p, 'week': w}
        for p in part_ids
        for w in np.random.choice(weeks, 10, replace=False)
    ])

    print(f"Feature rows to join: {len(feature_rows)}")
    result = soft_join_3d(feature_rows, events, part_lookup)

    match_rate = result['disruption_event_flag'].mean()
    print(f"\nMatch rate: {match_rate:.1%} of (part, week) pairs matched at least 1 event")
    print(f"Mean severity when matched: {result[result['disruption_event_flag']==1]['severity_score_nlp'].mean():.2f}")
    print(f"\nSample output:\n{result.head(10).to_string()}")

    out_path = P4_DIR / 'soft_join_mock_output.parquet'
    result.to_parquet(out_path, index=False)
    print(f"\nSaved mock output → {out_path}")
    print("\nNOTE: Replace mock events with real structured_risk_events.csv from P3-12.")


if __name__ == '__main__':
    main()
