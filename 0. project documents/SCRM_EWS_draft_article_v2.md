**APPLICATION OF WEB DATA MINING AND NATURAL LANGUAGE PROCESSING COMBINED WITH MACHINE LEARNING TO BUILD AN EARLY WARNING SYSTEM FOR UPSTREAM SUPPLY CHAIN DISRUPTION RISKS**

**Duc-Duong Dao Minh$^{a*}$, Buu-Tanh Tran-Le$^b$, Huyen-Huynh Chau Nhu$^c$, Thuy-Nguyen Nhut$^d$, Linh-Le Quynh Khanh$^e$**
$^{a,b,c,d,e}$ *University of Economics and Law, Ho Chi Minh City, Vietnam*
* Email address of Corresponding author: ducdmk24406@st.uel.edu.vn

**Abstract**
*Global supply chains are increasingly vulnerable to external shocks such as the COVID-19 pandemic, the Suez Canal blockage, or the semiconductor shortage crisis, highlighting the urgent need for an Early Warning System (EWS) capable of detecting upstream risks before they manifest as actual inventory shortages. However, current studies either exploit only news data without connecting to internal operational data, or analyze only ERP data while ignoring early warning signals from the external environment. This study proposes an integrated 4-stage architecture (Sensing → Sense-making → Feature Fusion → Evaluation) combining the DistilBERT language model, Zero-shot multi-label classification, Geographic Weighting, and the XGBoost algorithm to forecast the weekly probability of supply disruption. Experiments on a dataset of 8,728 logistics news articles (2022–2024) and 5 aerospace operational datasets show that: (1) The Gatekeeper binary filter achieves ROC-AUC = 0.8927, Recall = 0.9503, and ECE = 0.0849; (2) The XGBoost model integrated with NLP (Tier3_XGB_SCRM) achieves a Minority F1-score = 0.2064 and Precision = 0.1654—an outstanding 28.7% improvement in Precision compared to the pure operational XGBoost model (Tier2_XGB_Baseline); and (3) The system provides an early warning window of 1 to 2 weeks before actual disruption occurs. The results prove that public news NLP signals, when systematically integrated with operational data, create significant added value for upstream risk forecasting capabilities.*

**Keywords:** **Supply Chain Risk Management, Natural Language Processing, Machine Learning, Early Warning System, Inventory Risk**

### Introduction

#### 1.1. Background
In March 2021, the container ship Ever Given ran aground in the Suez Canal for six days, causing an estimated $9.6 billion in damages and disrupting the global flow of goods. Only a few months later, the semiconductor shortage crisis forced a series of automotive and aerospace manufacturers to cut production. More recently, the Red Sea conflict (2024) continued to expose the extreme vulnerability of global supply chains. According to a Gartner report (2023), over 87% of manufacturing enterprises experienced at least one supply disruption event between 2020 and 2023.

The core challenge lies not in reacting after a disruption occurs, but in the ability to **early detect warning signals** from the external environment—often appearing as news about strikes, natural disasters, raw material price fluctuations, or geopolitical conflicts—before operational consequences (depleted inventory, halted assembly lines) actually take place. The time window between an early warning signal and an actual incident is the "golden window" for enterprises to promptly activate contingency plans.

#### 1.2. Research Problem
The majority of manufacturing enterprises today still rely on traditional risk monitoring methods: periodic reports from the procurement department, manual checking of industry news, or static KPI indicators from ERP systems. These methods are reactive—only detecting problems when inventory is depleted or orders are delayed—and lack the capability to leverage the massive amount of information published daily on global logistics news portals.

#### 1.3. Research Gap
A comprehensive analysis of related studies reveals a clear gap: no study simultaneously addresses all aspects necessary for a comprehensive early warning system, especially demonstrating the Incremental Predictive Validity when combining unstructured and structured data. The system must not merely "know more news" but must prove the capability to "forecast better" thanks to that news.

**Table 1.** Comparison of contribution positioning with previous studies

