# P5-06 — Walk-Forward Cross-Validation

## Purpose
Provides `WalkForwardCV`, a reusable splitter that produces expanding-window
train/test index pairs for weekly time-series data.

## Mock / Real data
| Item | Status |
|------|--------|
| Splitter logic | **Real** — no mock data used |
| Self-test DataFrame | **Mock** — 80-week synthetic data in `__main__` block |

## What to replace when going live
- Nothing in the splitter itself needs changing.
- The self-test dummy DataFrame can be swapped for the real feature matrix
  from `P5-01\feature_matrix.parquet`.

## Usage
```python
from P5-06.walk_forward_cv import WalkForwardCV
cv = WalkForwardCV(n_folds=5, fold_size_weeks=13)
folds = cv.split(df, date_col='week')   # returns list of (train_idx, test_idx)
```
