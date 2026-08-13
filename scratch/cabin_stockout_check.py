"""
Diagnostic: Check Cabin stockout distribution across Val/Test splits
and all 8 part families for completeness.
"""
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load data
df_fm = pd.read_parquet(ROOT / "P2-03_Feature_Matrix" / "feature_matrix.parquet")
df_y2 = pd.read_parquet(ROOT / "P2-04_Derive_y2" / "y2_shifted.parquet")
df_parts = pd.read_csv(ROOT / "0. internal data" / "parts_master.csv")

# Merge to get y2_shift1 target + part_family
df = pd.merge(df_fm, df_y2[['part_id', 'week', 'y2_shift1']], on=['part_id', 'week'], how='inner')
df = pd.merge(df, df_parts[['part_id', 'part_family']], on='part_id', how='inner')

# Sort by week (same as pipeline)
df = df.sort_values('week').reset_index(drop=True)

# Chronological split 60/40 (same as run_phase3_pipeline.py)
split_idx = int(len(df) * 0.6)
df_val = df.iloc[:split_idx].copy()
df_test = df.iloc[split_idx:].copy()

print("=" * 70)
print("FULL STOCKOUT DISTRIBUTION BY PART FAMILY (ALL 8 FAMILIES)")
print("=" * 70)

all_families = sorted(df_parts['part_family'].unique())
print(f"\nAll families in parts_master: {all_families}")
print(f"Total families: {len(all_families)}")

print(f"\n{'Family':<15} {'Total':>8} {'y=1':>8} {'%pos':>8}   |  {'Val_total':>10} {'Val_y=1':>8} {'Test_total':>10} {'Test_y=1':>8}")
print("-" * 100)

for fam in all_families:
    mask_all = df['part_family'] == fam
    mask_val = df_val['part_family'] == fam
    mask_test = df_test['part_family'] == fam
    
    total = mask_all.sum()
    pos = df.loc[mask_all, 'y2_shift1'].sum()
    pct = (pos / total * 100) if total > 0 else 0
    
    val_total = mask_val.sum()
    val_pos = df_val.loc[mask_val, 'y2_shift1'].sum()
    test_total = mask_test.sum()
    test_pos = df_test.loc[mask_test, 'y2_shift1'].sum()
    
    marker = " <<<" if fam == "Cabin" else ""
    print(f"{fam:<15} {total:>8} {int(pos):>8} {pct:>7.2f}%   |  {val_total:>10} {int(val_pos):>8} {test_total:>10} {int(test_pos):>8}{marker}")

print("\n" + "=" * 70)
print("CABIN DEEP DIVE")
print("=" * 70)

cabin_all = df[df['part_family'] == 'Cabin']
cabin_val = df_val[df_val['part_family'] == 'Cabin']
cabin_test = df_test[df_test['part_family'] == 'Cabin']

print(f"\nCabin total samples: {len(cabin_all)}")
print(f"Cabin total stockouts (y2_shift1=1): {int(cabin_all['y2_shift1'].sum())}")
print(f"  - In Validation set: {int(cabin_val['y2_shift1'].sum())} / {len(cabin_val)} rows")
print(f"  - In Test set:       {int(cabin_test['y2_shift1'].sum())} / {len(cabin_test)} rows")

if cabin_test['y2_shift1'].sum() == 0:
    print("\n>>> CONCLUSION: Cabin has ZERO stockouts in test set.")
    print(">>> LTG = undefined for Cabin.")
    print(">>> Table 7 correctly excludes Cabin, but needs a footnote explaining why.")
elif cabin_test['y2_shift1'].sum() <= 3:
    print(f"\n>>> CONCLUSION: Cabin has only {int(cabin_test['y2_shift1'].sum())} stockout(s) in test set.")
    print(">>> Results are statistically unreliable (sample too small).")
    print(">>> Should add footnote about insufficient statistical power.")
else:
    print(f"\n>>> CONCLUSION: Cabin has {int(cabin_test['y2_shift1'].sum())} stockouts in test set.")
    print(">>> Should be included in Table 7.")

# Also check which weeks the Cabin stockouts happen
if cabin_all['y2_shift1'].sum() > 0:
    stockout_weeks = cabin_all[cabin_all['y2_shift1'] == 1][['week', 'part_id', 'y2_shift1']]
    print(f"\nCabin stockout events (all):")
    print(stockout_weeks.to_string(index=False))
    
    # Check if those weeks fall in val or test
    val_max_week = df_val['week'].max()
    test_min_week = df_test['week'].min()
    print(f"\nVal period ends at:   {val_max_week}")
    print(f"Test period starts at: {test_min_week}")
