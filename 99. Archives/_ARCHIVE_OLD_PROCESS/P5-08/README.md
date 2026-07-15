# P5-08 — XGBoost Main Model

## Purpose
Trains an XGBoost classifier on **all 10 features** (operational + NLP) using
5-fold walk-forward cross-validation.  Class imbalance is handled via
`scale_pos_weight = n_neg / n_pos` (computed per fold).

## Mock / Real data
| Item | Status |
|------|--------|
| Features 1-7 (operational) | **Real** (or mock if P5-01 parquet absent) |
| Features 8-10 (NLP) | **MOCK** random values — replace with `P3-12` output |
| xgboost package | Auto-installs via pip if missing |

## What to replace when going live
1. Ensure `P5-01/feature_matrix.parquet` contains real operational features.
2. Replace `news_risk_score`, `disruption_event_flag`, `severity_score`
   columns with real values from **P3-12**.
3. Set `nlp_features_mock: false` in results JSON after replacement.

## Outputs
- `P5-08/xgb_model.json` — best fold XGBoost model (JSON format)
- `P5-08/xgb_results.json` — per-fold and average Recall, Precision, F1, AUC
