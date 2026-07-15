# P1-04 | Data Fusion — Geographic Weighting (Soft Join)

This module replaces static "Hard Inner Joins" with dynamic **Geographic Weighting (Soft Join)** to accurately model network dependencies and the Ripple Effect in modern supply chains.

## Academic Framework
1. **Layered Risk Perception**: Recognizing that risk propagates across geographic borders. We employ **Initial Sensitivity Coefficients** calibrated by domain expertise:
   - `1.0`: Exact Match (Direct impact at supplier's country)
   - `0.6`: Regional Match (Spatial Propagation within the same continent)
   - `0.3`: Baseline Exposure Factor (Macro Events like GEOPOLITICAL or PORT_CONGESTION impacting global flows)
   - `0.1`: Remote Events
2. **Asymptotic Stability via Sensitivity Analysis**: To prevent cherry-picking allegations, this module recalculates risk scores across varying Regional weights (0.5, 0.6, 0.7) and reports on the variance, proving structural stability.

## Scripts
- `01_advanced_geo_join.py`: Performs the cross-join between news events and supplier locations for each week, applies the `geo_weight` penalty function, and executes the Sensitivity Analysis.

## Usage
Run the script using Python:
```bash
py scripts/01_advanced_geo_join.py
```
*Output*: `news_supplier_joined.parquet` and `sensitivity_analysis_report.md` will be generated in `pipeline_data/`.
