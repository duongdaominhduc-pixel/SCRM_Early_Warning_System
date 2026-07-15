# P1-02 | Weekly Feature Aggregation (X matrix)

This phase fuses unstructured NLP risk signals (from global news) with structured internal operational data (from ERP systems) into a unified weekly time-series feature matrix. 

## Academic Risk Mitigations Implemented:
1. **Conservative Information-Processing (No Look-Ahead)**: Features for predicting Week W are strictly derived from W-1 and W-2.
2. **Data Sparsity & Geographic Weighting**: Implements a continuous `geo_match_score` based on the Ripple Effect (tunable hyperparameter `region_weight`).
3. **Data Latency (Monday Morning Reality)**: Supports "Stress Testing" via a Sensitivity Analysis flag (`--use_w2_ops=True`) to validate robustness against ERP reporting lags.
4. **Multicollinearity**: Uses Lasso-Logistic regression for automated feature selection, paired with SHAP values for "white-box" managerial interpretability.

## Pipeline Scripts
- `01_preprocess_news.py`: Joins NER and event data, handles date standardisation (ISO 8601), and maps GPEs to Country and Region codes.
- `02_aggregate_operational.py`: Aggregates internal ERP data (purchase orders, inventory, supply chain history) into weekly ISO bins.
- `03_build_feature_matrix.py`: Merges NLP and operational features using time-shifted joins (W-1, W-2) and computes `geo_match_score` with geographic weighting.
- `04_multicollinearity_check.py`: Calculates VIF, trains a Lasso-Logistic model, and extracts SHAP values to explain feature importance.

## Usage
Run the scripts sequentially:
```bash
py scripts/01_preprocess_news.py
py scripts/02_aggregate_operational.py
py scripts/03_build_feature_matrix.py --region_weight 0.6
py scripts/04_multicollinearity_check.py
```
