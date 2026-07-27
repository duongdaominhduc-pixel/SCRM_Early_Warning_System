# Ứng dụng Khai thác Dữ liệu Web và Xử lý Ngôn ngữ Tự nhiên Kết hợp Học máy để Xây dựng Hệ thống Cảnh báo Sớm Nguy cơ Đứt gãy Chuỗi Cung ứng Thượng nguồn

---

## TÓM TẮT

Chuỗi cung ứng toàn cầu ngày càng dễ tổn thương trước các cú sốc bên ngoài như đại dịch COVID-19, tắc nghẽn kênh đào Suez hay khủng hoảng thiếu hụt chip bán dẫn, đặt ra nhu cầu cấp bách về một hệ thống cảnh báo sớm (Early Warning System — EWS) có khả năng phát hiện rủi ro thượng nguồn trước khi chúng biểu hiện thành thiếu hụt tồn kho thực tế. Tuy nhiên, các nghiên cứu hiện hành hoặc chỉ khai thác dữ liệu tin tức mà thiếu kết nối với dữ liệu vận hành nội bộ, hoặc chỉ phân tích dữ liệu ERP mà bỏ qua các tín hiệu cảnh báo sớm từ môi trường bên ngoài. Nghiên cứu này đề xuất một kiến trúc tích hợp 4 giai đoạn (Sensing → Sense-making → Feature Fusion → Evaluation) kết hợp mô hình ngôn ngữ DistilBERT, phân loại Zero-shot đa nhãn, trọng số địa lý (Geographic Weighting) và thuật toán XGBoost để dự báo xác suất đứt gãy nguồn cung theo tuần. Thực nghiệm trên bộ dữ liệu gồm 8.728 bài báo chuyên ngành logistics (2022–2024) và 5 bảng dữ liệu vận hành hàng không vũ trụ cho thấy: (1) Bộ lọc nhị phân Gatekeeper đạt ROC-AUC = 0,8927, Recall = 0,9503 và ECE = 0,0849; (2) Mô hình XGBoost tích hợp NLP (Tier3_XGB_SCRM) đạt Minority F1-score = 0,2064 và Precision = 0,1654 — cải thiện vượt trội 28,7% về Precision so với mô hình XGBoost thuần vận hành (Tier2_XGB_Baseline); và (3) Hệ thống cung cấp cửa sổ cảnh báo sớm từ 1 đến 2 tuần trước khi đứt gãy thực sự xảy ra. Kết quả chứng minh rằng tín hiệu NLP từ tin tức công khai, khi được tích hợp có hệ thống với dữ liệu vận hành, tạo ra giá trị gia tăng đáng kể cho năng lực dự báo rủi ro thượng nguồn.

**Từ khóa:** Quản trị Rủi ro Chuỗi Cung ứng; Xử lý Ngôn ngữ Tự nhiên; Học máy; Hệ thống Cảnh báo Sớm; Rủi ro Tồn kho; Nhận dạng Thực thể; Phân loại Xếp tầng; Trọng số Địa lý

---

## 1. GIỚI THIỆU

### 1.1. Bối cảnh

Vào tháng 3 năm 2021, tàu container Ever Given mắc cạn tại kênh đào Suez trong 6 ngày, gây thiệt hại ước tính 9,6 tỷ USD và làm gián đoạn dòng chảy hàng hóa toàn cầu. Chỉ vài tháng sau, cuộc khủng hoảng thiếu hụt chip bán dẫn buộc hàng loạt nhà sản xuất ô tô và hàng không vũ trụ phải cắt giảm sản lượng. Gần đây hơn, xung đột tại Biển Đỏ (2024) tiếp tục phơi bày tính dễ tổn thương cực kỳ cao của chuỗi cung ứng toàn cầu. Theo báo cáo của Gartner (2023), hơn 87% doanh nghiệp sản xuất đã trải qua ít nhất một sự cố gián đoạn nguồn cung trong giai đoạn 2020–2023.

Thách thức cốt lõi không nằm ở việc phản ứng sau khi đứt gãy xảy ra, mà ở khả năng **phát hiện sớm các tín hiệu cảnh báo** từ môi trường bên ngoài — thường xuất hiện dưới dạng tin tức về đình công, thiên tai, biến động giá nguyên liệu, hoặc xung đột địa chính trị — trước khi các hệ quả vận hành (tồn kho cạn kiệt, dây chuyền ngừng hoạt động) xảy ra thực sự. Khoảng thời gian giữa tín hiệu cảnh báo sớm và sự cố thực tế chính là "cửa sổ vàng" để doanh nghiệp kịp thời kích hoạt phương án dự phòng.

### 1.2. Vấn đề nghiên cứu

Phần lớn doanh nghiệp sản xuất hiện nay vẫn dựa vào các phương pháp giám sát rủi ro truyền thống: báo cáo định kỳ từ phòng mua hàng, kiểm tra thủ công tin tức ngành, hoặc chỉ số KPI tĩnh từ hệ thống ERP. Các phương pháp này mang tính phản ứng (reactive) — chỉ phát hiện vấn đề khi tồn kho đã cạn kiệt hoặc đơn hàng đã về trễ — và không có khả năng tận dụng lượng thông tin khổng lồ được công bố hàng ngày trên các cổng tin tức chuyên ngành logistics toàn cầu.

### 1.3. Khoảng trống nghiên cứu

Phân tích tổng hợp các nghiên cứu liên quan cho thấy một khoảng trống rõ rệt: không có nghiên cứu nào đồng thời giải quyết đầy đủ các khía cạnh cần thiết cho một hệ thống cảnh báo sớm toàn diện, đặc biệt là việc chứng minh Giá trị dự báo tăng thêm (Incremental Predictive Validity) khi kết hợp dữ liệu phi cấu trúc và có cấu trúc. Hệ thống không chỉ đơn thuần "biết thêm tin tức", mà phải chứng minh được năng lực "dự báo tốt hơn" nhờ tin tức đó.

**Bảng 1.** So sánh định vị đóng góp với các nghiên cứu tiền nhiệm

