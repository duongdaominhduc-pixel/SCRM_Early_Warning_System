# P5-07 — Logistic Regression Baseline

## Purpose
Trains a Logistic Regression model using **operational features only** (1-7)
via 5-fold walk-forward cross-validation. Serves as the performance baseline
against which XGBoost (P5-08) is compared.

## Mock / Real data
| Item | Status |
|------|--------|
| Feature matrix | **Auto-detects** `P5-01/feature_matrix.parquet`; falls back to 200-row mock |
| Features 8-10 (NLP) | **Present in schema but NOT used** in this model |

## What to replace when going live
- Ensure `P5-01/feature_matrix.parquet` exists with the real feature matrix.
- No other changes needed — the script will use real data automatically.

## Outputs
- `P5-07/baseline_results.json` — per-fold and average Recall, Precision, F1, AUC
