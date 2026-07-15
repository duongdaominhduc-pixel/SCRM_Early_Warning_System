"""
P5-01 — Build Feature Matrix X (10 features per part_group × week)

Feature Matrix schema:
  Index: (part_group, week)
  Operational (from Phase 4):
    1. burn_rate_daily       — avg daily consumption
    2. TTS_days              — time-to-survive in days
    3. avg_delivery_delay    — avg days late from supplier
    4. pct_late_deliveries   — % of POs arriving late
    5. quality_incident_rate — incidents per 100 POs
    6. supplier_risk_class   — encoded (0=low,1=med,2=high)
    7. criticality_class     — encoded (0=low,1=med,2=high)
  NLP (from Phase 3 / P4-05 Soft Join):
    8.  news_risk_score       — max severity_score from matched events
    9.  disruption_event_flag — 0/1
    10. severity_score_nlp    — alias for news_risk_score

NOTE: NLP features 8-10 currently MOCK (random values in correct range).
      Replace by running P4-05 soft_join_3d.py on real structured_risk_events.csv from P3-12.

part_group = part_family (6 groups: AVIONICS, AEROSTRUCTURES, HYDRAULICS, LANDING_GEAR, PROPULSION, ELECTRICAL)
"""

import sys, json
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE  = Path(r'/Users/lelinh/Documents/BBKH')
OUT   = BASE / 'P5-01'
OUT.mkdir(exist_ok=True)

RISK_CLASS_MAP = {'low': 0, 'medium': 1, 'high': 2, 'Low': 0, 'Medium': 1, 'High': 2}
CRIT_MAP       = {'low': 0, 'medium': 1, 'high': 2, 'Low': 0, 'Medium': 1, 'High': 2}
PART_GROUPS    = ['AVIONICS','AEROSTRUCTURES','HYDRAULICS','LANDING_GEAR','PROPULSION','ELECTRICAL']


def load_parts_master():
    path = BASE / 'P4-01' / 'parts_master.parquet'
    if path.exists():
        return pd.read_parquet(path)[['part_id','part_family','supplier_risk_class','criticality_class']]
    return pd.DataFrame({
        'part_id':            [f'P{i:05d}' for i in range(1, 11)],
        'part_family':        PART_GROUPS[:6] + PART_GROUPS[:4],
        'supplier_risk_class':['Low']*5+['High']*5,
        'criticality_class':  ['High']*3+['Medium']*4+['Low']*3,
    })


def load_or_mock_tts():
    """Real: part_id×site_id×week. Aggregate to part_family×week."""
    path = BASE / 'P4-02' / 'tts_weekly.parquet'
    pm   = load_parts_master()
    if path.exists():
        df = pd.read_parquet(path)
        # cols: part_id, site_id, week, mean_TTS_days, mean_burn_rate_daily
        df = df.merge(pm[['part_id','part_family']], on='part_id', how='left')
        df = df.groupby(['part_family','week']).agg(
            TTS_days=('mean_TTS_days','mean'),
            burn_rate_daily=('mean_burn_rate_daily','mean'),
        ).reset_index().rename(columns={'part_family':'part_group'})
        return df
    print("WARNING: tts_weekly.parquet not found — using mock TTS data")
    np.random.seed(42)
    weeks = pd.period_range('2015-01', periods=52*3, freq='W')
    records = [{'part_group':pg,'week':w,'burn_rate_daily':np.random.uniform(0.5,5.0),
                'TTS_days':np.random.uniform(7,90)} for pg in PART_GROUPS for w in weeks]
    return pd.DataFrame(records)


def load_or_mock_delays():
    """Real: supplier_id×part_id×week. Aggregate to part_family×week."""
    path = BASE / 'P4-03' / 'delivery_delays_weekly.parquet'
    pm   = load_parts_master()
    if path.exists():
        df = pd.read_parquet(path)
        # cols: supplier_id, part_id, week_of_promised_date, avg_delay, pct_late
        df = df.merge(pm[['part_id','part_family']], on='part_id', how='left')
        df = df.groupby(['part_family','week_of_promised_date']).agg(
            avg_delivery_delay=('avg_delay','mean'),
            pct_late=('pct_late','mean'),
        ).reset_index().rename(columns={'part_family':'part_group','week_of_promised_date':'week'})
        return df
    print("WARNING: delivery_delays_weekly.parquet not found — using mock delay data")
    np.random.seed(43)
    weeks = pd.period_range('2015-01', periods=52*3, freq='W')
    records = [{'part_group':pg,'week':w,'avg_delivery_delay':np.random.uniform(-2,15),
                'pct_late':np.random.uniform(0,0.6)} for pg in PART_GROUPS for w in weeks]
    return pd.DataFrame(records)


def load_or_mock_quality():
    path = BASE / 'P4-01' / 'quality_incidents.parquet'
    po_path = BASE / 'P4-01' / 'purchase_orders.parquet'
    if path.exists() and po_path.exists():
        qi = pd.read_parquet(path)
        po = pd.read_parquet(po_path)
        # Compute incidents per 100 POs per (part_group, week)
        # Simplified: aggregate by week
        return None  # placeholder — real logic in full implementation
    print("WARNING: quality data not found — using mock quality_incident_rate")
    np.random.seed(44)
    weeks = pd.period_range('2015-01', periods=52*3, freq='W')
    records = []
    for pg in PART_GROUPS:
        for w in weeks:
            records.append({
                'part_group':            pg,
                'week':                  w,
                'quality_incident_rate': np.random.uniform(0, 5),
            })
    return pd.DataFrame(records)