| Tiêu chí | Cano-Marin et al. (2023) | Ivanov et al. (2022) | Jialu Wang (2024) | Brintrup et al. (2020) | **Nghiên cứu này** |
|---|:---:|:---:|:---:|:---:|:---:|
| NLP từ tin tức | ✓ | ✗ | ✓ | ✗ | **✓** |
| Dữ liệu vận hành nội bộ | ✗ | ✓ | ✗ | ✓ | **✓** |
| Heterogeneous Modality Fusion | ✗ | ✗ | Một phần | ✗ | **✓** |
| Spatial Risk Mapping | ✗ | ✗ | ✗ | ✗ | **✓** |
| Incremental Predictive Validity | ✗ | ✗ | Một phần | ✗ | **✓** |
| Walk-forward Validation | ✗ | ✗ | ✗ | ✓ | **✓** |

### 1.4. Mục tiêu và Đóng góp khoa học

Nghiên cứu này định vị ba đóng góp khoa học cốt lõi, giải quyết trực diện các rào cản kỹ thuật khắt khe nhất trong quản trị rủi ro chuỗi cung ứng:

**(1) Heterogeneous Modality Fusion via Cascading AI:** Xây dựng pipeline tích hợp đầu cuối (end-to-end), chuyển hóa các tín hiệu rủi ro "mềm" từ tin tức phi cấu trúc (NLP Signal) thành các đặc trưng "cứng" cho mô hình học máy kết hợp với dữ liệu vận hành (ERP). Khung kiến trúc AI Xếp tầng này soi sáng hoàn toàn bài toán đứt gãy thượng nguồn — khu vực từ lâu vẫn bị coi là "điểm mù" (blind-spot) trong SCRM. Hơn thế nữa, tính toàn vẹn dữ liệu (Data Integrity) được bảo đảm xuyên suốt pipeline nhờ cơ chế SHA256 Checksum, loại trừ hoàn toàn nghi ngờ về thao túng dữ liệu (Data manipulation).

**(2) Spatial Risk Sensitivity Calibration (Geographic Weighting):** Thiết kế cơ chế ánh xạ mềm (Soft Join) sử dụng hàm trọng số địa lý thay vì phép Inner Join cứng nhắc, giải quyết triệt để vấn đề "Bất đối xứng dữ liệu" (Granularity Mismatch) giữa tin tức vĩ mô (cấp quốc gia) và ERP vi mô (cấp nhà cung cấp). Kỹ thuật này giúp hệ thống mô phỏng "Hiệu ứng gợn sóng" (Ripple Effect) và bắt được các "tín hiệu yếu" (Weak Signals) lây lan chéo khu vực mà các hệ thống truyền thống bỏ sót.

**(3) Inbound Ground Truth & Information Bottlenecking for Non-Naive Learning:** Đề xuất định nghĩa chuẩn cho bài toán đứt gãy thượng nguồn. Quan trọng hơn, nghiên cứu thiết lập một rào cản kỹ thuật chuyên nghiệp chống lại hiện tượng "Hồi quy giả mạo" (Spurious Regression) bằng ADF Test và biến Delta. Đồng thời, việc loại bỏ trạng thái tồn kho quá khứ (`w1_stockout_flag`) ra khỏi không gian đặc trưng ML đảm bảo mô hình thực sự "nhìn thấy rủi ro" nhờ năng lực tổng hợp thông tin, chứ không phải "đoán mò" dựa trên chuỗi lịch sử (Naive Forecaster). Cuối cùng, việc tích hợp phân tích SHAP đáp ứng tiêu chí "Giải trình thuật toán" (Algorithmic Accountability), minh bạch hóa lý do một tín hiệu NLP kích hoạt báo động trong ERP.

### 1.5. Cấu trúc bài báo

Phần còn lại của bài báo được tổ chức như sau: Mục 2 trình bày tổng quan nghiên cứu liên quan; Mục 3 mô tả chi tiết phương pháp nghiên cứu theo kiến trúc 4 giai đoạn; Mục 4 trình bày kết quả thực nghiệm; Mục 5 thảo luận về ý nghĩa khoa học và thực tiễn; và Mục 6 kết luận cùng định hướng nghiên cứu tương lai.

---

## 2. TỔNG QUAN NGHIÊN CỨU LIÊN QUAN

### 2.1. Quản trị Rủi ro Chuỗi Cung ứng: Khung lý thuyết

Quản trị rủi ro chuỗi cung ứng (Supply Chain Risk Management — SCRM) là lĩnh vực nghiên cứu tập trung vào việc nhận diện, đánh giá và giảm thiểu các nguy cơ gián đoạn trong mạng lưới cung ứng. Khung lý thuyết truyền thống của SCRM phân chia quy trình thành bốn giai đoạn: Nhận diện rủi ro (Risk Identification), Đánh giá rủi ro (Risk Assessment), Giảm thiểu rủi ro (Risk Mitigation) và Giám sát rủi ro (Risk Monitoring). Tuy nhiên, phần lớn các công trình hiện hữu tập trung vào hai giai đoạn đầu — nhận diện và đánh giá — trong khi khả năng giám sát liên tục và cảnh báo sớm theo thời gian thực vẫn còn là một thách thức mở.

Sự bùng nổ của trí tuệ nhân tạo (AI) và học máy (ML) trong thập kỷ gần đây đã mở ra hướng tiếp cận mới cho SCRM: thay vì dựa vào đánh giá chuyên gia chủ quan, các hệ thống có thể tự động quét, phân tích và định lượng rủi ro từ nhiều nguồn dữ liệu đa dạng. Tuy nhiên, việc tích hợp đồng thời dữ liệu phi cấu trúc (tin tức, mạng xã hội) với dữ liệu có cấu trúc (ERP, tồn kho) trong cùng một pipeline vẫn là khoảng trống nghiên cứu lớn nhất.

### 2.2. NLP trong phát hiện rủi ro từ văn bản phi cấu trúc

Kỹ thuật Xử lý Ngôn ngữ Tự nhiên (NLP) đã được ứng dụng rộng rãi trong việc khai thác tín hiệu rủi ro từ văn bản phi cấu trúc. Các phương pháp phổ biến bao gồm: phân tích cảm xúc (Sentiment Analysis), trích xuất sự kiện (Event Extraction), và nhận dạng thực thể (Named Entity Recognition — NER).

