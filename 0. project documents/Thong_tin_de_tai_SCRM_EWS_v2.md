# THÔNG TIN ĐỀ TÀI NGHIÊN CỨU KHOA HỌC

---

## TÊN ĐỀ TÀI

**Tiếng Việt:**
Ứng dụng Khai thác Dữ liệu Web và Xử lý Ngôn ngữ Tự nhiên Kết hợp Học máy để Xây dựng Hệ thống Cảnh báo Sớm Nguy cơ Đứt gãy Chuỗi Cung ứng Thượng nguồn

**Tiếng Anh:**
Smart Inbound Supply Chain Risk Monitoring with Web Data Mining, Natural Language Processing, and Machine Learning for Early Warning of Upstream Disruption and Inventory Stockout

**Từ khóa:** Inbound Supply Risk, Inventory Stockout, Early Warning System (EWS), Named Entity Recognition (NER), Event Classification, Supply Chain Risk Monitoring (SCRM), Web Data Mining, Vendor Disruption, DistilBERT, Walk-forward Validation

---

## TÓM TẮT

Đề tài xây dựng một hệ thống giám sát rủi ro chuỗi cung ứng **thượng nguồn** (inbound) tự động, có khả năng phát hiện sớm nguy cơ thiếu hụt tồn kho và đứt gãy nguồn cung bằng cách khai thác đồng thời hai nguồn dữ liệu: (1) tin tức rủi ro toàn cầu thu thập từ các nguồn chuyên ngành logistics (JOC, SupplyChainBrain) qua GDELT BigQuery Index, và (2) dữ liệu vận hành nội bộ gồm 05 bảng dữ liệu lịch sử mua hàng, mức tồn kho, sự cố chất lượng và phân bổ nhà cung cấp theo địa lý (Aerospace Supply Chain Dataset đã qua Data Enrichment).

Hệ thống hoạt động theo kiến trúc ba lớp tuần tự: **Lớp NLP** trích xuất tín hiệu rủi ro có cấu trúc từ văn bản báo chí phi cấu trúc; **Lớp Mapping** ánh xạ các sự kiện rủi ro bên ngoài vào dữ liệu vận hành nội bộ thông qua cơ chế 3D Soft Join (Thời gian × Địa lý × Danh mục); và **Lớp Intelligence** tổng hợp đặc trưng đa chiều, huấn luyện mô hình Machine Learning dự báo xác suất đứt gãy nguồn cung P ∈ [0, 1] theo tuần, với ngưỡng cảnh báo được xác định từ đường cong ROC.

Biến mục tiêu (y_true) được định nghĩa thuần túy từ góc độ inbound logistics: y_true = 1 khi mức tồn kho chạm ngưỡng ≤ 0 (on_hand_qty ≤ 0) hoặc khi tồn tại ít nhất một đơn hàng từ nhà cung cấp về trễ so với cam kết (receipt_date > promised_date) trong cùng tuần quan sát.

---

## I. LÝ DO CHỌN ĐỀ TÀI (TÍNH CẤP THIẾT)

### 1.1. Bối cảnh thực tiễn

Trong thập kỷ vừa qua, các cú sốc chuỗi cung ứng toàn cầu — từ đại dịch COVID-19 (2020–2021), sự cố tắc nghẽn kênh đào Suez (2021), đến cuộc khủng hoảng thiếu hụt chip bán dẫn (2021–2023) và xung đột địa chính trị tại Biển Đỏ (2024) — đã phơi bày tính dễ tổn thương cực kỳ cao của các doanh nghiệp sản xuất khi phụ thuộc vào chuỗi cung ứng thượng nguồn phân tán toàn cầu. Theo báo cáo của Gartner (2023), hơn 87% doanh nghiệp sản xuất toàn cầu đã trải qua ít nhất một sự cố gián đoạn nguồn cung có tác động vật chất trong giai đoạn 2020–2023.

Thách thức cốt lõi không nằm ở việc **phản ứng** sau khi đứt gãy xảy ra, mà ở khả năng **phát hiện sớm tín hiệu cảnh báo** từ môi trường bên ngoài — thường xuất hiện trước dưới dạng tin tức địa chính trị, thông báo đình công, thiên tai hoặc biến động giá nguyên liệu — trước khi các hệ quả vận hành (tồn kho cạn kiệt, dây chuyền dừng máy) xảy ra thực sự.

### 1.2. Khoảng trống nghiên cứu