def load_or_mock_part_attrs():
    pm = load_parts_master()
    if 'supplier_risk_class' in pm.columns:
        pm['supplier_risk_enc'] = pm['supplier_risk_class'].map(RISK_CLASS_MAP).fillna(1).astype(int)
        pm['criticality_enc']   = pm['criticality_class'].map(CRIT_MAP).fillna(1).astype(int)
        return pm.groupby('part_family').agg(
            supplier_risk_class=('supplier_risk_enc', lambda x: x.mode().iloc[0]),
            criticality_class=('criticality_enc', lambda x: x.mode().iloc[0]),
        ).reset_index().rename(columns={'part_family': 'part_group'})
    return pd.DataFrame({
        'part_group': PART_GROUPS,
        'supplier_risk_class': [0,1,2,1,2,0],
        'criticality_class':   [2,1,2,1,2,0],
    })


def load_or_mock_nlp_features():
    """NLP features from P4-05 soft join. Mock until structured_risk_events.csv is available."""
    path = BASE / 'P4-05' / 'soft_join_output.parquet'
    if path.exists():
        df = pd.read_parquet(path)
        # Group by part_group × week
        return df
    print("WARNING: soft_join_output.parquet not found — using MOCK NLP features (random)")
    print("  → Replace when P3-12 handoff is complete")
    np.random.seed(45)
    weeks = pd.period_range('2015-01', periods=52*3, freq='W')
    records = []
    for pg in PART_GROUPS:
        for w in weeks:
            flag = np.random.choice([0, 1], p=[0.85, 0.15])
            records.append({
                'part_group':           pg,
                'week':                 w,
                'news_risk_score':      np.random.uniform(0, 10) if flag else 0.0,
                'disruption_event_flag': flag,
                'severity_score_nlp':   np.random.uniform(0, 10) if flag else 0.0,
            })
    return pd.DataFrame(records)


def build_feature_matrix():
    print("=== P5-01: Build Feature Matrix X ===\n")

    tts     = load_or_mock_tts()
    delays  = load_or_mock_delays()
    quality = load_or_mock_quality()
    attrs   = load_or_mock_part_attrs()
    nlp     = load_or_mock_nlp_features()

    # Ensure part_group column in tts and delays
    if 'part_family' in tts.columns and 'part_group' not in tts.columns:
        tts = tts.rename(columns={'part_family': 'part_group'})
    if 'part_family' in delays.columns and 'part_group' not in delays.columns:
        delays = delays.rename(columns={'part_family': 'part_group'})

    # Normalize week to string across all tables
    for df in [tts, delays, nlp]:
        if df is not None and 'week' in df.columns:
            df['week'] = df['week'].astype(str)
    if quality is not None and 'week' in quality.columns:
        quality['week'] = quality['week'].astype(str)

    # Merge operational features
    X = tts[['part_group','week','burn_rate_daily','TTS_days']].copy()
    X = X.merge(delays[['part_group','week','avg_delivery_delay','pct_late']], on=['part_group','week'], how='left')
    if quality is not None:
        X = X.merge(quality[['part_group','week','quality_incident_rate']], on=['part_group','week'], how='left')
    else:
        X['quality_incident_rate'] = np.nan

    # Add static part attributes (same for all weeks)
    X = X.merge(attrs[['part_group','supplier_risk_class','criticality_class']], on='part_group', how='left')

    # Add NLP features
    X = X.merge(nlp[['part_group','week','news_risk_score','disruption_event_flag','severity_score_nlp']],
                on=['part_group','week'], how='left')

    # Fill NaNs
    X['quality_incident_rate']  = X['quality_incident_rate'].fillna(0)
    X['news_risk_score']         = X['news_risk_score'].fillna(0)
    X['disruption_event_flag']   = X['disruption_event_flag'].fillna(0).astype(int)
    X['severity_score_nlp']      = X['severity_score_nlp'].fillna(0)
    X['avg_delivery_delay']      = X['avg_delivery_delay'].fillna(0)
    X['pct_late']                = X['pct_late'].fillna(0)

    # Sort chronologically
    X = X.sort_values(['part_group','week']).reset_index(drop=True)

    print(f"Feature Matrix shape: {X.shape}")
    print(f"Part groups: {X['part_group'].unique().tolist()}")
    print(f"Week range: {X['week'].min()} → {X['week'].max()}")
    print(f"\nFeature stats:\n{X.describe().round(3)}")

    # Save
    # Convert Period to string for parquet compatibility
    X['week'] = X['week'].astype(str)
    X.to_parquet(OUT / 'feature_matrix.parquet', index=False)
    X.to_csv(OUT / 'feature_matrix.csv', index=False, encoding='utf-8-sig')
    print(f"\nSaved → P5-01/feature_matrix.parquet ({len(X)} rows × {len(X.columns)} cols)")

    # Save schema
    schema = {col: str(dtype) for col, dtype in X.dtypes.items()}
    with open(OUT / 'feature_matrix_schema.json', 'w') as f:
        import json
        json.dump(schema, f, indent=2)

    return X


if __name__ == '__main__':
    build_feature_matrix()
