# Schematic Outlines for the 2 Core Diagrams (SOTA V2.0)

This file defines the structure (Nodes) and flows (Edges) for drawing the two most important diagrams in the manuscript. It has been standardized based on the actual V2.0 system and **ensures 100% terminology alignment with the manuscript content (Phases 0-3, Geographic Weighting, Cascading Stage)**.

---

## 1. Research Methodology Framework Diagram

**Objective:** Visualize the journey from raw data to Actionable Intelligence.
**Recommended Style:** Vertical Flowchart (Top-Down) or Block Diagram.

> **⚠️ UPDATE REQUIREMENT:** Rename the blocks (Phases) to perfectly match section 3. Methodology in the manuscript (starting from Phase 0). Separate Data Collection from the main Phases.

### Text-Based Visual Reference (Mermaid)
You can use this layout as a direct visual guide:

```mermaid
flowchart TD
    subgraph Data_Collection ["Preparation (Section 3.2)"]
        A[Textual Data Source<br>GDELT & NewsAPI<br>2022-2024, ~7,200 articles]
        B[(Operational Data Source<br>Aerospace Inbound Logistics<br>Inventory & Lead-time)]
    end

    subgraph Phase_0 ["Block 1: Phase 0 - Sensing Layer (Section 3.3)"]
        C[Binary Filter<br>DistilBERT Risk Filtering]
        D{{[QUALITY GATE 1]<br>Fleiss' Kappa = 0.785<br>Cohen's Kappa = 0.635}}
        C --> D
    end

    subgraph Phase_1 ["Block 2: Phase 1 - Sense-making Layer (Section 3.4)"]
        E[Taxonomy Extraction<br>Multi-label Event Tagging]
        F[Severity Specialist<br>Context Shells]
        G[Time-Series Alignment<br>ISO Week format]
        E --> F --> G
    end

    subgraph Phase_2 ["Block 3: Phase 2 - Feature Fusion & ML (Section 3.5)"]
        H[ADF Stationarity Test &<br>Delta Momentum]
        I[Feature Extraction<br>Geographic Weighting]
        J[Walk-forward Validation<br>5 Folds, Chronological]
        K[Ablation Study<br>Tier 1, Tier 2, Tier 3 Hybrid]
        H --> I --> J --> K
    end

    subgraph Phase_3 ["Block 4: Phase 3 - Evaluation & Governance (Section 3.6)"]
        L[Core Metrics<br>PR-AUC, F1, Brier Score]
        M[Explainability & Viz<br>SHAP Value]
        N{{[QUALITY GATE 2]<br>Lead-Time Gain Analysis}}
        L --> M --> N
    end

    A --> Phase_0
    B --> Phase_2
    Phase_0 --> Phase_1
    Phase_1 --> Phase_2
    Phase_2 --> Phase_3

    Phase_3 -.->|Feedback Loop<br>Proactive Resilience| Phase_1
    
    style D stroke:#ff0000,stroke-width:2px,stroke-dasharray: 5 5
    style N stroke:#ff0000,stroke-width:2px,stroke-dasharray: 5 5
```

### Key Nodes & Edges:

**Preparation (Data Collection - Corresponding to section 3.2):**
- Node A: Textual Data Source (GDELT Project & NewsAPI, 2022-2024, ~7,200 articles).
- Node B: Operational Data Source (Aerospace Inbound Logistics, Inventory & Lead-time).
- *Arrow:* Pointing down to Block 1.

**Block 1: Phase 0 - Sensing Layer (Corresponding to section 3.3)**
- Node C: Binary Filter (Risk filtering using DistilBERT).
- Node D: *[QUALITY GATE 1]* Fleiss' Kappa = 0.785 & Cohen's Kappa = 0.635 (dashed border, red color).

**Block 2: Phase 1 - Sense-making Layer (Corresponding to section 3.4)**
- Node E: Taxonomy Extraction (Multi-label Event Tagging).
- Node F: Severity Specialist (Severity assessment using Context Shells).
- Node G: Time-Series Alignment – ISO Week format.

**Block 3: Phase 2 - Feature Fusion and Machine Learning (Corresponding to section 3.5)**
- Node H: ADF Stationarity Test & Delta Momentum.
- Node I: Feature Extraction (Geographic Weighting).
- Node J: Walk-forward Validation (5 Folds, Chronological Split).
- Node K: Ablation Study (Tier 1 Baseline, Tier 2 Baseline, Tier 3 Hybrid).

