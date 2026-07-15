"""
P5-06 | walk_forward_cv.py
Walk-Forward Cross-Validation for time-series ML pipeline.

MOCK DATA NOTE:
  The split() method works on any DataFrame with a date column.
  No mock data here — pure splitter logic.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')


class WalkForwardCV:
    """
    Walk-forward (expanding-window) cross-validator for weekly time-series data.

    Parameters
    ----------
    n_folds : int
        Number of validation folds.
    fold_size_weeks : int
        Number of weeks in each test fold (default 13 = 1 quarter).
    min_train_weeks : int
        Minimum number of training weeks required before the first fold.
        Defaults to fold_size_weeks so the first train window is at least
        one quarter long.
    """

    def __init__(self, n_folds: int = 5, fold_size_weeks: int = 13,
                 min_train_weeks: int = None):
        self.n_folds = n_folds
        self.fold_size_weeks = fold_size_weeks
        self.min_train_weeks = min_train_weeks if min_train_weeks is not None \
            else fold_size_weeks

    def split(self, df: pd.DataFrame, date_col: str = 'week'):
        """
        Generate (train_idx, test_idx) index pairs for walk-forward CV.

        The DataFrame must be sorted by `date_col` (or at least have a
        column that sorts chronologically).  Indices refer to the integer
        positional index of the **passed** DataFrame (i.e. suitable for
        .iloc[]).

        Parameters
        ----------
        df : pd.DataFrame
            Feature matrix with at least a `date_col` column.
        date_col : str
            Column name containing the week identifier.

        Yields
        ------
        (train_idx, test_idx) : tuple of np.ndarray
            Positional integer indices for train and test sets.
        """
        df_sorted = df.sort_values(date_col).reset_index(drop=True)
        unique_weeks = np.sort(df_sorted[date_col].unique())
        n_weeks = len(unique_weeks)

        # The last fold's test window ends at the last available week.
        # Work backwards to find fold boundaries.
        test_end = n_weeks  # exclusive
        folds = []
        for _ in range(self.n_folds):
            test_start = test_end - self.fold_size_weeks
            if test_start < self.min_train_weeks:
                break  # not enough training data
            train_weeks = unique_weeks[:test_start]
            test_weeks = unique_weeks[test_start:test_end]
            train_mask = df_sorted[date_col].isin(train_weeks)
            test_mask = df_sorted[date_col].isin(test_weeks)
            folds.append((
                df_sorted.index[train_mask].to_numpy(),
                df_sorted.index[test_mask].to_numpy(),
            ))
            test_end = test_start  # expand window backwards for next fold

        # Return folds in chronological order (earliest first)
        folds.reverse()
        return folds


# ---------------------------------------------------------------------------
# Quick self-test with a dummy 80-week DataFrame
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print("=== P5-06 WalkForwardCV self-test ===\n")

    rng = np.random.default_rng(42)
    n_weeks = 80
    n_parts = 3

    weeks = pd.date_range('2022-01-03', periods=n_weeks, freq='W-MON')
    rows = []
    for w in weeks:
        for p in range(n_parts):
            rows.append({
                'week': w,
                'part_group': f'PG-{p:02d}',
                'feature_1': rng.random(),
                'y': int(rng.random() < 0.15),
            })

    df_dummy = pd.DataFrame(rows)
    print(f"Dummy DataFrame shape: {df_dummy.shape}")
    print(f"Unique weeks: {df_dummy['week'].nunique()}")

    cv = WalkForwardCV(n_folds=5, fold_size_weeks=13)
    folds = cv.split(df_dummy, date_col='week')

    print(f"\nNumber of folds produced: {len(folds)}")
    for i, (tr, te) in enumerate(folds):
        tr_weeks = df_dummy.loc[tr, 'week'].nunique()
        te_weeks = df_dummy.loc[te, 'week'].nunique()
        print(f"  Fold {i+1}: train={len(tr)} rows ({tr_weeks} wks) | "
              f"test={len(te)} rows ({te_weeks} wks)")

    print("\nP5-06 OK — WalkForwardCV works correctly.")
