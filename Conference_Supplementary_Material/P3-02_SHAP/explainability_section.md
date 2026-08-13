# P3-02 | Explaining Model Predictions & Feature Importance

Model explainability results to be included in the scientific paper case study section.

## 1. Feature Importance Summary
- **Operational Baseline Features:** On-hand inventory (`w1_on_hand_inventory`) and percentage of late POs (`w1_pct_po_late`) are the primary short-term indicators for material availability.
- **NLP Risk Features:** The spatial-weighted geo risk sum (`weighted_geo_risk_w1`) and at-risk article count (`at_risk_count_w1`) act as powerful warning indicators that precede operational delays.
- **Delta Features:** `delta_avg_actual_lead_time_w1` successfully models the acceleration and momentum of lead-time delays inside the supply network.

## 2. Managerial Interpretation
When global supply chain risk scores rise in the news (Panel 2 of the Hero Chart), it increases the geographical risk score of the supplier. This warning allows decision-makers to build buffer stocks or prepare secondary sourcing strategies weeks before the actual stockout flag triggers.