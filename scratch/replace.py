import re

with open('0. project documents/SCRM_EWS_draft_article_v2.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix author list
old_authors = '''**Duc-Duong Dao Minh{a*}$, Buu-Tanh Tran-Leb$, Huyen-Huynh Chau Nhuc$, Thuy-Nguyen Nhutd$, Linh-Le Quynh Khanhe$**
{a,b,c,d,e}$ *University of Economics and Law, Ho Chi Minh City, Vietnam*
* Email address of Corresponding author: ducdmk24406@st.uel.edu.vn'''

new_authors = '''**Duc-Duong Dao Minh<sup>a*</sup>, Buu-Tanh Tran-Le<sup>a</sup>, Huyen-Huynh Chau Nhu<sup>a</sup>, Thuy-Nguyen Nhut<sup>a</sup>, Linh-Le Quynh Khanh<sup>a</sup>**
<sup>a</sup>*University of Economics and Law, Ho Chi Minh City, Vietnam*
* Email address of Corresponding author: ducdmk24406@st.uel.edu.vn'''
text = text.replace(old_authors, new_authors)

# Replace figures
text = text.replace('*(INSERT FIGURE 1: Research Methodology Framework HERE)*', '*(INSERT FIGURE 1: Research Methodology Framework HERE)*')
text = text.replace('*(INSERT FIGURE 2: Proposed System Architecture HERE)*', '*(INSERT FIGURE 2: Proposed System Architecture HERE)*')
text = text.replace('*(INSERT FIGURE 3: Gatekeeper diagnostic suite HERE)*', '**Figure 1.** Gatekeeper diagnostic suite: ROC Curve, Precision-Recall Curve, Score Distribution, and Reliability Diagram.\n\n![Figure 1. Gatekeeper diagnostic suite](../P0-04_Binary_Filter/output/p0_04_evaluation.png)')
text = text.replace('*(INSERT FIGURE 4: Calibration Comparison between Loss Function configurations HERE)*', '**Figure 2.** Calibration Comparison between Loss Function configurations—illustrating the Output Range Collapse phenomenon in Run 2.\n\n![Figure 2. Calibration Comparison](../P0-04_Binary_Filter/output/p0_04_calibration_comparison.png)')
text = text.replace('*(INSERT FIGURE 5: SHAP Severity Keywords Analysis HERE)*', '**Figure 3.** SHAP Severity Keywords Analysis—keywords pushing the AI to upgrade the alert to High Risk.\n\n![Figure 3. SHAP Severity Keywords](../P1-02_Severity_Specialist/shap_severity_keywords.png)')
text = text.replace('*(INSERT FIGURE 6: Global Threshold Sweep HERE)*', '**Figure 4.** Global Threshold Sweep—illustrating the trade-off between Precision and Recall across decision thresholds.\n\n![Figure 4. Global Threshold Sweep](../P3-01_Threshold/global_threshold_sweep.png)')
text = text.replace('*(INSERT FIGURE 7: SHAP Summary Plot and Waterfall Plot HERE)*', '**Figure 5.** SHAP Summary Plot—Overall contribution of each feature to the Stockout risk forecast.\n\n![Figure 5. SHAP Summary Plot](../P3-02_SHAP/shap_summary_plot.png)\n\n**Figure 6.** SHAP Waterfall Plot—Local Explanation for a specific data sample, allowing precise tracking of why the system issues an alert.\n\n![Figure 6. SHAP Waterfall Local](../P3-02_SHAP/shap_waterfall_local.png)')
text = text.replace('*(INSERT FIGURE 8: Hero Chart Case Study P00179 HERE)*', '**Figure 7.** Hero Chart—3-tier Case Study chart for component P00179 (Electrical family). Tier 1: Predicted Risk Score; Tier 2: Aggregated NLP Signal from news; Tier 3: Actual operational data (Inventory Level). The orange zone marks the "EWS Warning Period" prior to Stockout.\n\n![Figure 7. Hero Chart Case Study P00179](../P3-03_Integration/case_study_hero_chart.png)')

with open('0. project documents/SCRM_EWS_draft_article_v2.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Success')
