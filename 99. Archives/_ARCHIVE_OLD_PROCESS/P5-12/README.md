# P5-12 — Weekly Alert Generation

## Purpose
Applies the Youden's J optimal threshold (from P5-11) to XGBoost risk scores
(from P5-08) and outputs a CSV of binary supply-risk alerts per
`(part_group, week)`.

## Mock / Real data
| Item | Status |
|------|--------|
| Predictions | Loads `P5-08/xgb_predictions.csv`; falls back to **mock** |
| Threshold | Loads `P5-11/optimal_threshold.json`; falls back to **0.40** |

## What to replace when going live
1. Run P5-08 → saves `xgb_predictions.csv`.
2. Run P5-11 → saves `optimal_threshold.json`.
3. Rerun this script — no code changes needed.

## Outputs
- `P5-12/weekly_alerts.csv`

| Column | Description |
|--------|-------------|
| `part_group` | Part group identifier |
| `week` | ISO week start date |
| `risk_score` | XGBoost predicted probability |
| `y_true` | Actual label (if available) |
| `alert_level` | 1 = alert raised, 0 = no alert |
| `threshold_used` | Threshold applied (from Youden's J) |
