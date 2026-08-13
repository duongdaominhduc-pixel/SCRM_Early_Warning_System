# Schematic Outlines for the 2 Core Diagrams (SOTA V2.0)

This file defines the structure (Nodes) and flows (Edges) for drawing the two most important diagrams in the manuscript. It has been strictly designed based on sections 3.2 to 3.6 of the article `SCRM_EWS_draft_article_v2.md`.

---

## 1. Research Methodology Framework Diagram

**Objective:** Visualize the journey from raw data to Actionable Intelligence, showcasing the transition from Reactive to Proactive SCRM (Preemptive Mitigation Feedback Loop).
**Recommended Style:** Vertical Flowchart (Top-Down) or Block Diagram.

### Text-Based Visual Reference (Mermaid)
You can use this layout as a direct visual guide:

```mermaid
flowchart TD
    subgraph Preparation ["Data Collection (Section 3.2)"]
        A[Textual Data Source<br>Four Major Industry News Portals<br>8,728 articles]
        B[(Operational Data Source<br>ERP: parts, PO, history, quality, locations)]
    end

    subgraph Phase_0 ["Phase 0 - Sensing Layer (Section 3.3)"]
        C0[Manual Labeling<br>2,309 articles]
        C1[Binary Filter<br>DistilBERT Risk Filtering]
        C2{{[QUALITY GATE 1]<br>Fleiss' Kappa = 0.785<br>Cohen's Kappa = 0.635}}
        A --> C0 --> C1 --> C2
    end

    subgraph Phase_1 ["Phase 1 - Sense-making Layer (Section 3.4)"]
        D1[Taxonomy Extraction<br>BART-large-MNLI Zero-shot]
        D2[Severity Specialist<br>Context Shells]
        C2 --> D1 --> D2
    end

    subgraph Phase_2 ["Phase 2 - Feature Fusion & Machine Learning (Section 3.5)"]
        E1[Time-Series Aggregation<br>Weekly Frequency - ISO Week]
        E2[Geographic Mapping & Weighting<br>1.0, 0.6, 0.3, 0.1]
        E3[ADF Stationarity Test &<br>Delta Momentum]
        E4[3-Tier Ablation Study<br>Walk-forward Validation]
        
        D2 --> E1
        E1 --> E2
        B --> E2
        E2 --> E3 --> E4
    end

    subgraph Phase_3 ["Phase 3 - Evaluation & Data Governance (Section 3.6)"]
        F1[Core Metrics<br>PR-AUC, F1, ECE]
        F2[Explainability<br>SHAP]
        F3{{[QUALITY GATE 2]<br>SHA-256 Data Governance}}
        E4 --> F1 --> F2 --> F3
    end

    F3 -.->|Preemptive Mitigation<br>Feedback Loop| B
    
    style C2 stroke:#ff0000,stroke-width:2px,stroke-dasharray: 5 5
    style F3 stroke:#ff0000,stroke-width:2px,stroke-dasharray: 5 5
```

### Key Nodes & Edges:

**Data Collection (Section 3.2)**
- **Node A: Textual Data Source (GDELT & NewsAPI)**.
- **Node B: Operational Data Source (ERP)**. Comprises 5 datasets.

**Phase 0: Sensing Layer (Section 3.3)**
- **Node C0: Manual Labeling (2,309 articles)**.
- **Node C1: Binary Filter (DistilBERT)**. The Gatekeeper.
- **Node C2: [QUALITY GATE 1]**. Fleiss' Kappa = 0.785 & Cohen's Kappa = 0.635.
- *Connections:* `A -> C0 -> C1 -> C2`. Output flows to Phase 1.

**Phase 1: Sense-making Layer (Section 3.4)**
- **Node D1: Taxonomy Extraction (BART-large-MNLI)**. Zero-shot multi-label classification.
- **Node D2: Severity Specialist (Context Shells)**.
- *Connections:* `C2 -> D1 -> D2`. Output flows to Phase 2.

