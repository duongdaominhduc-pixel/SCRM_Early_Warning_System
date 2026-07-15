# P5-13 — Lead Time of Warning (LTW)

## Purpose
Measures how many weeks in advance the model correctly raised an alert
before an actual supply disruption occurred.  This is the key operational
usefulness metric: an alert that fires 3 weeks early is far more actionable
than one that fires the same week.

## Metric definition
For each **true positive** (alert raised AND disruption confirmed for that
part group), compute:

```
lead_time_weeks = (disruption_week − alert_week) / 7 days
```

Only positive lead times are counted.

## Mock / Real data
| Item | Status |
|------|--------|
| Alert data | Loads `P5-12/weekly_alerts.csv`; falls back to **mock** |
| `disruption_week` column | Inferred from `y_true` if absent in CSV |

## What to replace when going live
1. Run P5-12 → saves `weekly_alerts.csv`.
2. Ensure the CSV contains a `disruption_week` column (the confirmed date of
   the supply event), or that `y_true` is accurate enough to serve as proxy.

## Outputs
- `P5-13/lead_time_results.json`
  ```json
  {
    "n_true_positives": N,
    "mean_lead_time_weeks": X.XX,
    "median_lead_time_weeks": X.XX,
    "min_lead_time_weeks": X.XX,
    "max_lead_time_weeks": X.XX
  }
  ```
