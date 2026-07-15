# P5-09 — Model Comparison

## Purpose
Loads results from P5-07 (baseline) and P5-08 (XGBoost), prints a side-by-side
comparison table, and saves it as a Markdown file.

## Mock / Real data
| Item | Status |
|------|--------|
| Baseline results | Loads `P5-07/baseline_results.json`; falls back to **mock** |
| XGBoost results  | Loads `P5-08/xgb_results.json`; falls back to **mock** |

## What to replace when going live
- Run P5-07 and P5-08 first to generate real result JSON files.
- No code changes required after that.

## Outputs
- `P5-09/model_comparison.md` — Markdown comparison table with per-fold and average metrics