**Phase 2: Feature Fusion and Machine Learning (Section 3.5)**
- **Node E1: Time-Series Aggregation (Weekly)**.
- **Node E2: Geographic Mapping & Weighting**. Fuses textual insights with ERP data using weights `{1.0, 0.6, 0.3, 0.1}`.
- **Node E3: ADF Stationarity Test & Delta Momentum**.
- **Node E4: 3-Tier Ablation Study (Walk-forward Validation)**.
- *Connections:* `D2 -> E1`. `(E1 + Node B) -> E2`. `E2 -> E3 -> E4`.

**Phase 3: Evaluation and Data Governance (Section 3.6)**
- **Node F1: Core Metrics (PR-AUC, F1, ECE)**.
- **Node F2: Explainability (SHAP)**.
- **Node F3: [QUALITY GATE 2] SHA-256 Data Governance**.
- *Connections:* `E4 -> F1 -> F2 -> F3`.
- *Feedback Loop:* Dashed arrow (`F3 -> Node B`) demonstrating the Preemptive Mitigation Feedback Loop that alters operational outcomes.

---

## 2. Proposed System Architecture Diagram

**Objective:** Display the internal structure of the 3-Stage AI model (Cascading AI) from a software architecture perspective.
**Recommended Style:** 3 Stacked Layers (Stage).

### Text-Based Visual Reference (Mermaid)
You can use this layout as a direct visual guide:

```mermaid
flowchart TD
    subgraph Stage_1 ["Stage 1: NLP Sensing & Taxonomy-Conditioned AI"]
        L1_1[News Text Input]
        L1_2[Binary Filter]
        L1_3[Universal Information Extraction<br>Taxonomy]
        L1_4[Context Shells Injection]
        L1_5[Severity Specialist]
        L1_1 --> L1_2 --> L1_3 --> L1_4 --> L1_5
        Out1([Output L1<br>at_risk_count, high_severity_count, dominant_event_type])
        L1_5 --> Out1
    end

    subgraph Stage_2 ["Stage 2: Operational Mapping & Feature Generation"]
        L2_1[Geographic Weighting<br>Exact=1.0, Country=0.6, Region=0.3, Global=0.1]
        L2_2[Inbound Metrics Extraction<br>from ERP]
        L2_3[Delta Features Generation<br>delta_avg_actual_lead_time]
        Out1 --> L2_1
        Out1 -.->|Contextual trigger| L2_2
        L2_1 --> L2_3
        L2_2 --> L2_3
        Out2([Output L2<br>weighted_geo_risk_w1, delta_avg_actual_lead_time_w1...])
        L2_3 --> Out2
    end

    subgraph Stage_3 ["Stage 3: Intelligence Fusion & Data Integrity"]
        L3_1[Feature Matrix X<br>Combines Output L1 & L2 at W-1, W-2]
        L3_2{{[INTEGRITY LOCK]<br>SHA-256 Checksum}}
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
- **Nodes:** News Text -> Binary Filter -> UIE (Taxonomy) -> Context Shells -> Severity Specialist.
- **Output L1:** `at_risk_count`, `high_severity_count`, `dominant_event_type`.

**Stage 2: Operational Mapping & Feature Generation**
- **Nodes:** Receives Output L1 -> Geographic Weighting (cross-referenced with Inbound Metrics from ERP) -> Delta Features Generation.
- **Output L2:** Features like `weighted_geo_risk_w1`, `delta_avg_actual_lead_time_w1`.

**Stage 3: Intelligence Fusion & Data Integrity**
- **Nodes:** Receives Output L2 to build Feature Matrix X -> **Integrity Lock (SHA-256)** -> XGBoost (Cost-Sensitive) -> Forecast Y (W+1, W+2).
- **Final Output:** Early Warning Alert Probability & SHAP Explanations.