**Block 4: Phase 3 - Evaluation and Data Governance (Corresponding to section 3.6)**
- Node L: Core Metrics (PR-AUC, F1-Score, Brier Score).
- Node M: Explainability & Visualization (SHAP Value).
- Node N: *[QUALITY GATE 2]* Lead-Time Gain (LTG) Analysis (Economic efficiency assessment).
- *Feedback flow:* Dashed arrow (Feedback Loop) returning to Phase 1 (demonstrating Proactive Resilience).

---

## 2. Proposed System Architecture Diagram

**Objective:** Display the internal structure of the 3-Stage AI model (Cascading AI).
**Recommended Style:** 3 Stacked Layers (Stage).

> **⚠️ UPDATE REQUIREMENT:** 
> 1. Change the word "Layer" to "Stage" to align with the "four-stage Cascading AI architecture" keyword in section 3.1.
> 2. Add all 4 Geographic Weighting constants (Exact, Country, Region, Global).

### Text-Based Visual Reference (Mermaid)
You can use this layout as a direct visual guide:

```mermaid
flowchart TD
    subgraph Stage_1 ["Stage 1: NLP Sensing & Taxonomy-Conditioned AI"]
        L1_1[News Text Input]
        L1_2[Binary Filter]
        L1_3[Universal Information Extraction<br>Multi-label Event Tagging]
        L1_4[Context Shells Injection<br>[PORT_CONGESTION] Text...]
        L1_5[Severity Specialist]
        L1_1 --> L1_2 --> L1_3 --> L1_4 --> L1_5
        Out1([Stage 1 Output<br>at_risk_count, high_severity_count, dominant_event_type])
        L1_5 --> Out1
    end

    subgraph Stage_2 ["Stage 2: Operational Mapping & Feature Generation"]
        L2_1[Geographic Weighting<br>Exact=1.0, Country=0.6, Region=0.3, Global=0.1]
        L2_2[Inbound Metrics Extraction]
        L2_3[Delta Features Generation<br>delta_avg_actual_lead_time]
        Out1 --> L2_1
        Out1 -.->|Contextual trigger| L2_2
        L2_1 --> L2_3
        L2_2 --> L2_3
        Out2([Stage 2 Output<br>weighted_geo_risk_w1, avg_actual_lead_time_w1...])
        L2_3 --> Out2
    end

    subgraph Stage_3 ["Stage 3: Intelligence Fusion & Data Integrity"]
        L3_1[Feature Matrix X<br>Combines Output L1 & L2 at W-1, W-2]
        L3_2{{[INTEGRITY LOCK]<br>SHA256 Checksum}}
        L3_3[XGBoost Model<br>Cost-Sensitive Learning scale_pos_weight]
        L3_4[Target Shift Mechanism<br>Forecast Y at W+1, W+2]
        Out2 --> L3_1
        L3_1 --> L3_2 --> L3_3 --> L3_4
        Out3([Final Output<br>Early Warning Alert Probability & SHAP Explanations])
        L3_4 --> Out3
    end
    
    style L3_2 stroke:#ff0000,stroke-width:2px,stroke-dasharray: 5 5
```

### Key Nodes & Edges:

**Stage 1: NLP Sensing & Taxonomy-Conditioned AI**
- Node L1.1: News Text Input.
- Node L1.2: Binary Filter.
- Node L1.3: Universal Information Extraction (UIE) - Multi-label Event Tagging (Taxonomy).
- Node L1.4: Context Shells Injection (Example: `[PORT_CONGESTION] Text...`).
- Node L1.5: Severity Specialist.
- *Stage 1 Output:* `at_risk_count`, `high_severity_count`, `dominant_event_type`.

**Stage 2: Operational Mapping & Feature Generation**
- Node L2.1: Geographic Weighting (Spatial risk computation: **Exact=1.0, Country=0.6, Region=0.3, Global=0.1**).
- Node L2.2: Inbound Metrics Extraction.
- Node L2.3: Delta Features Generation (`delta_avg_actual_lead_time`).
- *Stage 2 Output:* `weighted_geo_risk_w1`, `avg_actual_lead_time_w1`, etc.

**Stage 3: Intelligence Fusion & Data Integrity**
- Node L3.1: Feature Matrix X (combining Output L1 and L2 at W-1 and W-2).
- Node L3.2: *[INTEGRITY LOCK]* Lock icon with `SHA256 Checksum`.
- Node L3.3: XGBoost Model (Cost-Sensitive Learning via `scale_pos_weight`).
- Node L3.4: Target Shift Mechanism (Forecast Y at W+1, W+2).
- *Final Output:* Early Warning Alert Probability & SHAP Explanations.
