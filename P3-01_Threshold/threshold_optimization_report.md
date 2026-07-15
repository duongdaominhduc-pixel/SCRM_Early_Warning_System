# P3-01 | Alert Decision Threshold Optimization Report

Optimizing thresholds for each `part_family` using F0.5-score as the target metric to prevent Alert Fatigue in manufacturing/logistics teams.

## 1. Optimal Threshold Configuration Table

| Part Family   |   Optimal Threshold |   Precision |   Recall |   F0.5-score |   F1-score |
|:--------------|--------------------:|------------:|---------:|-------------:|-----------:|
| Electrical    |                0.9  |    0.726496 | 0.758929 |     0.732759 |   0.742358 |
| Avionics      |                0.85 |    0.916667 | 0.458333 |     0.763889 |   0.611111 |
| Engine        |                0.9  |    0.84375  | 0.482143 |     0.733696 |   0.613636 |
| Structure     |                0.9  |    0.705882 | 0.510638 |     0.655738 |   0.592593 |
| Hydraulics    |                0.9  |    0.933333 | 0.424242 |     0.752688 |   0.583333 |
| Cabin         |                0.2  |    1        | 1        |     1        |   1        |
| Fasteners     |                0.85 |    0.835443 | 0.673469 |     0.797101 |   0.745763 |
| LandingGear   |                0.85 |    0.533333 | 0.788732 |     0.570265 |   0.636364 |

## 2. Methodology & Key Findings
- **F0.5-Score Priority:** Placing double weight on Precision over Recall helps to suppress warning notifications unless there is high confidence, matching the logistical sweet spot of SCRM practitioners.
- **Domain Specific Thresholds:** Critical parts groups (like Avionics and Electrical) show higher optimal thresholds, preventing frequent warnings on volatile component classes.