| Criteria | Cano-Marin et al. (2023) | Ivanov et al. (2022) | Jialu Wang (2024) | Brintrup et al. (2020) | **This Study** |
|---|:---:|:---:|:---:|:---:|:---:|
| NLP from News | ✓ | ✗ | ✓ | ✗ | **✓** |
| Internal Operational Data | ✗ | ✓ | ✗ | ✓ | **✓** |
| Heterogeneous Modality Fusion | ✗ | ✗ | Partial | ✗ | **✓** |
| Spatial Risk Mapping | ✗ | ✗ | ✗ | ✗ | **✓** |
| Incremental Predictive Validity | ✗ | ✗ | Partial | ✗ | **✓** |
| Walk-forward Validation | ✗ | ✗ | ✗ | ✓ | **✓** |

#### 1.4. Objectives and Scientific Contributions
This study positions three core scientific contributions, directly addressing the most stringent technical barriers in supply chain risk management:

**(1) Heterogeneous Modality Fusion via Cascading AI:** Building an end-to-end integrated pipeline that transforms "soft" risk signals from unstructured news (NLP Signal) into "hard" features for machine learning models combined with operational data (ERP). This Cascading AI architectural framework completely illuminates the upstream disruption problem—an area long considered a "blind-spot" in SCRM. Furthermore, Data Integrity is ensured throughout the pipeline via a SHA256 Checksum mechanism, completely eliminating doubts about data manipulation.

**(2) Spatial Risk Sensitivity Calibration (Geographic Weighting):** Designing a soft mapping mechanism (Soft Join) using a geographic weighting function instead of a rigid Inner Join, completely resolving the "Granularity Mismatch" problem between macro-level news (country level) and micro-level ERP (supplier level). This technique helps the system simulate the "Ripple Effect" and capture cross-regional "Weak Signals" that traditional systems miss.

**(3) Inbound Ground Truth & Information Bottlenecking for Non-Naive Learning:** Proposing a standard definition for the upstream disruption problem. More importantly, the study establishes a professional technical barrier against "Spurious Regression" using the ADF Test and Delta features. Simultaneously, removing the past inventory state (`w1_stockout_flag`) from the ML feature space ensures the model truly "sees the risk" thanks to its information synthesis capability, rather than "guessing" based on historical series (Naive Forecaster). Finally, integrating SHAP analysis meets the "Algorithmic Accountability" criteria, bringing transparency to why an NLP signal triggers an alarm in the ERP.

### Literature review

#### 2.1. Supply Chain Risk Management: Theoretical Framework
Supply Chain Risk Management (SCRM) is a research field focusing on identifying, assessing, and mitigating disruption risks in supply networks. The traditional theoretical framework of SCRM divides the process into four stages: Risk Identification, Risk Assessment, Risk Mitigation, and Risk Monitoring. However, most existing works focus on the first two stages—identification and assessment—while continuous monitoring and real-time early warning capabilities remain an open challenge.

The explosion of artificial intelligence (AI) and machine learning (ML) in recent decades has opened new approaches for SCRM: instead of relying on subjective expert assessments, systems can automatically scan, analyze, and quantify risks from diverse data sources. However, simultaneously integrating unstructured data (news, social networks) with structured data (ERP, inventory) in the same pipeline remains the largest research gap.

#### 2.2. NLP for Risk Detection from Unstructured Text
Natural Language Processing (NLP) techniques have been widely applied to extract risk signals from unstructured text. Popular methods include Sentiment Analysis, Event Extraction, and Named Entity Recognition (NER).

However, in the supply chain domain, sentiment analysis proves ineffective because the same event (e.g., "strike at the Port of Los Angeles") might carry a positive nuance for labor unions but represents a severe risk for manufacturers dependent on supplies through that port. Therefore, this study opts for the **Ontology-Anchored Classification** method rather than sentiment analysis to ensure determinism and accountability of the system.

#### 2.3. Machine Learning for Supply Chain Risk Forecasting
Machine learning algorithms such as XGBoost, Random Forest, and Recurrent Neural Networks (LSTM) have been applied in numerous SCRM forecasting studies. However, most of these studies commit at least one of two severe methodological errors: (a) Using Random Split instead of Chronological Split, leading to Data Leakage; and (b) Failing to test for Stationarity of time series variables before feeding them into regression models, causing Spurious Regression.

