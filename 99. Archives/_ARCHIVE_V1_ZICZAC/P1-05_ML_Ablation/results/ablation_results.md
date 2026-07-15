# ML Training - Ablation Study Results

Evaluation of NLP features ('Layered Risk Perception') vs Baseline using TimeSeriesSplit (gap=2) to prevent data leakage.

## Performance Metrics

| Target    | Configuration      |   Minority F1-Score |   Precision |   Recall |   PR-AUC |
|:----------|:-------------------|--------------------:|------------:|---------:|---------:|
| y2_shift1 | Tier1_RuleBased    |            0.1178   |   0.0638141 | 0.841971 | 0.455295 |
| y2_shift1 | Tier2_LR_Baseline  |            0.163853 |   0.0919819 | 0.832969 | 0.195977 |
| y2_shift1 | Tier2_XGB_Baseline |            0.206893 |   0.137108  | 0.496269 | 0.157168 |
| y2_shift1 | Tier3_LR_SCRM      |            0.164095 |   0.0922253 | 0.826644 | 0.192622 |
| y2_shift1 | Tier3_XGB_SCRM     |            0.225694 |   0.159282  | 0.421706 | 0.154104 |
| y2_shift2 | Tier1_RuleBased    |            0.107634 |   0.0583215 | 0.773413 | 0.419335 |
| y2_shift2 | Tier2_LR_Baseline  |            0.164072 |   0.0922754 | 0.834418 | 0.188011 |
| y2_shift2 | Tier2_XGB_Baseline |            0.191906 |   0.128747  | 0.451474 | 0.146946 |
| y2_shift2 | Tier3_LR_SCRM      |            0.162168 |   0.0911373 | 0.829129 | 0.190252 |
| y2_shift2 | Tier3_XGB_SCRM     |            0.203018 |   0.144395  | 0.388967 | 0.139789 |

*Note: High Recall with acceptable Precision is prioritized due to extreme class imbalance (3.16%). F1-Score acts as the definitive balancing metric.*
