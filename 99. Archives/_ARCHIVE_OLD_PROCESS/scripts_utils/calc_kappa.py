import pandas as pd
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters

EXCEL = r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH\P0-03_Pilot_Labeling\P0-03_pilot_labeling_150.xlsx"

df = pd.read_excel(EXCEL, sheet_name="📋 Gán Nhãn", header=1, usecols="G:J", nrows=155)
df.columns = ["Claude", "Gemini", "DeepSeek", "ChatGPT"]

# Ép kiểu số, bỏ NaN và separator rows
df = df.apply(pd.to_numeric, errors="coerce").dropna()
df = df.astype(int)
df = df[df.isin([0,1,2]).all(axis=1)]

print(f"So bai hop le: {len(df)}")
print(f"\nPhan phoi nhan tung rater:")
for col in df.columns:
    v = df[col]
    print(f"  {col}: 0={sum(v==0)}  1={sum(v==1)}  2={sum(v==2)}")

labels = df.values

# Kappa tong the
agg, _ = aggregate_raters(labels)
k_all = fleiss_kappa(agg, method="fleiss")
print(f"\nFleiss Kappa (150 bai): {k_all:.4f}")

# Kappa Block 1 (100 bai dau)
agg1, _ = aggregate_raters(labels[:100])
k1 = fleiss_kappa(agg1, method="fleiss")
print(f"Fleiss Kappa Block 1 (100 bai random): {k1:.4f}")

# Kappa Block 2 (50 bai sau)
agg2, _ = aggregate_raters(labels[100:])
k2 = fleiss_kappa(agg2, method="fleiss")
print(f"Fleiss Kappa Block 2 (50 bai HR boost): {k2:.4f}")

# Bat dong: bai co >= 3 nhan khac nhau
disagree = []
for i, row in enumerate(labels):
    if len(set(row)) >= 3:
        disagree.append({"idx": i+1, "labels": row.tolist()})

print(f"\nSo bai bat dong (>=3 nhan khac): {len(disagree)}")
for d in disagree[:20]:
    print(f"  Bai {d['idx']:03d}: {d['labels']}")

# Pairwise Cohen Kappa (giua tung cap rater)
from statsmodels.stats.inter_rater import cohens_kappa
raters = ["Claude","Gemini","DeepSeek","ChatGPT"]
print(f"\nPairwise Cohen Kappa:")
for i in range(4):
    for j in range(i+1, 4):
        ck = cohens_kappa(df[raters[i]].values, df[raters[j]].values)
        print(f"  {raters[i]} vs {raters[j]}: {ck.kappa:.4f}")
