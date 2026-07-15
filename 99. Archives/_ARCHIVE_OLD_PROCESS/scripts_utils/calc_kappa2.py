import pandas as pd
import numpy as np

EXCEL = r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH\P0-03_Pilot_Labeling\P0-03_pilot_labeling_150.xlsx"

df = pd.read_excel(EXCEL, sheet_name="\U0001f4cb Gán Nhãn", header=1, usecols="G:J", nrows=155)
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

def fleiss_kappa_manual(ratings, n_categories=3):
    """
    ratings: array of shape (n_subjects, n_raters)
    returns Fleiss' kappa
    """
    n_subjects, n_raters = ratings.shape
    # Build frequency matrix: n_subjects x n_categories
    freq = np.zeros((n_subjects, n_categories), dtype=int)
    for cat in range(n_categories):
        freq[:, cat] = np.sum(ratings == cat, axis=1)

    # P_j: proportion of all assignments to category j
    P_j = freq.sum(axis=0) / (n_subjects * n_raters)

    # P_i: extent of agreement for subject i
    P_i = (np.sum(freq * (freq - 1), axis=1)) / (n_raters * (n_raters - 1))

    P_bar = P_i.mean()
    P_e_bar = np.sum(P_j ** 2)

    if P_e_bar == 1.0:
        return float('nan')
    kappa = (P_bar - P_e_bar) / (1 - P_e_bar)
    return kappa

def cohens_kappa_manual(r1, r2, n_categories=3):
    """
    r1, r2: 1D arrays of ratings
    returns Cohen's kappa
    """
    n = len(r1)
    # Observed agreement
    p_o = np.sum(r1 == r2) / n
    # Expected agreement
    p_e = sum((np.sum(r1 == c) / n) * (np.sum(r2 == c) / n) for c in range(n_categories))
    if p_e == 1.0:
        return float('nan')
    kappa = (p_o - p_e) / (1 - p_e)
    return kappa

# Kappa tong the
k_all = fleiss_kappa_manual(labels)
print(f"\nFleiss Kappa (150 bai): {k_all:.4f}")

# Kappa Block 1 (100 bai dau)
k1 = fleiss_kappa_manual(labels[:100])
print(f"Fleiss Kappa Block 1 (100 bai random): {k1:.4f}")

# Kappa Block 2 (50 bai sau)
k2 = fleiss_kappa_manual(labels[100:])
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
raters = ["Claude","Gemini","DeepSeek","ChatGPT"]
print(f"\nPairwise Cohen Kappa:")
for i in range(4):
    for j in range(i+1, 4):
        ck = cohens_kappa_manual(df[raters[i]].values, df[raters[j]].values)
        print(f"  {raters[i]} vs {raters[j]}: {ck:.4f}")
