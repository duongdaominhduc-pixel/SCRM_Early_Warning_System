# P5-11 — Optimal Classification Threshold (Youden's J)

## Purpose
Finds the decision threshold that maximises Youden's J-statistic
(`Sensitivity + Specificity - 1`) from the XGBoost ROC curve.
This threshold is used downstream by P5-12 to generate binary alerts.

## Mock / Real data
| Item | Status |
|------|--------|
| Predictions | Loads `P5-08/xgb_predictions.csv`; falls back to **mock** beta-distributed scores |

## What to replace when going live
- Modify P5-08 to save `xgb_predictions.csv` (columns: `y_true`, `risk_score`,
  `part_group`, `week`) on each test fold or the final held-out set.
- No logic changes needed in this script.

## Outputs
- `P5-11/optimal_threshold.json`
  ```json
  {
    "threshold":   0.XXXX,
    "sensitivity": 0.XXXX,
    "specificity": 0.XXXX,
    "youdens_j":   0.XXXX
  }
  ```
