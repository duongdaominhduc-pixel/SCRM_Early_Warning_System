# P5-10 — SHAP Feature Importance

## Purpose
Loads the trained XGBoost model and computes SHAP values on the test set to
explain which features drive risk predictions.

## Mock / Real data
| Item | Status |
|------|--------|
| XGBoost model | Loads `P5-08/xgb_model.json`; trains dummy model if absent |
| Features 1-7 | Real (or mock if P5-01 parquet absent) |
| Features 8-10 (NLP) | **MOCK** — flagged with `[MOCK NLP]` in output |

## What to replace when going live
1. Run P5-08 first to generate `xgb_model.json`.
2. Replace NLP feature columns with real **P3-12** outputs.

## Outputs
- `P5-10/shap_values.csv` — raw SHAP values per observation (columns = features)
- `P5-10/shap_importance_summary.csv` — mean |SHAP| per feature, sorted descending
