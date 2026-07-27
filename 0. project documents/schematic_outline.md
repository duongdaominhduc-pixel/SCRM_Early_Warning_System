# Schematic Outlines for the 2 Core Diagrams (SOTA V2.0)

This file defines the structure (Nodes) and flows (Edges) for drawing the two most important diagrams in the manuscript. It has been standardized based on the actual V2.0 system and **ensures 100% terminology alignment with the manuscript content**.

---

## 1. Research Methodology Framework Diagram

**Objective:** Visualize the journey from raw data to Actionable Intelligence.
**Recommended Style:** Vertical Flowchart (Top-Down) or Block Diagram.

### Mermaid Visualization

```mermaid
flowchart TD
    classDef data fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef phase fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef gate fill:#ffebee,stroke:#f44336,stroke-width:2px,stroke-dasharray: 5 5;

    subgraph Data Collection [Data Collection - Section 3.2]
        A[Textual Data Source<br/>GDELT & NewsAPI]:::data
        B[Operational Data Source<br/>Aerospace Inventory & Lead-time]:::data
    end

    subgraph Phase 0 [Phase 0: Sensing Layer]
        C[Binary Filter<br/>DistilBERT]:::phase
        D{QUALITY GATE 1<br/>Fleiss' Kappa = 0.785}:::gate
    end

    subgraph Phase 1 [Phase 1: Sense-making Layer]
        E[Taxonomy Extraction<br/>Multi-label Event Tagging]:::phase
        F[Severity Specialist<br/>Context Shells]:::phase
        G[Time-Series Alignment<br/>ISO Week Format]:::phase
    end

    subgraph Phase 2 [Phase 2: Feature Fusion & ML]
        H[ADF Stationarity Test<br/>& Delta Momentum]:::phase
        I[Feature Extraction<br/>Geographic Weighting]:::phase
        J[Walk-forward Validation<br/>5 Folds]:::phase
        K[Ablation Study<br/>Tier 1, 2, 3]:::phase
    end

    subgraph Phase 3 [Phase 3: Evaluation & Data Governance]
        L[Core Metrics<br/>PR-AUC, F1, Brier]:::phase
        M[Explainability<br/>SHAP Value]:::phase
        N{QUALITY GATE 2<br/>Lead-Time Gain Analysis}:::gate
    end

    A --> C
    B --> H
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J --> K
    K --> L
    L --> M
    M --> N

    N -. "Feedback Loop (Proactive Resilience)" .-> E
```

---

## 2. Proposed System Architecture Diagram

**Objective:** Display the internal structure of the 3-Stage AI model (Cascading AI).
**Recommended Style:** 3 Stacked Layers (Stage).

### Mermaid Visualization

```mermaid
flowchart TD
    classDef stage1 fill:#e8eaf6,stroke:#3f51b5,stroke-width:2px;
    classDef stage2 fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef stage3 fill:#fce4ec,stroke:#e91e63,stroke-width:2px;
    classDef lock fill:#fff3e0,stroke:#ff9800,stroke-width:2px,stroke-dasharray: 5 5;

    subgraph Stage1 [Stage 1: NLP Sensing & Taxonomy-Conditioned AI]
        L1_1[News Text Input]:::stage1
        L1_2[Binary Filter]:::stage1
        L1_3[UIE: Multi-label Event Tagging]:::stage1
        L1_4[Context Shells Injection<br/>e.g. PORT_CONGESTION]:::stage1
        L1_5[Severity Specialist]:::stage1
    end

    subgraph Stage2 [Stage 2: Operational Mapping & Feature Generation]
        L2_1[Geographic Weighting<br/>Exact=1.0, Country=0.6, Region=0.3, Global=0.1]:::stage2
        L2_2[Inbound Metrics Extraction]:::stage2
        L2_3[Delta Features Generation]:::stage2
    end

    subgraph Stage3 [Stage 3: Intelligence Fusion & Data Integrity]
        L3_1[Feature Matrix X<br/>W-1, W-2]:::stage3
        L3_2{INTEGRITY LOCK<br/>SHA256 Checksum}:::lock
        L3_3[XGBoost Model<br/>Cost-Sensitive]:::stage3
        L3_4[Target Shift Mechanism<br/>Forecast Y at W+1, W+2]:::stage3
    end

    Out1([Output Stage 1:<br/>at_risk_count, high_severity_count, dominant_event_type])
    Out2([Output Stage 2:<br/>weighted_geo_risk_w1, avg_actual_lead_time_w1, etc.])
    Out3([Final Output:<br/>Early Warning Alert Probability & SHAP Explanations])

    L1_1 --> L1_2 --> L1_3 --> L1_4 --> L1_5
    L1_5 --> Out1

    Out1 --> L2_1
    Out1 --> L2_2
    L2_1 --> L2_3
    L2_2 --> L2_3
    L2_3 --> Out2

    Out2 --> L3_1
    L3_1 --> L3_2 --> L3_3 --> L3_4
    L3_4 --> Out3
```