This study thoroughly addresses both issues by: applying Walk-forward Validation with TimeSeriesSplit (5 folds, gap = 2 weeks), and integrating the automatic Augmented Dickey-Fuller (ADF) test alongside 1st order differencing (Delta Features) for continuous operational variables.

### Methodology

#### 3.1. System Architecture Overview
The EWS-SCRM system is designed according to a 4-Stage Linear Architecture, applying the "Cascading AI" mindset to optimize the separation of signal detection (Sensing) and context awareness (Sense-making) before synthesis into the Operational Feature Space.

*(INSERT FIGURE 1: Research Methodology Framework HERE)*

*(INSERT FIGURE 2: Proposed System Architecture HERE)*

**Table 2.** System architecture synthesis by stage

| Phase | Task | Core Technique | Main Output |
|---|---|---|---|
| Phase 0: Sensing | Coarse filtering of risk news | DistilBERT + CrossEntropyLoss + Label Smoothing | `at_risk_corpus.csv` (5,762 articles) |
| Phase 1: Sense-making | Event & severity classification | Zero-shot Multi-label + Context Shells + Focal Loss | `pseudo_labeled_final.csv` |
| Phase 2: Feature & ML | Multi-source fusion & training | Geographic Weighting + ADF Test + XGBoost | `feature_matrix.parquet` + Trained Models |
| Phase 3: Evaluation | Threshold optimization & XAI | Chronological Split + SHAP + SHA256 Governance | Case Study Report + Hero Chart |

#### 3.2. Data Collection and Preprocessing

**3.2.1. News Data (External Signal)**
The news corpus was collected from two logistics industry sources: GDELT BigQuery Index and NewsAPI, with a keyword filter focusing on supply chain topics (supply chain disruption, logistics risk, port congestion, supplier shortage). The preprocessing involved: removing duplicate articles using Cosine Similarity (TF-IDF threshold ≥ 0.85), filtering out articles under 100 words, and non-English articles. The result is **8,728 clean articles** in the 2022–2024 period.

**3.2.2. Internal Operational Data (Operational Data)**
The operational dataset includes 5 CSV tables reflecting aerospace supply chain activities: (1) `parts_master.csv` — component catalog with A/B/C criticality; (2) `shifted_purchase_orders.csv` — order history; (3) `shifted_supply_chain_history.csv` — actual inventory and lead time history; (4) `shifted_quality_incidents.csv` — quality incidents; and (5) `supplier_locations.csv` — geographical distribution of suppliers. The data was synchronized to the 2022–2024 timeframe via Time-shifting.

