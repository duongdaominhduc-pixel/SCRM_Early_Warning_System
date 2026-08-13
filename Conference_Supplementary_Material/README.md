# EWS-SCRM (Early Warning System for Supply Chain Risk Management)

This repository contains the supplementary source code and documentation for the EWS-SCRM research project. The system is designed to forecast supply chain disruptions and inbound stockout risks. It leverages a Cascading AI Architecture to integrate global unstructured news data (NLP) with structured internal supply chain operational data (ERP/Logistics).

## 1. Overview of the Codebase

The repository is structured into sequential modules reflecting the four phases (Phase 0 to Phase 3) of the Cascading AI Architecture. Each phase executes specific data processing, natural language processing, or machine learning tasks.

### Reproducibility

The source code is modularized into sequential pipelines. Execution can be reproduced via three primary scripts located in the root directory:
*   `run_phase1_pipeline.py`: Executes Phase 0 and Phase 1 (Data Acquisition, Zero-shot Classification, Severity Specialist).
*   `run_phase2_pipeline.py`: Executes Phase 2 (Named Entity Recognition, Geographic Join, Feature Engineering, Walk-forward CV Ablation/Stress Test).
*   `run_phase3_pipeline.py`: Executes Phase 3 (Final Model Training, Global/Local SHAP Analysis, Threshold Optimization, Integration Case Study).

## 2. Methodological Highlights

During the development and validation of the models, strict standards were applied to preserve scientific integrity:

*   **Prevention of Data Leakage:** Instead of random splitting, the entire validation process (Phase 2 and Phase 3) utilizes a 5-Fold Walk-forward TimeSeriesSplit. The calculation of class weights (`scale_pos_weight`) is performed strictly within each fold (in-fold calculation) rather than globally.
*   **Fair Evaluation (Ablation & Stress Test):** In the Ablation and Stress Test studies, the decision threshold is fixed at the default level (t = 0.50). This isolates the native predictive capability of the algorithmic architecture and prevents threshold-tuning biases during structural comparisons.
*   **Operational Utility:** In Phase 3 (Lead-Time Gain evaluation), the Threshold Optimization technique is activated. Warning thresholds are optimized specifically for each component family to maximize the F0.5-score. This addresses the industrial challenge of alert fatigue by penalizing false positives.

## 3. Directory Structure

```text
Conference_Supplementary_Material/
├── P0-03_Pilot_Labeling/             # Phase 0: Pilot labeling and Fleiss' Kappa test
├── P0-04_Binary_Filter/              # Phase 0: Gatekeeper filter training (DistilBERT)
├── P1-01_Risk_Taxonomy/              # Phase 1: Taxonomy extraction (Zero-shot BART)
├── P1-02_Severity_Specialist/        # Phase 1: Risk severity assessment
├── P1-03_Label_Distribution/         # Phase 1: Distribution reports and SHA256 integrity
├── P2-01_NLP_NER/                    # Phase 2: Named Entity Recognition (NER)
├── P2-02_Geo_Join/                   # Phase 2: Soft Join and Geographic Weighting
├── P2-03_Feature_Matrix/             # Phase 2: ADF testing and Delta variables (Momentum)
├── P2-04_Derive_y2/                  # Phase 2: Target variable initialization (Target Shifting)
├── P2-05_ML_Ablation/                # Phase 2: Model benchmarking and Stress Test (W-2)
├── P3-01_Threshold/                  # Phase 3: Per-Family warning threshold optimization
├── P3-02_SHAP/                       # Phase 3: Model interpretation (Global/Local SHAP)
├── P3-03_Integration/                # Phase 3: Case study analysis and Lead-time Gain
├── run_phase1_pipeline.py            # Execution script for Phase 1
├── run_phase2_pipeline.py            # Execution script for Phase 2
├── run_phase3_pipeline.py            # Execution script for Phase 3
└── requirements.txt                  # Python dependencies
```

*Note: Heavy data files (.parquet, .csv, .pkl models) are intentionally excluded from this supplementary package to comply with size limitations and protect proprietary operational data.*