Các nghiên cứu hiện có về Supply Chain Risk Monitoring (SCRM) tồn tại một trong hai giới hạn: (a) sử dụng dữ liệu tin tức đơn thuần mà không kết nối được với dữ liệu vận hành nội bộ (Cano-Marin et al., 2023; Zhu et al., 2023), hoặc (b) sử dụng dữ liệu vận hành nội bộ mà không khai thác tín hiệu cảnh báo sớm từ môi trường bên ngoài (Ivanov et al., 2022; Brintrup et al., 2020). Không có nghiên cứu nào giải quyết đồng thời bài toán **ánh xạ liên kết** (entity-to-operations mapping) giữa hai luồng dữ liệu có granularity và cấu trúc hoàn toàn khác biệt này.

Hơn nữa, hầu hết các framework SCRM hiện tại tập trung vào **outbound logistics** (rủi ro giao hàng trễ đến khách hàng cuối) mà bỏ qua **inbound logistics** (rủi ro đứt gãy nguồn cung từ nhà cung cấp thượng nguồn) — vốn là nguyên nhân gốc rễ của hầu hết các sự cố vận hành sản xuất.

### 1.3. Tính cấp thiết của đề tài

Đề tài này giải quyết trực tiếp khoảng trống kép trên bằng cách xây dựng một pipeline tích hợp đầu cuối (end-to-end), kết hợp kỹ thuật Web Data Mining, NLP và Machine Learning để tạo ra một Hệ thống Cảnh báo Sớm (Early Warning System — EWS) cho rủi ro thượng nguồn, có khả năng cung cấp tín hiệu cảnh báo có độ trễ (lead time) đủ lớn để doanh nghiệp kịp thời hành động (tìm nhà cung cấp thay thế, điều chỉnh kế hoạch sản xuất, tăng cường dự phòng tồn kho).

---

## II. MỤC TIÊU NGHIÊN CỨU

### 2.1. Mục tiêu chung

Xây dựng và kiểm chứng thực nghiệm một hệ thống giám sát rủi ro chuỗi cung ứng thượng nguồn (Inbound Supply Chain Risk Monitoring) tích hợp NLP và Machine Learning, có khả năng cảnh báo sớm nguy cơ đứt gãy nguồn cung và thiếu hụt tồn kho dựa trên tín hiệu từ tin tức rủi ro toàn cầu kết hợp với dữ liệu vận hành nội bộ, với thời gian cảnh báo trước (Lead Time of Warning) đủ để doanh nghiệp phản ứng chủ động.

### 2.2. Mục tiêu cụ thể

