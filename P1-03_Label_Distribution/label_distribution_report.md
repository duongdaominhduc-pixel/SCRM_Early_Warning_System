# P1-03 | Label Distribution & Anti-Overfitting Report (Version 2.0)

## 1. Corpus Statistics
- **Total Articles:** 8728
- **At Risk (Label 1 + 2):** 5762 (66.02%)

## 2. Gate Verification

| Gate | Requirement | Actual Value | Status |
|---|---|---|---|
| Stage 1 (Binary Filter) | AT_RISK Rate >= 15% | 66.02% | PASSED |
| Stage 2 (Severity) | Accept Natural Imbalance (No SMOTE) | 25.91% | PASSED (V2.0 Rule) |

## 3. Class Counts of Final Corpus
|   label |   count |
|--------:|--------:|
|       0 |    2966 |
|       1 |    2951 |
|       2 |    2811 |

## 4. Checksums of Output Files
- **`pseudo_labeled_final.csv` (SHA256):** `5d99d69ada0e922e3545bfa5175698329d923bcd263f726ace4f704cecfbe64d`