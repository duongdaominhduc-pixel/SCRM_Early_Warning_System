"""
P5-02 — Derive y_true (Inbound Ground Truth)

y_true = 1 if in week W for part_group G:
  (A) on_hand_qty ≤ 0 in any day of that week  (stockout)
  OR
  (B) receipt_date > promised_date for any PO due that week  (late delivery)
y_true = 0 otherwise

Aggregation: if ANY part within part_group has y_true=1 in that week → group y_true=1
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')
OUT  = BASE / 'P5-02'
OUT.mkdir(exist_ok=True)


def derive_y_true():
    print("=== P5-02: Derive y_true ===\n")

    # ── Load supply chain history ─────────────────────────────────────────────
    sch_path = BASE / 'P4-01' / 'supply_chain_history.parquet'
    if sch_path.exists():
        sch = pd.read_parquet(sch_path)
    else:
        print("WARNING: supply_chain_history.parquet not found — using mock data")
        np.random.seed(42)
        days  = pd.date_range('2015-01-01', '2017-12-31', freq='D')
        parts = ['P001','P002','P003','P004','P005']
        records = []
        for p in parts:
            for d in days:
                records.append({
                    'date':       d,
                    'part_id':    p,
                    'on_hand_qty': max(0, int(np.random.normal(50, 20))),
                })
        sch = pd.DataFrame(records)

    # ── Load parts master for part_family mapping ─────────────────────────────
    pm_path = BASE / 'P4-01' / 'parts_master.parquet'
    if pm_path.exists():
        pm = pd.read_parquet(pm_path)[['part_id','part_family']]
    else:
        print("WARNING: parts_master.parquet not found — using mock mapping")
        pm = pd.DataFrame({
            'part_id':    ['P001','P002','P003','P004','P005'],
            'part_family': ['AVIONICS','AEROSTRUCTURES','HYDRAULICS','LANDING_GEAR','PROPULSION'],
        })

    # ── Load purchase orders for late delivery ────────────────────────────────
    po_path = BASE / 'P4-01' / 'purchase_orders.parquet'
    if po_path.exists():
        po = pd.read_parquet(po_path)
    else:
        print("WARNING: purchase_orders.parquet not found — using mock PO data")
        np.random.seed(43)
        n = 500
        dates = pd.date_range('2015-01-01', '2017-12-31', freq='D')
        po = pd.DataFrame({
            'part_id':       np.random.choice(['P001','P002','P003','P004','P005'], n),
            'promised_date': np.random.choice(dates, n),
            'receipt_date':  None,
        })
        po['receipt_date'] = po['promised_date'] + pd.to_timedelta(
            np.random.randint(-3, 15, n), unit='D'
        )

    # ── Stockout signal ───────────────────────────────────────────────────────
    sch['date'] = pd.to_datetime(sch['date'])
    sch['week'] = sch['date'].dt.to_period('W')
    sch = sch.merge(pm, on='part_id', how='left')
    sch['stockout'] = (sch['on_hand_qty'] <= 0).astype(int)

    stockout_weekly = sch.groupby(['part_family','week'])['stockout'].max().reset_index()
    stockout_weekly.columns = ['part_group','week','stockout_flag']

    # ── Late delivery signal (Phương án A) ───────────────────────────────────
    # y_true = 1 chỉ khi avg_delay >= 3 ngày VÀ pct_late >= 50% trong tuần đó
    # Lý do: 55.85% PO đều late → threshold "any late" cho positive rate 98% → vô nghĩa
    DELAY_THRESHOLD   = 3    # ngày
    PCT_LATE_THRESHOLD = 0.5  # 50%

    po['promised_date'] = pd.to_datetime(po['promised_date'])
    po['receipt_date']  = pd.to_datetime(po['receipt_date'])
    po['week'] = po['promised_date'].dt.to_period('W')
    po['delay_days'] = (po['receipt_date'] - po['promised_date']).dt.days
    po['is_late'] = (po['delay_days'] > 0).astype(int)
    po = po.merge(pm, on='part_id', how='left')

    late_agg = po.groupby(['part_family','week']).agg(
        avg_delay=('delay_days','mean'),
        pct_late=('is_late','mean'),
    ).reset_index()
    late_agg['late_flag'] = (
        (late_agg['avg_delay'] >= DELAY_THRESHOLD) &
        (late_agg['pct_late'] >= PCT_LATE_THRESHOLD)
    ).astype(int)
    late_agg = late_agg.rename(columns={'part_family':'part_group'})

    # ── Merge and derive y_true ───────────────────────────────────────────────
    y = stockout_weekly.merge(late_agg[['part_group','week','late_flag','avg_delay','pct_late']],
                              on=['part_group','week'], how='outer')
    y['stockout_flag'] = y['stockout_flag'].fillna(0).astype(int)
    y['late_flag']     = y['late_flag'].fillna(0).astype(int)
    y['y_true']        = ((y['stockout_flag'] == 1) | (y['late_flag'] == 1)).astype(int)
    y['week']          = y['week'].astype(str)

    print(f"y_true shape: {y.shape}")
    print(f"Positive rate: {y['y_true'].mean():.1%} ({y['y_true'].sum()} / {len(y)} weeks)")
    print(f"Stockout-only: {((y['stockout_flag']==1)&(y['late_flag']==0)).sum()}")
    print(f"Late-only:     {((y['stockout_flag']==0)&(y['late_flag']==1)).sum()}")
    print(f"Both:          {((y['stockout_flag']==1)&(y['late_flag']==1)).sum()}")

    y.to_parquet(OUT / 'y_true.parquet', index=False)
    y.to_csv(OUT / 'y_true.csv', index=False, encoding='utf-8-sig')
    print(f"\nSaved → P5-02/y_true.parquet ({len(y)} rows)")
    return y


if __name__ == '__main__':
    derive_y_true()
