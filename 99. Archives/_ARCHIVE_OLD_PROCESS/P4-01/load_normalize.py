import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = Path(r'/Users/lelinh/Documents/BBKH')
DATA_DIR = BASE / '0. internal data'
OUT_DIR = BASE / 'P4-01'
OUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Ensure dependencies
# ---------------------------------------------------------------------------
try:
    import pandas as pd
    import pyarrow  # noqa: F401
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'pyarrow'])
    import pandas as pd

# ---------------------------------------------------------------------------
# 1. Load CSVs with correct dtypes
# ---------------------------------------------------------------------------
print("Loading CSVs...")

parts_master = pd.read_csv(
    DATA_DIR / 'parts_master.csv',
    dtype={
        'part_id': str,
        'part_family': str,
        'criticality_class': str,
        'unit_cost': float,
        'lead_time_days': float,
        'supplier_id_primary': str,
        'supplier_risk_class': str,
        'is_repairable': str,
        'shelf_life_days': 'Int64',
    }
)

purchase_orders = pd.read_csv(
    DATA_DIR / 'shifted_purchase_orders.csv',
    dtype={
        'po_id': str,
        'supplier_id': str,
        'site_id': str,
        'part_id': str,
        'ordered_qty': float,
        'received_qty': float,
    },
    parse_dates=['order_date', 'promised_date', 'receipt_date'],
)

quality_incidents = pd.read_csv(
    DATA_DIR / 'shifted_quality_incidents.csv',
    dtype={
        'incident_id': str,
        'part_id': str,
        'supplier_id': str,
        'site_id': str,
        'defect_severity': str,
        'defect_type': str,
        'scrap_qty': float,
    },
    parse_dates=['incident_date'],
)

supply_chain_history = pd.read_csv(
    DATA_DIR / 'shifted_supply_chain_history.csv',
    dtype={
        'site_id': str,
        'part_id': str,
        'planned_maintenance': str,
        'consumption_qty': float,
        'on_hand_qty': float,
        'backorder_qty': float,
        'blocked_qty': float,
        'forecast_qty': float,
        'forecast_type': str,
        'forecast_uplift_pct': float,
    },
    parse_dates=['date'],
)

supplier_locations = pd.read_csv(
    DATA_DIR / 'supplier_locations.csv',
    dtype={
        'supplier_id': str,
        'country': str,
        'region': str,
    }
)

# ---------------------------------------------------------------------------
# 2. Add week column (ISO week period)
# ---------------------------------------------------------------------------
supply_chain_history['week'] = supply_chain_history['date'].dt.to_period('W')
purchase_orders['week'] = purchase_orders['order_date'].dt.to_period('W')

# ---------------------------------------------------------------------------
# 3. Validation
# ---------------------------------------------------------------------------
EXPECTED_ROWS = {
    'parts_master': 300,
    'purchase_orders': 29666,
    'quality_incidents': 368,
    'supply_chain_history': 280800,
    'supplier_locations': 40,
}

DATE_RANGES = {
    'purchase_orders': ('order_date', '2015-01-01', '2018-04-12'),
    'quality_incidents': ('incident_date', '2015-01-01', '2018-12-31'),
    'supply_chain_history': ('date', '2015-01-01', '2017-12-21'),
}

frames = {
    'parts_master': parts_master,
    'purchase_orders': purchase_orders,
    'quality_incidents': quality_incidents,
    'supply_chain_history': supply_chain_history,
    'supplier_locations': supplier_locations,
}

print("\n=== Validation Summary ===")
all_ok = True
for name, df in frames.items():
    expected = EXPECTED_ROWS[name]
    actual = len(df)
    status = 'OK' if actual == expected else f'MISMATCH (expected {expected})'
    if actual != expected:
        all_ok = False
    print(f"  {name}: {actual} rows  [{status}]")

print("\n  Date ranges:")
for name, (col, exp_min, exp_max) in DATE_RANGES.items():
    df = frames[name]
    actual_min = df[col].min().date()
    actual_max = df[col].max().date()
    print(f"  {name}.{col}: {actual_min} -> {actual_max}  (expected {exp_min} -> {exp_max})")

print("\n  Null counts (selected columns):")
print(f"  parts_master.shelf_life_days nulls: {parts_master['shelf_life_days'].isna().sum()}")
print(f"  purchase_orders.receipt_date nulls: {purchase_orders['receipt_date'].isna().sum()}")

# ---------------------------------------------------------------------------
# 4. Save parquet — period columns must be converted to str for Arrow compat
# ---------------------------------------------------------------------------
print("\nSaving parquet files...")

def save_parquet(df: pd.DataFrame, path: Path):
    df_out = df.copy()
    for col in df_out.columns:
        if hasattr(df_out[col], 'dt') and hasattr(df_out[col].dt, 'freq'):
            # Period column
            df_out[col] = df_out[col].astype(str)
    df_out.to_parquet(path, index=False)

save_parquet(parts_master,         OUT_DIR / 'parts_master.parquet')
save_parquet(purchase_orders,      OUT_DIR / 'purchase_orders.parquet')
save_parquet(quality_incidents,    OUT_DIR / 'quality_incidents.parquet')
save_parquet(supply_chain_history, OUT_DIR / 'supply_chain_history.parquet')
save_parquet(supplier_locations,   OUT_DIR / 'supplier_locations.parquet')

print("\nAll parquet files saved to P4-01\\")
print("=== DONE ===")
