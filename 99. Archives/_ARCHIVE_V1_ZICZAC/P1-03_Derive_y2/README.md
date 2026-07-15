# P1-03 | Derive y2 — Target Shift (Fix Look-ahead Bias)

This module derives the target variable for the Supply Chain Risk Management (SCRM) predictive system, effectively converting a standard classification problem into a true Early Warning System (EWS).

## Academic Framework
1. **Operational Continuity Proxy**: Uses the binary `w1_stockout_flag` as the primary proxy for supply chain disruption (Actionable Intelligence).
2. **Lead-Time Advantage**: Calculates predictions for two future time horizons:
   - `y2_shift1`: Probability of stockout at Week W+1 (Short-term Horizon)
   - `y2_shift2`: Probability of stockout at Week W+2 (Medium-term Horizon)
3. **Data Alignment for Supervised Time-Series**: Properly handles right-censored data by dropping NaN rows (`dropna`) caused by the time shift, ensuring strict separation of historical features and future outcomes (eliminating Look-Ahead Bias).

## Pipeline Scripts
- `01_target_shift.py`: Merges the generated feature matrix from P1-02, derives the W+1 and W+2 targets via `.shift(-n)`, handles end-of-series missing values, and assesses the Positive Class Imbalance.

## Usage
Run the target shift script via Python:
```bash
py scripts/01_target_shift.py
```

*Note: The script outputs `feature_matrix_with_targets.parquet` and warns if class imbalance (e.g., < 5% positive rate) requires techniques like SMOTE in the subsequent modeling phase.*
