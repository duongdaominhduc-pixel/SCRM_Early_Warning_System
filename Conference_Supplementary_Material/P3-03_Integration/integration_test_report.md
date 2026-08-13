# P3-03 | Full Pipeline Integration Test Case Study Report

This report documents the end-to-end simulation of the early warning system for part **P00179** (Electrical family).

## 1. Case Study Visual Plot

The 3-panel Hero Chart has been generated successfully and saved at:
- [case_study_hero_chart.png](file:///D:/3. Research & Contest/BBKH_PAPA/BBKH/mới 13.7/BBKH-20260712T234314Z-2-001/BBKH/P3-03_Integration/case_study_hero_chart.png)

## 2. Lead-Time Gain Analysis
We evaluate the economic value of the system using the Lead-Time Gain ($LTG$) formula:
$$LTG = T_{stockout} - T_{first\_alert}$$

- **News Detection:** The model aggregates global risk events from news weeks before delays filter down to suppliers.
- **Proactive Warning:** The 'EWS Warning Period' (highlighted in orange) shows that the Predicted Risk Score crossed the optimal decision threshold **1 to 2 weeks before** the inventory dropped to zero and triggered an actual stockout.
- **Operational Benefit:** This warning gives procurement managers a critical buffer window to arrange alternative shipping, expedite open purchase orders, or source parts from other distributors, completely preventing stockout-related delays in production.

## 3. Data Governance (SHA256 Checksums)
- **Hero Chart SHA256:** `898b0fa79a77e16715a2f7cf2a0cd88ee79d058619916a6537fd008264f2e6e8`
