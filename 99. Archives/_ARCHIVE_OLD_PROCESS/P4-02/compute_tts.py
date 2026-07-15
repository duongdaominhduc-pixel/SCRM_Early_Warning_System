import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
IN_FILE = BASE / 'P4-01' / 'supply_chain_history.parquet'
OUT_DIR = BASE / 'P4-02'
OUT_DIR.mkdir(exist_ok=True)

try:
    import pandas as pd
    import numpy as np
    import pyarrow  # noqa: F401
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'pyarrow', 'numpy'])
    import pandas as pd
    import numpy as np

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
print("Loading supply_chain_history.parquet ...")
sch = pd.read_parquet(IN_FILE)

# Restore date dtype if stored as string
if sch['date'].dtype == object:
    sch['date'] = pd.to_datetime(sch['date'])

# Restore week as period
if sch['week'].dtype == object:
    sch['week'] = sch['week'].apply(lambda x: pd.Period(x, freq='W') if pd.notna(x) else pd.NaT)

print(f"  Rows loaded: {len(sch):,}")

# ---------------------------------------------------------------------------
# Rolling 4-week burn_rate_daily per (part_id, site_id)
# The data is already at WEEKLY granularity (7-day steps).
# Sort then apply rolling window of 4 observations (= 4 weeks).
# ---------------------------------------------------------------------------
print("Computing rolling 4-week burn_rate_daily ...")

sch = sch.sort_values(['part_id', 'site_id', 'date']).reset_index(drop=True)

# rolling mean of consumption_qty over 4-week window, then divide by 7 → daily rate
sch['burn_rate_daily'] = (
    sch.groupby(['part_id', 'site_id'], group_keys=False)['consumption_qty']
    .transform(lambda s: s.rolling(window=4, min_periods=1).mean() / 7)
)

# ---------------------------------------------------------------------------
# TTS_days = on_hand_qty / burn_rate_daily  (NaN when burn_rate == 0)
# ---------------------------------------------------------------------------
sch['TTS_days'] = np.where(
    sch['burn_rate_daily'] > 0,
    sch['on_hand_qty'] / sch['burn_rate_daily'],
    float('nan')
)

# ---------------------------------------------------------------------------
# Aggregate to weekly level
# week column is already present (ISO period string)
# ---------------------------------------------------------------------------
print("Aggregating to weekly level ...")

weekly = (
    sch.groupby(['part_id', 'site_id', 'week'], as_index=False)
    .agg(
        mean_TTS_days=('TTS_days', 'mean'),
        mean_burn_rate_daily=('burn_rate_daily', 'mean'),
        on_hand_qty_mean=('on_hand_qty', 'mean'),
        rows=('TTS_days', 'count'),
    )
)

print(f"  Weekly rows: {len(weekly):,}")
print(f"  TTS_days null pct: {weekly['mean_TTS_days'].isna().mean():.2%}")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
OUT_FILE = OUT_DIR / 'tts_weekly.parquet'
weekly.to_parquet(OUT_FILE, index=False)
print(f"\nSaved: {OUT_FILE}")
print("=== DONE ===")
