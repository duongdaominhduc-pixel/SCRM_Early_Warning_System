# SCRM Event Taxonomy Report (Q1)

This report outlines the static taxonomy used for Supply Chain Risk Management (SCRM) Event Extraction in Phase P1-01. The taxonomy is designed to overcome the limitations of standard NER models by using semantic matching (BERTopic + SentenceTransformers) against predefined risk categories.

## Taxonomy Overview
Version: 1.0

### 1. Port Congestion and Logistics Delay (`PORT_CONGESTION`)
- **Description:** Delays, bottlenecks, and congestion at maritime ports, shipping lanes, or logistics hubs. Includes container shortages, port strikes affecting operations, and customs hold-ups.
- **Keywords:** port, congestion, shipping, container, freight, vessel, logistics, delay, maritime, cargo

### 2. Geopolitical Conflict and Trade War (`GEOPOLITICAL`)
- **Description:** Disruptions caused by war, military conflict, international sanctions, trade wars, tariffs, export bans, or political instability.
- **Keywords:** war, sanction, tariff, geopolitical, conflict, military, ban, export, government, policy

### 3. Weather Disaster and Natural Catastrophe (`WEATHER_DISASTER`)
- **Description:** Supply chain interruptions due to extreme weather events, hurricanes, typhoons, floods, earthquakes, wildfires, or climate-related issues.
- **Keywords:** hurricane, flood, earthquake, weather, storm, wildfire, disaster, typhoon, climate, natural

### 4. Labor Dispute and Workforce Shortage (`LABOR_DISPUTE`)
- **Description:** Issues stemming from labor union strikes, worker protests, workforce shortages, or factory walkouts.
- **Keywords:** strike, labor, union, worker, protest, walkout, wage, shortage, employee, staff

### 5. Supplier Financial Insolvency (`SUPPLIER_FINANCIAL`)
- **Description:** Disruptions caused by a supplier's bankruptcy, financial distress, liquidation, or failure to secure funding.
- **Keywords:** bankruptcy, financial, insolvency, liquidation, debt, funding, distress, chapter 11, restructuring

### 6. Cybersecurity Attack and IT Outage (`CYBERSECURITY`)
- **Description:** Hacks, ransomware, data breaches, or IT system failures that paralyze supply chain operations or factory production.
- **Keywords:** cyber, ransomware, hack, breach, outage, system, software, attack, malware, it

### 7. ESG Violation and Compliance Risk (`ESG_VIOLATION`)
- **Description:** Supply chain halts due to environmental violations, forced labor allegations, regulatory compliance failures, or sustainability issues.
- **Keywords:** esg, compliance, forced labor, violation, environmental, regulation, sustainability, audit, human rights

### 8. General Operational Disruption (`GENERAL_DISRUPTION`)
- **Description:** Other operational supply chain disruptions such as factory fires, equipment breakdowns, or unclassified production halts.
- **Keywords:** fire, breakdown, halt, production, factory, operational, disruption, facility, suspend, accident

## Methodology
Instead of relying on fragile keyword matching or black-box LLMs, this taxonomy is used in a **Deterministic Mapping** approach:
1. News articles are clustered using `BERTopic` to find latent semantic groups.
2. The centroids of these clusters are compared against the embedding vectors of the categories above using **Cosine Similarity**.
3. Clusters are assigned the label of the closest taxonomy category, ensuring high interpretability and reproducibility.
