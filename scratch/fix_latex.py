import re

file_path = r"d:\3. Research & Contest\BBKH_PAPA\BBKH\mới 13.7\BBKH-20260712T234314Z-2-001\BBKH\0. project documents\SCRM_EWS_draft_article_v2.tex"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace figure environments
content = content.replace(r"\begin{figure}", r"\begin{figure*}")
content = content.replace(r"\end{figure}", r"\end{figure*}")
content = content.replace(r"\begin{figure}[htbp]", r"\begin{figure*}[!t]")

# Replace table environments just in case
content = content.replace(r"\begin{table}", r"\begin{table*}")
content = content.replace(r"\end{table}", r"\end{table*}")

# Replace Title, Author, Abstract, Keywords
start_idx = content.find(r"\author{}")
intro_idx = content.find(r"\subsection{1. Introduction}")

if start_idx != -1 and intro_idx != -1:
    replacement = r"""\title{From Reactive to Proactive: An AI-Driven Early Warning System for Enhancing Supply Chain Resilience Through News-Operational Data Fusion}

\author{\IEEEauthorblockN{Duc-Duong Dao Minh\IEEEauthorrefmark{1}, Buu-Tanh Tran-Le, Huyen-Huynh Chau Nhu,\\Thuy-Nguyen Nhut, Linh-Le Quynh Khanh}
\IEEEauthorblockA{University of Economics and Law, Ho Chi Minh City, Vietnam\\
\IEEEauthorrefmark{1}Corresponding author. E-mail: ducdmk24406@st.uel.edu.vn}}
\date{}

\begin{document}

\maketitle

\begin{abstract}
Existing supply chain disruption forecasting approaches remain confined to a single data modality, leaving a critical blind-spot: no validated pipeline demonstrates whether fusing heterogeneous modalities yields measurable Incremental Predictive Validity over unimodal baselines. This study proposes a four-stage Cascading AI architecture that transforms raw logistics news into calibrated risk features via DistilBERT-based binary filtering and zero-shot multi-label classification, then fuses them with structured ERP data through a Geographic Weighting function before training gradient-boosted classifiers. Experiments on 8,728 logistics news articles (2022--2024) and five aerospace operational datasets yield three principal findings: (1) the Gatekeeper binary filter achieves ROC-AUC = 0.8927 and Recall = 0.9503; (2) the fused XGBoost model attains Precision = 0.1654 on minority-class stockout prediction --- a 28.7\% relative improvement over the ERP-only baseline, substantiating Incremental Predictive Validity; and (3) the system provides a Lead-Time Gain of 1.0 to 3.2 weeks across all component families prior to disruption onset. These results validate that integrating public-domain textual signals with operational telemetry produces an actionable early warning capability for upstream inventory risk.
\end{abstract}

\begin{IEEEkeywords}
Supply Chain Risk Management, Natural Language Processing, Heterogeneous Data Fusion, Early Warning System, Inventory Disruption Forecasting
\end{IEEEkeywords}

"""
    content = content[:start_idx] + replacement + content[intro_idx:]

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