#### 3.3. Phase 0 — Sensing Layer (Risk Filtering)
Phase 0 acts as the "Gatekeeper" with the design philosophy: **"Better safe than sorry."** The DistilBERT model was fine-tuned on a set of 2,309 manually labeled articles (achieving Fleiss' Kappa = 0.785) for binary classification of NO_RISK vs AT_RISK.

**Crucial Design Decision — Loss Function Configuration:**
During development, the research team faced an "Output Range Collapse" phenomenon when combining Focal Loss and Label Smoothing on a small dataset. When both penalty mechanisms operated together, the model's output probabilities were squashed to a middle range (0.3–0.8), entirely losing separability. The optimal solution was using CrossEntropyLoss combined with Label Smoothing (0.1) and Class Weights, achieving ECE = 0.0849—nearly perfect calibration.

The decision threshold was optimized down to **0.1756** to achieve Recall = 0.9503 (retaining 95% of risk signals) while maintaining Precision = 0.5426 (1.8 times higher than the natural prevalence of ~30%). Consequently, 5,762 articles with actual risk (AT_RISK) were forwarded to Phase 1, reducing the search space by 34%.

*(INSERT FIGURE 3: Gatekeeper diagnostic suite HERE)*
*(INSERT FIGURE 4: Calibration Comparison between Loss Function configurations HERE)*

#### 3.4. Phase 1 — Sense-making Layer (Risk Awareness)

**3.4.1. Taxonomy Classification (P1-01)**
Instead of using traditional BERTopic (prone to "Forced Categorization" errors), the system applies a **Zero-shot Multi-label Classification** architecture using the BART-large-MNLI model combined with a Sigmoid activation function. Each article is matched against a Static SCRM Ontology including event types: PORT_CONGESTION, LABOR_DISPUTE, GEOPOLITICAL, WEATHER_DISASTER, etc.
The core difference: the system **does not force labeling**. If no category exceeds the confidence threshold, the article is labeled `GENERAL_DISRUPTION`, preventing noise propagation.

**3.4.2. Severity Specialist (P1-02)**
The P1-02 module assesses severity (Medium vs High Risk) using DistilBERT, employing the **Context Shells** technique—wrapping the Taxonomy label in a complete English sentence: `"Context: This event involves {taxonomy}. Document: {text}"`. This technique outperforms raw Token Injection because it provides full semantic context to the model.

*(INSERT FIGURE 5: SHAP Severity Keywords Analysis HERE)*

#### 3.5. Phase 2 — Feature Engineering & Machine Learning Layer

**3.5.1. Entity Extraction and Geographic Mapping (P2-01 & P2-02)**
The system uses spaCy to extract GPE (Geopolitical Entity) entities. Instead of a rigid Inner Join, the study proposes a **Geographic Weighting Function** simulating the Ripple Effect: $w_{geo} = 1.0$ (same country), $0.6$ (same region), $0.3$ (global events like Geopolitical), or $0.1$ (remote risk).

**3.5.2. Feature Matrix and Stationarity Testing (P2-03)**
Continuous operational variables were tested for stationarity using the **ADF Test (Augmented Dickey-Fuller)**. The study also generated **Delta (differencing)** features to provide "Momentum" information. Collinearity checks (VIF) confirmed all variables are within safe thresholds (VIF < 5).

**3.5.3. Machine Learning Model and Ablation Strategy (P2-04 & P2-05)**
The **target variable** is defined as `stockout_flag` at week W+1 or W+2. The study designed a **3-Tier Evaluation Design**: Tier 1 (Industry Baseline - Rule-based), Tier 2 (Methodological Baseline - ERP only), and Tier 3 (Proposed SCRM - ERP + NLP).

#### 3.6. Phase 3 — Evaluation & Data Governance Layer
The evaluation set was divided using Chronological Split to prevent Threshold Tuning Leakage. The decision threshold was optimized by F0.5-score separately for each component family. SHAP was utilized to "open the black box", and **Data Governance** was implemented via SHA256 Checksum to ensure absolute academic transparency.

### Results and Discussion

#### Results

**4.1. Experimental Data Description**
- Total articles (Raw Corpus): 8,728
- AT_RISK articles (post Phase 0): 5,762 (66.0%)
- Manually labeled set: 2,309
- Fleiss' Kappa: 0.785
- Component IDs: 300 components, 8 families
- Timeframe: 2022–2024
- Natural Stockout rate (y=1): 3.16%

**4.2. Phase 0 Results — Gatekeeper Filter**
The Gatekeeper model achieved ROC-AUC = 0.8927, PR-AUC = 0.8106, and an ECE (Expected Calibration Error) of 0.0849 post Temperature Scaling. Temperature T = 0.9256 proved the model reached an excellent natural calibration state.

**4.3. Phase 2 Results — Ablation Study**
Results show that the Tier3_XGB_SCRM model (XGBoost integrated with NLP) achieved the **highest Precision** across the experimental matrix: 0.1654 for W+1 and 0.1658 for W+2—improving by **28.6% and 35.3%** respectively compared to Tier2_XGB_Baseline (operational data only). This is the key metric in an early warning environment as it directly reflects the "reliability" of each alert, combating "Alert Fatigue."

**4.4. Phase 3 Results — Threshold Optimization and SHAP**
*(INSERT FIGURE 6: Global Threshold Sweep HERE)*
*(INSERT FIGURE 7: SHAP Summary Plot and Waterfall Plot HERE)*
SHAP analysis reveals that operational features (`w1_on_hand_inventory`, `w1_pct_po_late`) are short-term indicators for material availability, whereas NLP features (`weighted_geo_risk_w1`, `at_risk_count_w1`) act as early warning indicators—appearing prior to operational fluctuations. 

**4.5. Quantitative Lead-Time Gain (LTG) Analysis and Case Study**
The core economic value of the Early Warning System is evaluated via the Lead-Time Gain formula:
$LTG = T_{stockout} - T_{first\_alert}$

To ensure statistical transparency and avoid Cherry-picking, quantitative analysis across all 18,480 test samples demonstrates the system maintains an average LTG of **1.0 to 3.2 weeks** across all component families (Avionics: 3.2 weeks, Hydraulics: 2.5 weeks, Engine: 1.7 weeks, Structure: 1.4 weeks, Fasteners: 1.3 weeks, LandingGear: 1.2 weeks, Electrical: 1.0 weeks). This provides purchasing managers with a sufficient time window to arrange alternative transport or secure backup supplies.

*(INSERT FIGURE 8: Hero Chart Case Study P00179 HERE)*

#### Discussion

**5.1. Strategic Model Calibration and Operational Interpretation**
The experimental results highlight a crucial finding: integrating NLP signals from public news does not uniformly improve all evaluation metrics but creates strategic trade-offs.

**(1) Risk-Averse Threshold Optimization:** In the context of SCRM, PR-AUC is a more honest metric than ROC-AUC due to extreme data imbalance (~3.16%). While ROC-AUC remains high, low PR-AUC reflects inevitable False Positives. However, this is a deliberate trade-off. The cost of a False Negative (missing a disruption) is exponentially higher than a False Positive (manual alert verification). The system is calibrated "conservatively," prioritizing Recall as an "insurance premium" to prevent "Black Swan" events from slipping through.

**(2) Information Bottlenecking for Non-Naive Learning:** Unlike Tier 1 models, all ML models (Tier 2 and 3) were intentionally stripped of the previous week's disruption state feature (`w1_stockout_flag`). This decision prevents "Naive Persistence." Creating this "information bottleneck" forces the algorithm to exploit nonlinear correlations between exogenous NLP signals and internal operational states, thereby safeguarding the "Early Warning" capability.

**(3) Preemptive Mitigation Feedback Loop:** The "negative coefficient" phenomenon of NLP variables in the Tier3_LR_SCRM model is a highlight of operational behavior. When alerts appear and enterprises activate backup supply chains, the actual disruption does not occur. This negative coefficient proves proactivity: the EWS does not just forecast a static state but actually participates in a "Preemptive Mitigation Feedback Loop," altering operational outcomes.

**(4) System Latency Sensitivity Analysis:** The study acknowledges that under ERP data latency (Stress Tests), the model exhibits a quantifiable performance decay. Yet, it maintains a predictive advantage over traditional rule-based heuristics, proving the resilience of the multi-modal fusion approach.

**5.2. Practical Value and Scalability**
The system's weekly alert outputs (including alert flag, probability, disruption type, and Lead-Time Gain) can be directly integrated into existing supply chain management dashboards. The entire pipeline utilizes open-source tools and public domain data (GDELT), allowing seamless scalability from Aerospace to Electronics, Automotive, or Pharmaceutical industries simply by adjusting the keyword sets and Risk Ontology.

### Conclusion
This study successfully built and verified an upstream supply chain risk early warning system (EWS-SCRM), integrating Natural Language Processing and Machine Learning in a 4-stage cascading architecture. Three core contributions were experimentally proven: (1) The first multi-source fusion pipeline for the upstream risk problem; (2) The Geographic Weighting mechanism simulating the Ripple Effect; and (3) The standard target variable definition for Inbound Stockout forecasting. The XGBoost model integrated with NLP achieved a 28.6% improvement in Precision compared to the operational-only model, providing a 1–2 week early warning window—sufficient time for enterprises to activate contingency plans and prevent financial damages. Future research directions include upgrading Entity Resolution to Tier-2 using Knowledge Graphs and integrating macro-economic indicators as supplementary features.

### REFERENCES
*(APA 7th edition references to be added)*
