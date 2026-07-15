# P5 Evaluation Report — Supply Chain Risk Monitoring (SCRM)
## Level 3 (L3) Research Deliverable

> **Status**: SKELETON — replace all `[PLACEHOLDER]` values with results from
> the corresponding pipeline scripts before submission.

---

## 1. Executive Summary

This report presents the evaluation results for the ML-based supply chain risk
prediction pipeline.  Two models were compared using 5-fold walk-forward
cross-validation on weekly `(part_group × week)` observations:

| Model | Features used |
|-------|---------------|
| Logistic Regression (baseline) | Operational features 1-7 |
| XGBoost (main) | All 10 features (operational + NLP) |

**Key finding**: [PLACEHOLDER — e.g., "XGBoost improved AUC by +X.XX over
baseline, with mean lead time of warning of X.X weeks."]

---

## 2. Dataset

| Item | Value |
|------|-------|
| Observation unit | (part_group × week) |
| Total observations | [PLACEHOLDER] |
| Positive class rate (y=1) | [PLACEHOLDER] % |
| Date range | [PLACEHOLDER] to [PLACEHOLDER] |
| CV scheme | Walk-forward, 5 folds × 13 weeks |

**Positive label definition**:  
`y_true = 1` if `on_hand_qty ≤ 0` **OR** `receipt_date > promised_date`
in that week; else `0`.

---

## 3. Feature Matrix (10 Features)

| # | Feature | Type | Source | Status |
|---|---------|------|--------|--------|
| 1 | `burn_rate_daily` | Operational | TTS computation | Real |
| 2 | `TTS_days` | Operational | TTS computation | Real |
| 3 | `avg_delivery_delay` | Operational | Purchase orders | Real |
| 4 | `pct_late_deliveries` | Operational | Purchase orders | Real |
| 5 | `quality_incident_rate` | Operational | QA records | Real |
| 6 | `supplier_risk_class` | Operational (encoded) | Supplier master | Real |
| 7 | `criticality_class` | Operational (encoded) | Part master | Real |
| 8 | `news_risk_score` | NLP | P3-12 output | **MOCK** |
| 9 | `disruption_event_flag` | NLP | P3-12 output | **MOCK** |
| 10 | `severity_score` | NLP | P3-12 output | **MOCK** |

---

## 4. Model Performance — Walk-Forward CV

### 4.1 Logistic Regression Baseline (features 1-7)

Source: `P5-07/baseline_results.json`

| Fold | Recall | Precision | F1 | AUC |
|------|--------|-----------|----|-----|
| 1 | [PH] | [PH] | [PH] | [PH] |
| 2 | [PH] | [PH] | [PH] | [PH] |
| 3 | [PH] | [PH] | [PH] | [PH] |
| 4 | [PH] | [PH] | [PH] | [PH] |
| 5 | [PH] | [PH] | [PH] | [PH] |
| **AVG** | **[PH]** | **[PH]** | **[PH]** | **[PH]** |

### 4.2 XGBoost Main Model (all 10 features)

Source: `P5-08/xgb_results.json`

| Fold | Recall | Precision | F1 | AUC | scale_pos_weight |
|------|--------|-----------|----|-----|-----------------|
| 1 | [PH] | [PH] | [PH] | [PH] | [PH] |
| 2 | [PH] | [PH] | [PH] | [PH] | [PH] |
| 3 | [PH] | [PH] | [PH] | [PH] | [PH] |
| 4 | [PH] | [PH] | [PH] | [PH] | [PH] |
| 5 | [PH] | [PH] | [PH] | [PH] | [PH] |
| **AVG** | **[PH]** | **[PH]** | **[PH]** | **[PH]** | — |

### 4.3 Delta (XGBoost − Baseline)

Source: `P5-09/model_comparison.md`

| Metric | Baseline | XGBoost | Delta |
|--------|----------|---------|-------|
| Recall | [PH] | [PH] | [PH] |
| Precision | [PH] | [PH] | [PH] |
| F1 | [PH] | [PH] | [PH] |
| AUC | [PH] | [PH] | [PH] |

---

## 5. Optimal Decision Threshold

Source: `P5-11/optimal_threshold.json`

Method: **Youden's J-statistic** (`Sensitivity + Specificity − 1`), evaluated
at each point on the ROC curve.  The threshold that maximises J is selected —
no hardcoded value is used.

| Parameter | Value |
|-----------|-------|
| Optimal threshold | [PLACEHOLDER] |
| Sensitivity (TPR) | [PLACEHOLDER] |
| Specificity | [PLACEHOLDER] |
| Youden's J | [PLACEHOLDER] |

---

## 6. SHAP Feature Importance

Source: `P5-10/shap_importance_summary.csv`

> **Note**: NLP features (8-10) are currently MOCK — SHAP values will change
> substantially once real P3-12 outputs are integrated.

| Rank | Feature | Mean |SHAP| | NLP? |
|------|---------|-------------|------|
| 1 | [PLACEHOLDER] | [PH] | |
| 2 | [PLACEHOLDER] | [PH] | |
| 3 | [PLACEHOLDER] | [PH] | |
| … | … | … | |
| 8 | `news_risk_score` | [PH] | MOCK |
| 9 | `disruption_event_flag` | [PH] | MOCK |
| 10 | `severity_score` | [PH] | MOCK |

---

## 7. Alert Generation

Source: `P5-12/weekly_alerts.csv`

| Metric | Value |
|--------|-------|
| Total observations | [PLACEHOLDER] |
| Alerts raised | [PLACEHOLDER] |
| Alert rate | [PLACEHOLDER] % |
| Threshold used | [PLACEHOLDER] (Youden's J) |

---

## 8. Lead Time of Warning (LTW)

Source: `P5-13/lead_time_results.json`

The LTW measures how many weeks in advance the model correctly flagged an
upcoming supply disruption.

| Metric | Value |
|--------|-------|
| True positives with positive LTW | [PLACEHOLDER] |
| **Mean LTW** | **[PLACEHOLDER] weeks** |
| Median LTW | [PLACEHOLDER] weeks |
| Min LTW | [PLACEHOLDER] weeks |
| Max LTW | [PLACEHOLDER] weeks |

---

## 9. Limitations and Next Steps

1. **NLP features are MOCK** — `news_risk_score`, `disruption_event_flag`,
   and `severity_score` use random values.  Replace with P3-12 output and
   re-run P5-08 through P5-14 for final numbers.

2. **Hyperparameter tuning** — XGBoost uses default `n_estimators=100`,
   `max_depth=4`.  A grid/Bayesian search over these parameters is
   recommended.

3. **Calibration** — Predicted probabilities should be calibrated (e.g.,
   Platt scaling) if the alert threshold needs to be interpretable as a
   true probability of disruption.

4. **External validation** — The walk-forward CV uses historical data only.
   Prospective validation on a future quarter is recommended before
   production deployment.

---

## 10. Pipeline Script Reference

| Task | Script | Key Output |
|------|--------|------------|
| P5-06 | `walk_forward_cv.py` | `WalkForwardCV` class |
| P5-07 | `train_baseline.py` | `baseline_results.json` |
| P5-08 | `train_xgboost.py` | `xgb_model.json`, `xgb_results.json` |
| P5-09 | `compare_models.py` | `model_comparison.md` |
| P5-10 | `shap_analysis.py` | `shap_values.csv`, `shap_importance_summary.csv` |
| P5-11 | `find_threshold.py` | `optimal_threshold.json` |
| P5-12 | `generate_alerts.py` | `weekly_alerts.csv` |
| P5-13 | `lead_time_warning.py` | `lead_time_results.json` |
| P5-14 | `evaluation_report_L3.md` | This document |

---

*Template generated by SCRM ML Pipeline skeleton.
Replace all [PLACEHOLDER] / [PH] values before submission.*
