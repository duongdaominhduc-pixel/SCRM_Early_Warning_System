import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
IN_FILE = BASE / 'P4-01' / 'purchase_orders.parquet'
OUT_DIR = BASE / 'P4-03'
OUT_DIR.mkdir(exist_ok=True)

try:
    import pandas as pd
    import pyarrow  # noqa: F401
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'pyarrow'])
    import pandas as pd

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
print("Loading purchase_orders.parquet ...")
po = pd.read_parquet(IN_FILE)

# Restore date dtypes if needed
for col in ['order_date', 'promised_date', 'receipt_date']:
    if po[col].dtype == object:
        po[col] = pd.to_datetime(po[col])

print(f"  Rows loaded: {len(po):,}")

# ---------------------------------------------------------------------------
# Compute delivery_delay_days
# ---------------------------------------------------------------------------
po['receipt_date'] = pd.to_datetime(po['receipt_date'])
po['promised_date'] = pd.to_datetime(po['promised_date'])
po['delivery_delay_days'] = (po['receipt_date'] - po['promised_date']).dt.days
po['is_late'] = (po['delivery_delay_days'] > 0).astype(int)

print(f"  Late orders: {po['is_late'].sum():,} / {len(po):,} ({po['is_late'].mean():.2%})")
print(f"  Avg delay (all): {po['delivery_delay_days'].mean():.2f} days")

# ---------------------------------------------------------------------------
# Add week_of_promised_date
# ---------------------------------------------------------------------------
po['week_of_promised_date'] = po['promised_date'].dt.to_period('W').astype(str)

# ---------------------------------------------------------------------------
# Aggregate to weekly per (supplier_id, part_id, week_of_promised_date)
# ---------------------------------------------------------------------------
print("Aggregating to weekly level ...")

weekly = (
    po.groupby(['supplier_id', 'part_id', 'week_of_promised_date'], as_index=False)
    .agg(
        avg_delay=('delivery_delay_days', 'mean'),
        pct_late=('is_late', 'mean'),
        order_count=('po_id', 'count'),
        total_ordered_qty=('ordered_qty', 'sum'),
        total_received_qty=('received_qty', 'sum'),
    )
)

print(f"  Weekly rows: {len(weekly):,}")
print(f"  Avg weekly avg_delay: {weekly['avg_delay'].mean():.2f} days")
print(f"  Avg weekly pct_late: {weekly['pct_late'].mean():.2%}")

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
OUT_FILE = OUT_DIR / 'delivery_delays_weekly.parquet'
weekly.to_parquet(OUT_FILE, index=False)
print(f"\nSaved: {OUT_FILE}")
print("=== DONE ===")