**Mục tiêu 1 — Xây dựng Lớp NLP:** Thiết kế và triển khai pipeline NLP tự động, có khả năng phân loại mức độ rủi ro và trích xuất thực thể địa lý, ngành nghề từ corpus tin tức (JOC/SupplyChainBrain, ~2.000 bài) thông qua mô hình DistilBERT fine-tuned, với bộ dữ liệu huấn luyện 700 bài được gán nhãn thủ công có kiểm tra độ đồng thuận (Fleiss' Kappa ≥ 0.70) và sử dụng chronological split (80/10/10) để đảm bảo tính toàn vẹn thời gian.

**Mục tiêu 2 — Thiết kế cơ chế 3D Soft Join:** Xây dựng cơ chế ánh xạ đa chiều (3D Soft Join theo Thời gian × Địa lý × Danh mục) để liên kết các sự kiện rủi ro được trích xuất từ tin tức với dữ liệu vận hành nội bộ, trong đó chiều Địa lý sử dụng vị trí nhà cung cấp thượng nguồn (supplier_locations.csv) được xây dựng theo phương pháp rule-based enrichment có cơ sở domain (phân bổ quốc gia theo nhóm linh kiện dựa trên báo cáo ngành FAA/IATA).

**Mục tiêu 3 — Xây dựng Lớp Machine Learning:** Xây dựng Feature Matrix X tổng hợp đặc trưng từ cả hai nguồn dữ liệu (đơn vị quan sát: 1 hàng = 1 tuần × 1 nhóm linh kiện), huấn luyện và đánh giá mô hình phân loại nhị phân dự báo xác suất đứt gãy nguồn cung P ∈ [0, 1] theo phương pháp Walk-forward Validation (5 folds, mỗi fold mở rộng thêm một quý), với Logistic Regression làm baseline (chỉ dùng operational features, không có NLP) và với ngưỡng cảnh báo được xác định tự động từ đường cong ROC tối ưu hóa F1-score cho lớp thiểu số (y = 1).

**Mục tiêu 4 — Đánh giá hiệu quả thực tiễn:** Đo lường Lead Time of Warning — khoảng thời gian (ngày) từ thời điểm hệ thống phát cảnh báo đầu tiên đến khi tồn kho thực sự chạm đáy (on_hand_qty = 0) — nhằm chứng minh giá trị kinh tế và thực tiễn của hệ thống.

---

## III. ĐỐI TƯỢNG VÀ PHẠM VI NGHIÊN CỨU

### 3.1. Đối tượng nghiên cứu

Đối tượng nghiên cứu của đề tài là **cơ chế kết hợp dữ liệu phi cấu trúc từ tin tức và dữ liệu vận hành có cấu trúc** để nhận diện và định lượng rủi ro đứt gãy chuỗi cung ứng thượng nguồn. Cụ thể, đề tài tập trung vào hai thực thể chính:

- **Nguồn dữ liệu bên ngoài:** Corpus tin tức rủi ro từ các ấn phẩm chuyên ngành logistics và chuỗi cung ứng quốc tế (JOC, SupplyChainBrain), thu thập qua GDELT BigQuery Index trong giai đoạn **2022–2024** (đồng bộ với khung thời gian dữ liệu vận hành).
- **Nguồn dữ liệu bên trong:** Bộ dữ liệu vận hành nội bộ Aerospace Supply Chain gồm 05 bảng CSV (parts_master, shifted_purchase_orders, shifted_quality_incidents, shifted_supply_chain_history, supplier_locations), phản ánh lịch sử mua hàng, tồn kho và sự cố nhà cung cấp trong giai đoạn **2022–2024**.

### 3.2. Phạm vi nghiên cứu

| Chiều phạm vi | Giới hạn áp dụng |
|---|---|
| **Loại rủi ro** | Rủi ro thượng nguồn (Inbound/Upstream Supply Risk): đứt gãy từ nhà cung cấp dẫn đến thiếu hụt nguyên vật liệu và stockout tồn kho. Không bao gồm rủi ro outbound (giao hàng trễ đến khách hàng cuối). |
| **Giai đoạn thời gian** | **2022–2024** (đồng bộ hóa giữa hai nguồn dữ liệu bằng Time-shifting). |
| **Ngành nghề** | Ngành sản xuất hàng không vũ trụ (Aerospace Manufacturing), đặc biệt chuỗi cung ứng linh kiện có phân loại criticality_class A/B/C. |
| **Tín hiệu rủi ro bên ngoài** | Tin tức địa chính trị, thiên tai, đình công, logistics disruption liên quan đến khu vực địa lý của nhà cung cấp thượng nguồn. |
| **Đơn vị dự báo** | Tuần (weekly granularity), aggregated theo nhóm linh kiện. |

### 3.3. Sự kết hợp giữa hai nguồn dữ liệu

Điểm khác biệt cốt lõi của đề tài so với các nghiên cứu trước là việc khai thác **đồng thời và có hệ thống** cả tin tức rủi ro bên ngoài lẫn dữ liệu vận hành nội bộ. Tin tức đóng vai trò "tín hiệu sớm" (leading indicator), trong khi dữ liệu vận hành cung cấp "nhãn thực tế" (ground truth label) và "đặc trưng trạng thái" (operational state features) cho mô hình học máy.

### 3.4. Cơ sở khoa học của Synthetic Inbound Data (Dữ liệu vận hành tổng hợp)

Trong nghiên cứu SCRM, dữ liệu ERP thực tế (PO, Inventory, Lead time) của doanh nghiệp Hàng không vũ trụ mang tính tuyệt mật và không thể tiếp cận. Để giải quyết hạn chế này, nghiên cứu áp dụng phương pháp tạo **Synthetic Inbound Data (Dữ liệu tổng hợp)**. 
- **Cơ sở thống kê**: Dữ liệu vận hành tuân theo các phân phối chuẩn mực (ví dụ: Nhu cầu theo phân phối Poisson/Negative Binomial, Lead time theo phân phối Lognormal/Gamma). Việc sử dụng thuật toán mô phỏng (Simulation) để sinh dữ liệu phản ánh chính xác các đặc tính thống kê của chuỗi cung ứng thực tế.
- **Tính hợp lệ học thuật**: Phương pháp sử dụng Synthetic Data để huấn luyện và kiểm định mô hình AI hiện đang được chấp nhận rộng rãi và báo cáo minh bạch tại các tạp chí Q1 hàng đầu (như IJPR, C&IE) cũng như các hội nghị chuyên sâu (FinNLP 2024). Điều này đảm bảo tính hợp lệ (validity) và độ tin cậy của khung cảnh báo rủi ro mà nghiên cứu đề xuất.
- **Tính Nhân quả và Đồng bộ thời gian (Temporal Alignment)**: Thuật toán sinh dữ liệu tuân thủ quy tắc mô phỏng nhân quả khắt khe. Các điểm đứt gãy mô phỏng (ví dụ: Stockout, Delay) được tạo ra bắt buộc phải có độ trễ (Lag 7-14 ngày) xảy ra **SAU** thời điểm một tin tức rủi ro thực tế trên GDELT được công bố. Cơ chế này loại bỏ hoàn toàn hiện tượng rò rỉ dữ liệu (Data Leakage) từ tương lai và đảm bảo mô hình đang thực sự làm nhiệm vụ "dự báo".

---

## IV. PHƯƠNG PHÁP NGHIÊN CỨU

### 4.1. Tổng quan kiến trúc hệ thống

Hệ thống được thiết kế theo Kiến trúc Tuyến tính 4 Giai đoạn (Linear 4-Phase Pipeline), áp dụng tư duy "Cascading AI" (Trí tuệ nhân tạo xếp tầng) nhằm xử lý thông tin từ thô đến tinh:

```text
[Phase 0] Sensing ──► [Phase 1] Sense-making ──► [Phase 2] Feature & ML ──► [Phase 3] Evaluation
(Binary Filter)       (Taxonomy & Severity)      (Geo-Join & XGBoost)       (Threshold & SHAP)
```

### 4.2. Phase 0 — Sensing (Cảm nhận rủi ro)

**Mục tiêu:** Lọc ra các bài báo có mang tín hiệu rủi ro (At Risk) từ lượng lớn tin tức thô.
- **Dữ liệu:** ~7.200 bài báo thu thập qua GDELT API (2022-2024).
- **Mô hình (Classifier C0):** Sử dụng mô hình Ngôn ngữ lớn DistilBERT để phân loại nhị phân (NO_RISK vs AT_RISK).
- **Quyết định học thuật**: Tại Phase này, mô hình chỉ làm nhiệm vụ "người gác cổng" (Gatekeeper). Việc tối ưu hóa sẽ ưu tiên chỉ số **Recall**, đảm bảo không bỏ lọt bất kỳ tín hiệu yếu (weak signal) nào, thay vì cố gắng phân tích sâu mức độ rủi ro ngay từ đầu. Để chứng minh hệ thống không bị quá tải bởi nhiễu (Lỗi lan truyền xếp tầng - Cascading Error), nghiên cứu sẽ xuất báo cáo minh bạch mức độ đánh đổi độ chính xác (Precision Trade-off) nhằm thuyết phục tính vững (Robustness) của khung cảnh báo.

### 4.3. Phase 1 — Sense-making (Hiểu rủi ro và Phân loại mức độ)

**Mục tiêu:** Bóc tách các bài báo "At Risk" thành các chủ đề cụ thể và đánh giá mức độ nghiêm trọng (Severity).
- **Trích xuất Taxonomy (P1-01):** Sử dụng BERTopic (kết hợp UMAP và HDBSCAN) để tự động nhóm các bài báo thành các cụm rủi ro tự nhiên (Data-driven Taxonomy) thay vì dùng bộ từ khóa cứng nhắc. Hệ thống tích hợp Quality Gate để kiểm soát Cluster -1 (Cụm nhiễu), nếu nhiễu > 40% sẽ dừng để tinh chỉnh thuật toán.
- **Chuyên gia đánh giá mức độ nghiêm trọng (P1-02):** Các bài báo sau khi được gán nhãn Taxonomy sẽ đi qua một bộ phân loại (Severity Specialist Model) để chia thành Medium Risk và High Risk. Đây là đặc tính của "Taxonomy-Conditioned AI", giúp mô hình đánh giá rủi ro chính xác hơn nhờ hiểu được bối cảnh (Context).

### 4.4. Phase 2 — Feature Engineering & Machine Learning

**Mục tiêu:** Ánh xạ rủi ro địa lý và huấn luyện mô hình dự báo đứt gãy.
- **Trích xuất thực thể (NER):** Dùng spaCy trích xuất vị trí địa lý từ tin tức rủi ro cao.
- **Geographic Weighting (Soft Join):** Thay vì Inner Join cứng nhắc, dự án sử dụng Hàm trọng số địa lý (Geographic Weighting) để khớp rủi ro từ bài báo với Quốc gia của Nhà cung cấp (Supplier Country). Điều này giúp hệ thống "cảm nhận" được hiệu ứng gợn sóng (Ripple Effect) trong chuỗi cung ứng.
- **Feature Matrix & Time-Series Stationarity:** Các biến số được gộp theo tuần (W-1). Đặc biệt, hệ thống sử dụng kiểm định Augmented Dickey-Fuller (ADF Test) cho các biến vận hành (Operational Features). Nếu phát hiện tính không dừng (Non-stationary), biến sai phân bậc 1 (Delta) sẽ được tạo ra để ngăn chặn hoàn toàn rủi ro **Hồi quy giả mạo (Spurious Regression)**. Hệ thống giữ cả biến gốc (Baseline State) để cung cấp cho XGBoost học các tương tác phi tuyến.
- **Ablation Study 2x2:** So sánh hiệu suất giữa mô hình Tuyến tính (LR Lasso - sử dụng L1 Penalty để tự động lọc nhiễu đa cộng tuyến) và Phi tuyến (XGBoost) để chứng minh tính ưu việt của việc kết hợp dữ liệu NLP.

### 4.5. Phase 3 — Evaluation & Explainability

- **Tối ưu hóa Threshold:** Tự động tìm ngưỡng cắt (Threshold Optimization) từ đường cong ROC-AUC thay vì dùng mức 0.5 cố định, nhằm cân bằng giữa việc chống "Alert Fatigue" và không bỏ sót rủi ro.
- **SHAP Analysis (Tính diễn giải):** Sử dụng thư viện SHAP để "mở hộp đen" mô hình XGBoost, giải thích rõ đặc trưng NLP hay Operational đóng vai trò quyết định trong việc phát cảnh báo.
- **Kiểm soát tính tái lập & Quản trị Dữ liệu (Reproducibility & Data Governance):** Toàn bộ hệ thống 4 giai đoạn tuân thủ giao thức đóng băng tham số ngẫu nhiên (`seed=42`). Đặc biệt, các biểu đồ (Hero Chart) và báo cáo thực nghiệm đều được nhúng hệ thống mã băm mật mã **SHA256 Checksum** để khóa dữ liệu, đảm bảo tính nguyên bản và minh bạch học thuật tuyệt đối trước các hội đồng kiểm duyệt.

---

## V. TÍNH MỚI VÀ ĐÓNG GÓP KHOA HỌC

| Tiêu chí | Cano-Marin et al. (2023) | Ivanov et al. (2022) | Zhu et al. (2023) | Brintrup et al. (2020) | **Đề tài này** |
|---|---|---|---|---|---|
| NLP từ tin tức | ✓ | ✗ | ✓ | ✗ | **✓** |
| Dữ liệu vận hành nội bộ | ✗ | ✓ | ✗ | ✓ | **✓** |
| Multi-source Fusion | ✗ | ✗ | Một phần | ✗ | **✓** |
| Supply-side Geography Mapping | ✗ | ✗ | ✗ | ✗ | **✓** |
| Inbound Stockout Target | ✗ | Một phần | ✗ | ✗ | **✓** |
| Walk-forward Validation | ✗ | ✗ | ✗ | ✓ | **✓** |

**Đóng góp 1 — Multi-source Inbound Risk Fusion:** Đề tài là nghiên cứu đầu tiên xây dựng pipeline tích hợp đầu cuối kết hợp tin tức phi cấu trúc (NLP) và dữ liệu vận hành inbound có cấu trúc trong cùng một hệ thống cảnh báo rủi ro thượng nguồn.

**Đóng góp 2 — Entity-to-Operations Mapping theo Supply-side Geography:** Thiết kế 3D Soft Join (Thời gian × Địa lý NHÀ CUNG CẤP × Danh mục) để ánh xạ thực thể rủi ro trong tin tức vào dữ liệu vận hành mà không cần entity overlap tự nhiên — giải quyết bài toán granularity mismatch và demand/supply geography confusion chưa được xử lý trong các nghiên cứu trước.

**Đóng góp 3 — Inbound Ground Truth Definition:** Đề xuất định nghĩa biến mục tiêu y_true chuẩn cho bài toán inbound stockout prediction: y_true = 1 khi on_hand_qty ≤ 0 OR receipt_date > promised_date — phân biệt rõ ràng với outbound delivery risk (late_delivery_risk) vốn bị dùng nhầm trong nhiều nghiên cứu trước.

---

## VI. Ý NGHĨA KHOA HỌC VÀ THỰC TIỄN

### 6.1. Ý nghĩa khoa học

Đề tài đóng góp vào cơ sở lý luận của Supply Chain Risk Monitoring (SCRM) bằng cách: (a) xác lập quy trình chuẩn cho việc khai thác tín hiệu rủi ro từ tin tức chuyên ngành và ánh xạ sang dữ liệu vận hành inbound; (b) đề xuất phương pháp đánh giá mô hình nghiêm ngặt theo thứ tự thời gian (chronological split + walk-forward validation) phù hợp với đặc thù time-series của dữ liệu chuỗi cung ứng; (c) xây dựng framework định nghĩa biến mục tiêu inbound rõ ràng, có thể tái sử dụng trong các nghiên cứu tiếp theo.

### 6.2. Ý nghĩa thực tiễn

**Đối với doanh nghiệp sản xuất:**
- Hệ thống cung cấp cảnh báo trước (lead time) đủ để doanh nghiệp kịp thời kích hoạt phương án dự phòng: khi TTS < 7 ngày → phát đơn hàng khẩn; khi TTS 7–14 ngày → liên hệ nhà cung cấp thay thế; khi TTS > 14 ngày → theo dõi và tăng cường giám sát.
- Output cảnh báo theo tuần (is_alert, P, TTS, disruption_type) có thể tích hợp trực tiếp vào dashboard quản lý chuỗi cung ứng hiện có mà không yêu cầu thay đổi hệ thống ERP.

**Phân tích tác động quản trị qua Kịch bản phản thực tế (Counterfactual Managerial Impact):**
- *Kịch bản Không có NLP (Baseline ERP):* Hệ thống chỉ phát hiện rủi ro khi vật tư đã cập cảng trễ hoặc Hàng tồn kho sụt giảm. Chi phí chữa cháy cực kỳ cao.
- *Kịch bản Có NLP (EWS đề xuất):* Hệ thống phát cảnh báo ngay khi sự kiện địa chính trị/thời tiết tại khu vực nhà cung cấp vừa nổ ra trên GDELT (cho trước Lead Time trung bình từ 7-14 ngày). Sự chênh lệch Lead Time này chính là "Tỷ suất hoàn vốn" (ROI) cực lớn cho việc triển khai AI, giúp quản lý chuỗi cung ứng chuyển từ bị động sang chủ động.

**Đối với doanh nghiệp vừa và nhỏ (SME):**
- Toàn bộ pipeline sử dụng nguồn dữ liệu mở (GDELT public domain, Aerospace public dataset) và công cụ open-source → reproducible, không phát sinh chi phí licensing, có thể triển khai tại SME.

**Khả năng mở rộng:**
- Scope ngành có thể mở rộng từ Aerospace sang Electronics, Automotive hoặc Pharmaceutical bằng cách điều chỉnh keyword filter và rule-based enrichment, không cần thiết kế lại kiến trúc.

---

## VII. KẾ HOẠCH THỰC HIỆN (DỰ KIẾN)

| Giai đoạn | Nhiệm vụ | Sản phẩm đầu ra |
|---|---|---|
| **Phase 0** | Tiền xử lý dữ liệu, huấn luyện mô hình Binary Filter (DistilBERT) | clean_news.csv, Mô hình C0 |
| **Phase 1** | Xây dựng BERTopic Taxonomy, gán nhãn Severity | risk_taxonomy.csv, Mô hình Severity |
| **Phase 2** | NER, Geographic Weighting, Build Feature Matrix X (ADF Test), huấn luyện XGBoost/Lasso | feature_matrix_x.parquet, Bảng Ablation |
| **Phase 3** | Threshold Optimization, SHAP Analysis, báo cáo Integration | Báo cáo hoàn chỉnh, Biểu đồ SHAP |

---

*Tài liệu này được soạn thảo phục vụ mục đích nộp Thông tin Đề tài cho Giảng viên hướng dẫn. Mọi điều chỉnh về phạm vi, dữ liệu hoặc phương pháp sẽ được cập nhật theo ý kiến phản hồi từ Hội đồng Khoa học.*
