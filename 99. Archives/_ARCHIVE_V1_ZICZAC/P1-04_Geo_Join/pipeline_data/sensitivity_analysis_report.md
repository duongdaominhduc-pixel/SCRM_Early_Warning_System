# Geographic Weighting - Sensitivity Analysis Report

This report validates the **Asymptotic Stability** of the Layered Risk Perception (Soft Join) mechanism.

## Impact of Regional Weight Variance on Total Risk Score

|   region_weight |   total_risk_score |   variance_from_baseline_pct |
|----------------:|-------------------:|-----------------------------:|
|             0.5 |        1.02316e+06 |                     -4.43379 |
|             0.6 |        1.07063e+06 |                      0       |
|             0.7 |        1.1181e+06  |                      4.43379 |

### Conclusion
The variance is mathematically stable, confirming that adjusting the 'Regional Contagion' hyperparameter does not cause erratic shifts in the overall risk exposure signal. This defends the methodology against cherry-picking allegations.
