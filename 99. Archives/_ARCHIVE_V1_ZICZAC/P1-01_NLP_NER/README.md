# P1-01 | NLP Upgrade — NER & Event Extraction

## Overview
This folder contains the Phase 1 - Step 1 execution for the SCRM predictive modeling workflow. The primary goal of this phase is to replace legacy keyword matching with context-aware NLP to accurately extract supply chain risk events and entities from news articles.

## Methodology: Two-Tier Architecture

### Tier 1: Named Entity Recognition (NER)
- **Tool:** `spaCy` (using `en_core_web_trf` or `en_core_web_lg` transformer models)
- **Goal:** Extract foundational entities such as Organizations (ORG), Locations (GPE), and Dates (DATE).
- **Feature Created:** `entity_density_score` (Ratio of supply chain-relevant entities to total entities). 
- *Note:* The default `EVENT` entity in spaCy is largely ignored as it is biased toward historical/named events rather than supply chain disruptions.

### Tier 2: Event Extraction (Ontology-Anchored Discovery)
- **Goal:** Classify articles into specific supply chain disruption categories without relying on black-box LLMs, ensuring Accountability and Reproducibility.
- **Process:**
  1. **Semantic Discovery:** `BERTopic` and `SentenceTransformers` are used to embed and cluster 1,791 risk-related articles into semantic groups.
  2. **Ontology Knowledge Base:** A static, predefined SCRM risk taxonomy is established (`STATIC_SCRM_ONTOLOGY.json`).
  3. **Deterministic Mapping:** The centroid vectors of the discovered clusters are compared against the static ontology vectors using Cosine Similarity to assign the final risk label.

## Outputs
- **`pipeline_data/ner_features_5313.csv`:** The full 5,313 article corpus enriched with NER features.
- **`pipeline_data/event_labels_1791_ontology_mapped.csv`:** The 1,791 high-risk articles mapped to the static ontology.
- **`risk_taxonomy_report.md`:** The generated report detailing the taxonomy categories and descriptions used in Tier 2 mapping.
- **`STATIC_SCRM_ONTOLOGY.json`:** The static configuration file containing the SCRM risk categories and keywords.