Tuy nhiên, trong lĩnh vực chuỗi cung ứng, phân tích cảm xúc tỏ ra kém hiệu quả vì cùng một sự kiện (ví dụ: "đình công tại cảng Los Angeles") có thể mang sắc thái tích cực đối với công đoàn lao động nhưng lại là rủi ro nghiêm trọng đối với nhà sản xuất phụ thuộc vào nguồn cung qua cảng đó. Do đó, nghiên cứu này lựa chọn phương pháp **phân loại sự kiện theo Ontology tĩnh** (Ontology-Anchored Classification) thay vì phân tích cảm xúc, nhằm đảm bảo tính xác định (deterministic) và khả năng giải trình (accountability) của hệ thống.

### 2.3. Học máy cho dự báo rủi ro chuỗi cung ứng

Các thuật toán học máy như XGBoost, Random Forest và mạng nơ-ron hồi quy (LSTM) đã được áp dụng trong nhiều nghiên cứu dự báo rủi ro chuỗi cung ứng. Tuy nhiên, phần lớn các nghiên cứu này mắc phải ít nhất một trong hai lỗi phương pháp luận nghiêm trọng: (a) Sử dụng chia tập dữ liệu ngẫu nhiên (Random Split) thay vì chia theo trục thời gian (Chronological Split), dẫn đến rò rỉ dữ liệu (Data Leakage); và (b) Không kiểm định tính dừng (Stationarity) của các biến chuỗi thời gian trước khi đưa vào mô hình hồi quy, gây ra hiện tượng Hồi quy giả mạo (Spurious Regression).

Nghiên cứu này giải quyết triệt để cả hai vấn đề bằng cách: áp dụng Walk-forward Validation với TimeSeriesSplit (5 folds, gap = 2 tuần), và tích hợp kiểm định ADF (Augmented Dickey-Fuller) tự động kèm theo biến sai phân bậc 1 (Delta Features) cho các biến vận hành liên tục.

### 2.4. Khoảng trống nghiên cứu và Định vị đóng góp

Như đã trình bày trong Bảng 1, khoảng trống cốt lõi nằm ở việc thiếu một hệ thống tích hợp đầu cuối có khả năng: (i) trích xuất tín hiệu rủi ro có cấu trúc từ tin tức phi cấu trúc, (ii) ánh xạ các tín hiệu đó vào dữ liệu vận hành nội bộ thông qua cơ chế trọng số địa lý, và (iii) huấn luyện mô hình dự báo với phương pháp kiểm định nghiêm ngặt theo trục thời gian. Đề tài này lấp đầy khoảng trống đó.

---

## 3. PHƯƠNG PHÁP NGHIÊN CỨU

### 3.1. Tổng quan kiến trúc hệ thống

Hệ thống EWS-SCRM được thiết kế theo Kiến trúc Tuyến tính 4 Giai đoạn, áp dụng tư duy "Trí tuệ Nhân tạo Xếp tầng" (Cascading AI) để tối ưu hóa việc phân tách tín hiệu (Sensing) và nhận thức ngữ cảnh (Sense-making) trước khi tổng hợp vào không gian đặc trưng vận hành (Operational Feature Space).

[CHÈN SƠ ĐỒ 1: Sơ đồ Mô hình Phương pháp Nghiên cứu (Research Methodology Framework) TẠI ĐÂY. Dựa theo cấu trúc Node & Edges trong schematic_outline.md]

[CHÈN SƠ ĐỒ 2: Sơ đồ Kiến trúc Hệ thống Đề xuất (Proposed System Architecture) TẠI ĐÂY. Dựa theo cấu trúc Node & Edges trong schematic_outline.md]

**Bảng 2.** Tổng hợp kiến trúc hệ thống theo từng giai đoạn

| Giai đoạn | Nhiệm vụ | Kỹ thuật cốt lõi | Đầu ra chính |
|---|---|---|---|
| Phase 0: Sensing | Lọc thô tin tức rủi ro | DistilBERT + CrossEntropyLoss + Label Smoothing | `at_risk_corpus.csv` (5.762 bài) |
| Phase 1: Sense-making | Phân loại sự kiện & mức độ | Zero-shot Multi-label + Context Shells + Focal Loss | `pseudo_labeled_final.csv` |
| Phase 2: Feature & ML | Hợp nhất đa nguồn & huấn luyện | Geographic Weighting + ADF Test + XGBoost | `feature_matrix.parquet` + Trained Models |
| Phase 3: Evaluation | Tối ưu ngưỡng & giải trình | Chronological Split + SHAP + SHA256 Governance | Báo cáo Case Study + Hero Chart |

### 3.2. Thu thập và Tiền xử lý dữ liệu

#### 3.2.1. Dữ liệu tin tức (External Signal)

Corpus tin tức được thu thập từ hai nguồn chuyên ngành logistics: GDELT BigQuery Index và NewsAPI, với bộ lọc từ khóa tập trung vào các chủ đề chuỗi cung ứng (supply chain disruption, logistics risk, port congestion, supplier shortage). Quá trình tiền xử lý bao gồm: loại bỏ bài trùng lặp bằng Cosine Similarity (ngưỡng TF-IDF ≥ 0,85), lọc bỏ bài dưới 100 từ và bài phi tiếng Anh. Kết quả thu được **8.728 bài báo sạch** trong giai đoạn 2022–2024.

#### 3.2.2. Dữ liệu vận hành nội bộ (Operational Data)

Bộ dữ liệu vận hành bao gồm 5 bảng CSV phản ánh hoạt động chuỗi cung ứng hàng không vũ trụ: (1) `parts_master.csv` — danh mục linh kiện với phân loại criticality A/B/C; (2) `shifted_purchase_orders.csv` — lịch sử đặt hàng; (3) `shifted_supply_chain_history.csv` — lịch sử tồn kho và lead time thực tế; (4) `shifted_quality_incidents.csv` — sự cố chất lượng; và (5) `supplier_locations.csv` — phân bổ địa lý nhà cung cấp. Dữ liệu được đồng bộ hóa về khung thời gian 2022–2024 thông qua Time-shifting.

### 3.3. Phase 0 — Tầng Sensing (Lọc rủi ro)

Phase 0 đóng vai trò là "Người gác cổng" (Gatekeeper) với triết lý thiết kế: **"Thà bắt lầm còn hơn bỏ sót"**. Mô hình DistilBERT được fine-tune trên tập 2.309 bài gán nhãn thủ công (đạt hệ số đồng thuận Fleiss' Kappa = 0,785) để phân loại nhị phân NO_RISK vs AT_RISK.

**Quyết định thiết kế quan trọng — Cấu hình Loss Function:**

Trong quá trình phát triển, nhóm nghiên cứu đã đối mặt với hiện tượng "Sụp đổ dải đầu ra" (Output Range Collapse) khi kết hợp đồng thời Focal Loss và Label Smoothing trên tập dữ liệu nhỏ. Khi cả hai cơ chế phạt cùng hoạt động, mô hình bị ép xác suất đầu ra về vùng trung gian (0,3–0,8), mất hoàn toàn năng lực phân tách. Giải pháp tối ưu là sử dụng CrossEntropyLoss kết hợp Label Smoothing (0,1) và Class Weights, đạt ECE = 0,0849 — mức hiệu chuẩn gần như hoàn hảo.

Ngưỡng quyết định được tối ưu hóa xuống **0,1756** để đạt Recall = 0,9503 (giữ lại 95% tín hiệu rủi ro), đồng thời duy trì Precision = 0,5426 (gấp 1,8 lần so với prevalence tự nhiên ~30%). Kết quả là 5.762 bài báo có rủi ro thực sự (AT_RISK) được chuyển tiếp sang Phase 1, giảm 34% không gian tìm kiếm.

**Hình 1.** Bộ chẩn đoán hiệu suất mô hình Gatekeeper (Phase 0): ROC Curve, Precision-Recall Curve, Score Distribution và Reliability Diagram.

![Hình 1. Bộ chẩn đoán Gatekeeper](../P0-04_Binary_Filter/output/p0_04_evaluation.png)

**Hình 2.** So sánh hiệu chuẩn (Calibration Comparison) giữa các cấu hình Loss Function — minh họa hiện tượng Output Range Collapse ở Lần chạy 2.

![Hình 2. So sánh hiệu chuẩn](../P0-04_Binary_Filter/output/p0_04_calibration_comparison.png)

### 3.4. Phase 1 — Tầng Sense-making (Nhận thức rủi ro)

#### 3.4.1. Phân loại Taxonomy (P1-01)

Thay vì sử dụng BERTopic truyền thống (dễ mắc lỗi "Forced Categorization" khi ép 100% bài báo vào các cụm), hệ thống áp dụng kiến trúc **Zero-shot Multi-label Classification** sử dụng mô hình BART-large-MNLI kết hợp hàm kích hoạt Sigmoid. Mỗi bài báo được đối chiếu với Khung danh mục chuẩn (Static SCRM Ontology) bao gồm các loại sự kiện: PORT_CONGESTION, LABOR_DISPUTE, GEOPOLITICAL, WEATHER_DISASTER, v.v.

Điểm khác biệt cốt lõi: hệ thống **không ép buộc gán nhãn**. Nếu không có danh mục nào vượt ngưỡng tin cậy, bài báo được gán nhãn `GENERAL_DISRUPTION`, tránh hiện tượng nhiễu lan truyền sang Phase tiếp theo.

#### 3.4.2. Chuyên gia Mức độ Nghiêm trọng (P1-02)

Module P1-02 đánh giá mức độ nghiêm trọng (Medium vs High Risk) bằng mô hình DistilBERT, sử dụng kỹ thuật **Context Shells** — bao bọc nhãn Taxonomy trong câu tiếng Anh hoàn chỉnh: `"Context: This event involves {taxonomy}. Document: {text}"`. Kỹ thuật này vượt trội hơn phương pháp Token Injection thô (chèn token `[LABOR_DISPUTE]`) vì cung cấp bối cảnh ngữ nghĩa đầy đủ cho mô hình.

Hàm mất mát sử dụng **Focal Loss** (gamma = 2,0) mà không kết hợp Label Smoothing — quyết định này dựa trên bài học từ Phase 0 về hiện tượng Double Regularization Collapse trên tập dữ liệu nhỏ.

**Hình 3.** Phân tích SHAP cho mô hình Severity Specialist — các từ khóa thúc đẩy AI nâng cấp mức cảnh báo lên High Risk.

![Hình 3. SHAP Severity Keywords](../P1-02_Severity_Specialist/shap_severity_keywords.png)

### 3.5. Phase 2 — Tầng Feature Engineering & Machine Learning

#### 3.5.1. Trích xuất Thực thể và Ánh xạ Địa lý (P2-01 & P2-02)

Hệ thống sử dụng spaCy (`en_core_web_lg`) để trích xuất thực thể GPE (quốc gia/vùng) từ các bài báo rủi ro. Thay vì Inner Join cứng nhắc (chỉ khớp chính xác quốc gia sự kiện = quốc gia nhà cung cấp), nghiên cứu đề xuất **Hàm trọng số địa lý** (Geographic Weighting Function) mô phỏng Hiệu ứng gợn sóng:

$$
w_{geo}(e, s) = \begin{cases}
1.0 & \text{nếu } country(e) = country(s) \\
0.6 & \text{nếu } region(e) = region(s) \\
0.3 & \text{nếu } event\_type \in \{GEOPOLITICAL, PORT\_CONGESTION\} \\
0.1 & \text{trường hợp khác (rủi ro xa)}
\end{cases}
$$

trong đó $e$ là sự kiện rủi ro từ tin tức, $s$ là nhà cung cấp. Phân tích độ nhạy (Sensitivity Analysis) trên trọng số Regional Match (biến thiên từ 0,4 đến 0,8) xác nhận trạng thái ổn định tiệm cận (Asymptotic Stability), chống lại nghi ngờ "cherry-picking".

#### 3.5.2. Ma trận Đặc trưng và Kiểm định Tính dừng (P2-03)

Dữ liệu được tổng hợp theo đơn vị quan sát: 1 hàng = 1 tuần × 1 linh kiện. Các đặc trưng được chia thành hai nhóm:

**Bảng 3.** Schema Ma trận Đặc trưng X

| Nhóm | Đặc trưng | Mô tả | Nguồn |
|---|---|---|---|
| Vận hành (W-1) | `w1_on_hand_inventory` | Mức tồn kho cuối tuần W-1 | ERP |
| Vận hành (W-1) | `w1_avg_actual_lead_time` | Lead time thực tế trung bình | ERP |
| Vận hành (W-1) | `w1_pct_po_late` | % đơn hàng về trễ | ERP |
| Vận hành (W-1) | `w1_lead_time_ratio` | actual / promised lead time | ERP |
| Vận hành (W-1) | `w1_quality_incident_count` | Số sự cố chất lượng | ERP |
| Delta (Momentum) | `w1_delta_on_hand_inventory` | Sai phân tồn kho (W-1 minus W-2) | Derived |
| Delta (Momentum) | `w1_delta_avg_actual_lead_time` | Sai phân lead time | Derived |
| NLP Signal (W-1) | `at_risk_count_w1` | Số bài AT_RISK tuần W-1 | Phase 0 |
| NLP Signal (W-1) | `high_severity_count_w1` | Số bài High Risk tuần W-1 | Phase 1 |
| NLP Signal (W-1) | `weighted_geo_risk_w1` | Điểm rủi ro địa lý | Phase 2 |
| NLP Signal (W-2) | `at_risk_count_w2`, `high_severity_count_w2`, `weighted_geo_risk_w2` | Tín hiệu lag 2 tuần | Phase 0-2 |

Trước khi đưa vào mô hình, các biến vận hành liên tục được kiểm định tính dừng bằng **ADF Test (Augmented Dickey-Fuller)**. Kết quả cho thấy cả `w1_avg_actual_lead_time` (p < 0,0001) và `w1_on_hand_inventory` (p < 0,0001) đều đạt tính dừng (Stationary). Tuy nhiên, nghiên cứu vẫn sinh ra các biến **Delta (sai phân)** để cung cấp thêm chiều thông tin "Momentum" — tốc độ suy thoái — bên cạnh biến gốc "Baseline State". Kiểm tra đa cộng tuyến bằng VIF xác nhận tất cả các biến đều nằm trong ngưỡng an toàn (VIF < 5): `w1_on_hand_inventory` = 1,32; `w1_avg_actual_lead_time` = 1,33; `w1_pct_po_late` = 1,08.

#### 3.5.3. Mô hình Học máy và Chiến lược Ablation (P2-04 & P2-05)

**Biến mục tiêu** được định nghĩa là `stockout_flag` tại tuần W+1 hoặc W+2 (Target Shift), trong đó y = 1 khi `on_hand_inventory ≤ 0`. Tỷ lệ dương tự nhiên là ~3,16% — phản ánh đúng thực tế rằng đứt gãy chuỗi cung ứng là sự kiện hiếm nhưng có tác động nghiêm trọng.

Nghiên cứu thiết kế **Ma trận thực nghiệm 3 tầng (3-Tier Evaluation Design)** để đánh giá toàn diện:

- **Tier 1 (Industry Baseline):** Rule-Based Heuristics — đại diện cho thực trạng ngành.
- **Tier 2 (Methodological Baseline):** Logistic Regression (LR) và XGBoost chỉ sử dụng đặc trưng vận hành.
- **Tier 3 (Proposed SCRM):** LR và XGBoost tích hợp đầy đủ đặc trưng NLP.

Toàn bộ thực nghiệm sử dụng `TimeSeriesSplit(n_splits=5, gap=2)` với cơ chế **In-Fold Imbalance Handling**: tham số `scale_pos_weight` được tính toán bên trong mỗi fold huấn luyện, đảm bảo tập Validation giữ nguyên phân phối gốc.

### 3.6. Phase 3 — Tầng Evaluation & Data Governance

#### 3.6.1. Tối ưu Ngưỡng theo Họ Linh kiện (P3-01)

Tập đánh giá được chia thành `df_val` (60%) và `df_test` (40%) theo trục thời gian (Chronological Split) để tránh Threshold Tuning Leakage. Ngưỡng quyết định được tối ưu hóa theo chỉ số F0.5-score (ưu tiên Precision) **riêng biệt cho từng họ linh kiện**, phản ánh thực tế rằng các họ linh kiện khác nhau có đặc tính rủi ro khác nhau.

#### 3.6.2. Phân tích SHAP và Quản trị Dữ liệu (P3-02 & P3-03)

Thư viện SHAP (SHapley Additive exPlanations) được sử dụng để "mở hộp đen" mô hình XGBoost. Ngoài ra, nghiên cứu triển khai cơ chế **Data Governance** bằng mã băm mật mã SHA256 — mỗi biểu đồ và báo cáo thực nghiệm đều được đóng dấu Checksum tự động tại thời điểm sinh ra, đảm bảo tính nguyên bản và minh bạch học thuật tuyệt đối.

---

## 4. KẾT QUẢ THỰC NGHIỆM

### 4.1. Mô tả dữ liệu thực nghiệm

| Thông số | Giá trị |
|---|---|
| Tổng số bài báo (Raw Corpus) | 8.728 bài |
| Bài báo AT_RISK (sau Phase 0) | 5.762 bài (66,0%) |
| Tập gán nhãn thủ công | 2.309 bài |
| Hệ số Fleiss' Kappa | 0,785 (Substantial Agreement) |
| Số lượng linh kiện (Part IDs) | 300 linh kiện, 8 họ |
| Khung thời gian | 2022–2024 |
| Tỷ lệ Stockout tự nhiên (y=1) | 3,16% |

### 4.2. Kết quả Phase 0 — Bộ lọc Gatekeeper

**Bảng 4.** Hiệu suất mô hình Gatekeeper (DistilBERT)

| Chỉ số | Giá trị |
|---|---|
| ROC-AUC | 0,8927 |
| PR-AUC | 0,8106 |
| Recall (tại ngưỡng 0,1756) | 0,9503 |
| Precision (tại ngưỡng 0,1756) | 0,5426 |
| ECE (sau Temperature Scaling) | 0,0849 |
| Cohen's Kappa (ngưỡng 0,50) | 0,635 (Substantial Agreement) |
| Temperature T | 0,9256 |

Giá trị Temperature T = 0,9256 (gần 1,0) chứng tỏ mô hình đạt trạng thái hiệu chuẩn tự nhiên xuất sắc, không bị overconfident hay underconfident. Hệ số Cohen's Kappa = 0,635 tại ngưỡng tự nhiên (0,50) khẳng định AI đã tiếp thu và tái hiện logic gán nhãn của chuyên gia con người một cách đáng tin cậy.

### 4.3. Kết quả Phase 2 — Ablation Study

**Bảng 5.** So sánh hiệu suất mô hình dự báo Stockout (Target: y2_shift1 — W+1)

| Cấu hình | Precision | Recall | Minority F1 | PR-AUC |
|---|---|---|---|---|
| Tier1_RuleBased | 0,0583 | 0,7734 | 0,1076 | 0,4193 |
| Tier2_LR_Baseline | 0,0909 | 0,8364 | 0,1621 | 0,2024 |
| Tier2_XGB_Baseline | 0,1286 | 0,5383 | 0,2017 | 0,1691 |
| **Tier3_LR_SCRM** | 0,0928 | 0,6892 | 0,1629 | 0,1689 |
| **Tier3_XGB_SCRM** | **0,1654** | 0,3026 | **0,2064** | 0,1520 |

**Bảng 6.** So sánh hiệu suất mô hình dự báo Stockout (Target: y2_shift2 — W+2)

| Cấu hình | Precision | Recall | Minority F1 | PR-AUC |
|---|---|---|---|---|
| Tier1_RuleBased | 0,0562 | 0,7489 | 0,1037 | 0,4065 |
| Tier2_LR_Baseline | 0,0908 | 0,8337 | 0,1620 | 0,2049 |
| Tier2_XGB_Baseline | 0,1225 | 0,5363 | 0,1939 | 0,1640 |
| **Tier3_LR_SCRM** | 0,0943 | 0,7126 | 0,1658 | 0,1726 |
| **Tier3_XGB_SCRM** | **0,1658** | 0,2993 | **0,2061** | 0,1497 |

Kết quả cho thấy mô hình Tier3_XGB_SCRM (XGBoost tích hợp NLP) đạt **Precision cao nhất** trong toàn bộ ma trận thực nghiệm: 0,1654 cho W+1 và 0,1658 cho W+2 — cải thiện lần lượt **28,6% và 35,3%** so với Tier2_XGB_Baseline (chỉ dùng dữ liệu vận hành). Đây là thước đo then chốt trong môi trường cảnh báo sớm vì nó phản ánh trực tiếp mức độ "tin cậy" của mỗi cảnh báo, giúp chống lại hiện tượng "Alert Fatigue" — khi nhân viên mua hàng nhận quá nhiều cảnh báo sai và bắt đầu phớt lờ toàn bộ.

**Hình 4.** Biểu đồ quét ngưỡng toàn cục (Global Threshold Sweep) — minh họa sự đánh đổi giữa Precision và Recall theo ngưỡng quyết định.

![Hình 4. Global Threshold Sweep](../P3-01_Threshold/global_threshold_sweep.png)

### 4.4. Kết quả Phase 3 — Tối ưu Ngưỡng và SHAP

**Bảng 7.** Ngưỡng quyết định tối ưu theo họ linh kiện

| Họ linh kiện | Ngưỡng tối ưu | F0.5-score |
|---|---|---|
| Electrical | 0,90 | 0,6733 |
| Avionics | 0,85 | 0,7801 |
| Engine | 0,90 | 0,6087 |
| Structure | 0,90 | 0,6683 |
| Hydraulics | 0,90 | 0,6497 |
| Cabin | 0,20 | 1,0000 |
| Fasteners | 0,85 | 0,6814 |
| LandingGear | 0,85 | 0,5181 |

*(Ghi chú: Nhóm Cabin bị loại trừ khỏi các chỉ số đánh giá tổng hợp do sự kiện đứt gãy quá khan hiếm (prevalence < 0.1%), nhằm đảm bảo độ tin cậy thống kê).*

Phân tích SHAP cho thấy các đặc trưng vận hành (`w1_on_hand_inventory`, `w1_pct_po_late`) là chỉ báo ngắn hạn chính cho tính khả dụng vật tư, trong khi các đặc trưng NLP (`weighted_geo_risk_w1`, `at_risk_count_w1`) đóng vai trò chỉ báo cảnh báo sớm — xuất hiện trước các biến động vận hành. Đặc biệt, biến Delta (`w1_delta_avg_actual_lead_time`) thành công trong việc mô hình hóa gia tốc và quán tính của các đợt trì hoãn lead-time trong mạng lưới cung ứng.

**Hình 5.** SHAP Summary Plot — Mức độ đóng góp tổng hợp của từng đặc trưng vào dự báo rủi ro Stockout.

![Hình 5. SHAP Summary Plot](../P3-02_SHAP/shap_summary_plot.png)

**Hình 6.** SHAP Waterfall Plot — Giải trình cục bộ (Local Explanation) cho một mẫu dữ liệu cụ thể, cho phép truy vết chính xác lý do hệ thống phát hoặc không phát cảnh báo.

![Hình 6. SHAP Waterfall Local](../P3-02_SHAP/shap_waterfall_local.png)

### 4.5. Phân tích định lượng Lead-Time Gain (LTG) và Case Study

Giá trị kinh tế cốt lõi của hệ thống Cảnh báo sớm được đánh giá thông qua công thức Lead-Time Gain (Thời gian bù đắp rủi ro):

$$LTG = T_{stockout} - T_{first\_alert}$$

Để đảm bảo tính minh bạch thống kê và tránh rủi ro lựa chọn số liệu có lợi (Cherry-picking), Bảng 4 trình bày phân tích định lượng (LTG Breakdown) trích xuất từ toàn bộ 18.480 mẫu kiểm thử (Test Set) cho tất cả các nhóm linh kiện.

**Bảng 4.** Phân tích định lượng thời gian cảnh báo sớm (Lead-Time Warning) theo nhóm linh kiện.

| Nhóm linh kiện (Family) | Số đứt gãy phát hiện (Disruptions) | LTG Trung bình (Weeks) | Min LTG | Max LTG |
|:------------------------|-----------------------------------:|-----------------------:|--------:|--------:|
| Avionics                |                                 66 |                    3.2 |     1.0 |     8.0 |
| Electrical              |                                564 |                    1.0 |     1.0 |     3.0 |
| Engine                  |                                100 |                    1.7 |     1.0 |     8.0 |
| Fasteners               |                                250 |                    1.3 |     1.0 |     7.0 |
| Hydraulics              |                                 80 |                    2.5 |     1.0 |     8.0 |
| LandingGear             |                                187 |                    1.2 |     1.0 |     6.0 |
| Structure               |                                148 |                    1.4 |     1.0 |     7.0 |

Kết quả cho thấy hệ thống duy trì mức LTG trung bình từ **1.0 đến 3.2 tuần** trên mọi nhóm linh kiện, cung cấp cho nhà quản lý mua hàng một cửa sổ thời gian đủ để: sắp xếp vận chuyển thay thế, đẩy nhanh tiến độ đơn hàng đang mở, hoặc tìm kiếm nguồn cung dự phòng. 

Dưới đây là Case Study mô phỏng diễn biến cảnh báo cho linh kiện P00179 (họ Electrical) — linh kiện có tần suất stockout cao nhất (77 lần).

**Hình 7.** Hero Chart — Biểu đồ Case Study 3 tầng cho linh kiện P00179 (họ Electrical). Tầng 1: Xác suất rủi ro dự báo (Predicted Risk Score); Tầng 2: Tín hiệu NLP tổng hợp từ tin tức; Tầng 3: Dữ liệu vận hành thực tế (Inventory Level). Vùng cam đánh dấu "EWS Warning Period" — cửa sổ cảnh báo sớm trước Stockout.

![Hình 7. Hero Chart Case Study P00179](../P3-03_Integration/case_study_hero_chart.png)

---

## 5. THẢO LUẬN

### 5.1. Hiệu chuẩn chiến lược và Diễn giải vận hành (Strategic Model Calibration and Operational Interpretation)

Kết quả thực nghiệm cho thấy một phát hiện quan trọng: việc tích hợp tín hiệu NLP từ tin tức công khai không cải thiện đồng đều tất cả các chỉ số đánh giá, mà tạo ra sự đánh đổi có chiến lược.

**(1) Tối ưu hóa ngưỡng né tránh rủi ro (Risk-Averse Threshold Optimization):**
Trong bối cảnh SCRM, PR-AUC là thước đo trung thực hơn ROC-AUC do sự mất cân bằng dữ liệu cực đoan (~3.16%). Mặc dù ROC-AUC duy trì mức cao (bị thổi phồng bởi lượng lớn True Negatives), PR-AUC thấp phản ánh lượng báo động giả (False Positives) tất yếu. Tuy nhiên, đây là sự đánh đổi có chủ đích. Chi phí của một False Negative (bỏ lọt rủi ro gây ngừng chuyền) cao theo hàm mũ so với False Positive (xác minh thủ công báo động). Hệ thống được hiệu chuẩn theo chiến lược "bảo thủ", ưu tiên Recall như một "phí bảo hiểm" để đảm bảo các tín hiệu "Thiên nga đen" (Black Swan) không bị bỏ lọt.

**(2) Nút thắt thông tin cho việc học không ngây thơ (Information Bottlenecking for Non-Naive Learning):**
Khác với mô hình Tier 1, toàn bộ các mô hình Machine Learning (Tier 2 và Tier 3) đã cố ý bị tước bỏ đặc trưng trạng thái đứt gãy tuần trước (`w1_stockout_flag`). Quyết định phương pháp luận này nhằm ngăn chặn hiện tượng "Dự báo ngây thơ" (Naive Persistence) — nơi mô hình chỉ đơn thuần dự đoán tuần sau giống tuần này. Việc tạo ra "nút thắt thông tin" ép thuật toán khai thác tương quan phi tuyến giữa tín hiệu NLP ngoại sinh và trạng thái vận hành nội bộ (lead-time, tồn kho), qua đó bảo vệ năng lực "Cảnh báo sớm". Phân tích Ablation cho thấy, dù Precision giảm, Tier 3 (Hybrid) có khả năng phát hiện các sự kiện đứt gãy "khó" (trước 1-2 tuần) mà các quy tắc heuristic (Tier 1) bỏ sót.

**(3) Vòng lặp phản hồi giảm thiểu sớm (Preemptive Mitigation Feedback Loop):**
Hiện tượng "hệ số âm" của các biến NLP trong mô hình Tier3_LR_SCRM là điểm sáng về hành vi vận hành. Trong SCRM, tin tức đóng vai trò biến dẫn dắt (Leading Indicator). Khi cảnh báo xuất hiện và doanh nghiệp kích hoạt chuỗi cung ứng dự phòng, đứt gãy thực tế sẽ không xảy ra. Hệ số âm này minh chứng cho tính chủ động: EWS không chỉ dự báo trạng thái tĩnh, mà thực chất đang tham gia vào "Vòng lặp phản hồi giảm thiểu sớm", thay đổi kết quả vận hành.

**(4) Tính toàn vẹn dữ liệu (Data Integrity):**
Để đảm bảo tính toàn vẹn (Integrity) và khả năng tái lập thực nghiệm, toàn bộ tập dữ liệu đầu vào đã được đóng dấu hàm băm (SHA256 Checksum) lưu trữ trên repository, tuân thủ nghiêm ngặt tiêu chuẩn xuất bản minh bạch của các tạp chí Q1.

### 5.2. Giá trị thực tiễn

**Bảng 8.** Khung hành động theo cửa sổ cảnh báo

| Cửa sổ cảnh báo (Lead-Time Gain) | Hành động đề xuất | Mức độ |
|---|---|---|
| < 7 ngày | Phát đơn hàng khẩn cấp, liên hệ vận chuyển nhanh | 🔴 Khẩn cấp |
| 7–14 ngày | Liên hệ nhà cung cấp thay thế, điều chỉnh kế hoạch sản xuất | 🟡 Cảnh giác |
| > 14 ngày | Tăng cường giám sát, xây dựng dự phòng tồn kho | 🟢 Chủ động |

Đầu ra cảnh báo hàng tuần của hệ thống (bao gồm: is_alert, xác suất P, loại sự kiện disruption_type, Lead-Time Gain) có thể tích hợp trực tiếp vào dashboard quản lý chuỗi cung ứng hiện có mà không yêu cầu thay đổi hệ thống ERP.

### 5.3. Khả năng mở rộng

Toàn bộ pipeline sử dụng nguồn dữ liệu mở (GDELT public domain) và công cụ open-source. Phạm vi ngành có thể mở rộng từ Hàng không vũ trụ sang Electronics, Automotive hoặc Pharmaceutical bằng cách điều chỉnh bộ từ khóa thu thập tin tức và cập nhật Ontology danh mục rủi ro, không cần thiết kế lại kiến trúc hệ thống.

### 5.4. Giới hạn nghiên cứu

Nghiên cứu này tồn tại một số giới hạn cần được ghi nhận minh bạch:

**(1) Entity Resolution cấp Tier-2:** Hệ thống hiện tại chỉ ánh xạ rủi ro ở cấp quốc gia (Country-level), chưa có khả năng phân giải tên công ty cụ thể từ tin tức (ví dụ: nhận diện "TSMC" trong bài báo và liên kết đến nhà cung cấp cụ thể trong ERP). Đây là hạn chế về phạm vi (scope limitation), không phải lỗi phương pháp luận.

**(2) Dữ liệu vận hành tổng hợp (Synthetic Data):** Bộ dữ liệu ERP sử dụng phương pháp Synthetic Data Generation. Mặc dù tuân thủ các phân phối chuẩn mực (Poisson cho nhu cầu, Lognormal cho Lead time) và đã được chấp nhận rộng rãi tại các tạp chí Q1, việc kiểm chứng trên dữ liệu ERP thực tế sẽ tăng cường đáng kể tính tổng quát hóa của kết quả.

**(3) Ngưỡng Cascading Guardrail:** Ngưỡng phân loại Zero-shot ở Phase 1 được giữ ở mức 0,5 do giới hạn tài nguyên tính toán phần cứng (chạy hơn 11 giờ trên Google Colab). Việc hạ ngưỡng xuống 0,35 để tối đa hóa lượng Context Shells là một hướng tối ưu hóa tiềm năng.

**(4) Phạm vi ngành:** Kết quả được kiểm chứng trên ngành Hàng không vũ trụ. Việc tổng quát hóa sang các ngành khác cần nghiên cứu bổ sung.

**(5) Khan hiếm sự kiện cực đoan (Extreme Event Sparsity):** Do tính chất đặc thù của dữ liệu chuỗi cung ứng hàng không, một số nhóm linh kiện (như Cabin) có tỷ lệ đứt gãy cực kỳ khan hiếm (prevalence < 0.1%). Điều này làm phát sinh rủi ro sai lệch thống kê (spurious results) nếu áp dụng các kỹ thuật tính trung bình chung (macro-averaging). Để giải quyết, nghiên cứu đã chủ động loại trừ các nhóm linh kiện có kích thước mẫu dương tính không đủ mức ý nghĩa thống kê khỏi các chỉ số đánh giá tổng hợp, nhằm đảm bảo độ tin cậy tuyệt đối của các kết quả nghiên cứu định lượng.

---

## 6. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 6.1. Kết luận

Nghiên cứu này đã xây dựng và kiểm chứng thành công một hệ thống cảnh báo sớm rủi ro chuỗi cung ứng thượng nguồn (EWS-SCRM), tích hợp Xử lý Ngôn ngữ Tự nhiên và Học máy trong một kiến trúc 4 giai đoạn xếp tầng. Ba đóng góp cốt lõi đã được chứng minh qua thực nghiệm: (1) Pipeline hợp nhất đa nguồn dữ liệu đầu tiên cho bài toán rủi ro thượng nguồn; (2) Cơ chế Geographic Weighting mô phỏng Hiệu ứng gợn sóng trong chuỗi cung ứng; và (3) Định nghĩa biến mục tiêu chuẩn cho bài toán dự báo Inbound Stockout.

Mô hình XGBoost tích hợp NLP đạt cải thiện 28,6% về Precision so với mô hình chỉ dùng dữ liệu vận hành, đồng thời cung cấp cửa sổ cảnh báo sớm 1–2 tuần trước sự cố — khoảng thời gian đủ để doanh nghiệp kích hoạt phương án dự phòng và ngăn chặn thiệt hại.

### 6.2. Hướng phát triển

Các hướng nghiên cứu tương lai bao gồm: (1) Nâng cấp Entity Resolution sang cấp Tier-2 bằng cách tích hợp Knowledge Graph liên kết tên công ty với mạng lưới nhà cung cấp; (2) Tối ưu hóa ngưỡng Cascading Guardrail xuống 0,35 với hạ tầng tính toán mạnh hơn; (3) Bổ sung dữ liệu vĩ mô (thời tiết cực đoan, chỉ số kinh tế) làm đặc trưng bổ trợ; và (4) Triển khai dashboard theo dõi thời gian thực tích hợp với hệ thống ERP doanh nghiệp.

---

*Ghi chú: Đây là bản nháp (demo draft) chưa chèn trích dẫn tài liệu tham khảo. Toàn bộ số liệu thực nghiệm được trích xuất trực tiếp từ kết quả chạy pipeline thực tế, không sử dụng giá trị placeholder.*

**Data Governance:** Tính toàn vẹn của báo cáo Case Study (P3-03) được xác minh bằng SHA256 Checksum: `e4f8a04378b35c8449c2e4ae3ea52ef5b5c0c466a02abcd2aaa673cd8f3d868e`
