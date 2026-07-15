# Hướng dẫn chạy P1-01 (NER & Ontology-Anchored Discovery) trên Google Colab

Giai đoạn P1-01 đã được chuẩn hóa lại theo phương pháp **Ontology-Anchored Discovery** (Tự động hóa 100%, Không LLM, Minh bạch bằng Toán học). 
Để xử lý 5,313 bài báo bằng Transformer nhanh nhất, hãy chạy trên Google Colab.

## Bước 0: Chuẩn bị Google Drive
1. Mở Google Drive của sếp lên.
2. Tạo một thư mục tên là `SCRM_P1_01` ngay ngoài cùng (My Drive).
3. Upload 3 file sau từ máy tính của sếp vào thư mục `SCRM_P1_01` vừa tạo:
   - `pipeline_data/combined_5313.csv`
   - `pipeline_data/event_classification_input_1791.csv`
   - `P1-01_NLP_NER/STATIC_SCRM_ONTOLOGY.json`

## Bước 1: Khởi tạo Colab và Kết nối Drive
1. Tạo một sổ tay (Notebook) mới trên Google Colab.
2. Vào **Runtime > Change runtime type > Chọn T4 GPU** (hoặc xịn hơn).
3. Chạy 2 block code sau để cài thư viện và kết nối tới Google Drive của sếp:

```python
# Block 1: Cài thư viện
!pip install spacy transformers datasets bertopic sentence-transformers
!python -m spacy download en_core_web_trf
```

```python
# Block 2: Kết nối Google Drive
from google.colab import drive
drive.mount('/content/drive')

import os
# Di chuyển thư mục làm việc vào thư mục SCRM_P1_01 sếp vừa tạo
os.chdir('/content/drive/MyDrive/SCRM_P1_01')
print("Đã kết nối thành công! Các file hiện có trong thư mục:")
!ls
```

## Bước 2: Tầng 1 - Trích xuất Thực thể (NER) với spaCy
Dùng mô hình Transformer của spaCy để tìm Tên Công ty, Quốc gia, và Sự kiện. Code này sẽ đọc file `combined_5313.csv` từ Drive và lưu kết quả `ner_features_5313.csv` thẳng lên Drive.

```python
import pandas as pd
import spacy
from tqdm import tqdm
tqdm.pandas()

# Đọc file trực tiếp từ Google Drive
df = pd.read_csv("combined_5313.csv")
nlp = spacy.load("en_core_web_trf")

def extract_entities(text):
    if not isinstance(text, str): return "", "", "", ""
    # Cắt 1500 ký tự đầu để tránh tràn RAM
    doc = nlp(text[:1500])
    orgs = list(set([ent.text for ent in doc.ents if ent.label_ == "ORG"]))
    gpes = list(set([ent.text for ent in doc.ents if ent.label_ == "GPE"]))
    dates = list(set([ent.text for ent in doc.ents if ent.label_ == "DATE"]))
    events = list(set([ent.text for ent in doc.ents if ent.label_ == "EVENT"]))
    return ", ".join(orgs), ", ".join(gpes), ", ".join(dates), ", ".join(events)

print("Đang chạy NER...")
df[['NER_ORG', 'NER_GPE', 'NER_DATE', 'NER_EVENT']] = df['content'].progress_apply(
    lambda x: pd.Series(extract_entities(x))
)

# Lưu thẳng vào Google Drive
df.to_csv("ner_features_5313.csv", index=False)
print("Xong Tầng 1! File ner_features_5313.csv đã được lưu an toàn trong Drive của bạn.")
```

## Bước 3: Tầng 2 - Ontology-Anchored Event Discovery (Không LLM)
Thay vì dùng LLM hay dùng con người gán nhãn thủ công, chúng ta dùng Cosine Similarity để so khớp Tâm cụm của BERTopic với các Nhãn chuẩn mực trong file Ontology tĩnh.

```python
import json
import numpy as np
import pandas as pd
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Đọc dữ liệu từ Google Drive
df_risk = pd.read_csv("event_classification_input_1791.csv")
docs = df_risk['content'].fillna("").tolist()

with open("STATIC_SCRM_ONTOLOGY.json", "r", encoding="utf-8") as f:
    ontology = json.load(f)

# 2. Extract Embeddings & Khởi tạo BERTopic
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
topic_model = BERTopic(embedding_model=embedding_model, language="english", verbose=True)

print("Đang chạy BERTopic để phân cụm...")
topics, probs = topic_model.fit_transform(docs)
df_risk['bertopic_cluster_id'] = topics

# 3. Chuyển đổi Ontology thành Vectors
ontology_labels = []
ontology_texts = []
for key, data in ontology['categories'].items():
    ontology_labels.append(key)
    # Gộp Tên, Mô tả và Keywords để tạo ngữ nghĩa (Knowledge Base)
    text_repr = f"{data['name']}. {data['description']}. Keywords: {', '.join(data['keywords'])}"
    ontology_texts.append(text_repr)

print("Đang mã hóa Ontology...")
ontology_embeddings = embedding_model.encode(ontology_texts)

# 4. Gán nhãn tự động bằng Cosine Similarity (Deterministic Mapping)
print("Đang gán nhãn tự động dựa trên Cosine Similarity...")
topic_info = topic_model.get_topic_info()

# Lấy embedding của tâm các cụm (Topic Embeddings)
topic_embeddings = topic_model.topic_embeddings_

cluster_to_label = {}
for i, row in topic_info.iterrows():
    topic_id = row['Topic']
    if topic_id == -1:
        cluster_to_label[topic_id] = "GENERAL_DISRUPTION" # Outlier
        continue
        
    # Tính Cosine Similarity giữa cụm này và tất cả các nhãn Ontology
    sim_scores = cosine_similarity([topic_embeddings[i]], ontology_embeddings)[0]
    
    # Lấy nhãn có điểm tương đồng cao nhất
    best_match_idx = np.argmax(sim_scores)
    best_label = ontology_labels[best_match_idx]
    cluster_to_label[topic_id] = best_label

# Cập nhật nhãn vào file
df_risk['final_event_type'] = df_risk['bertopic_cluster_id'].map(cluster_to_label)

# Lưu thẳng vào Google Drive
df_risk.to_csv("event_labels_1791_ontology_mapped.csv", index=False)
print("Hoàn thành! File event_labels_1791_ontology_mapped.csv đã nằm ngoan ngoãn trong Drive của bạn.")
```

## Bước 4: Tải kết quả về
Sau khi chạy xong, bạn mở thư mục `SCRM_P1_01` trên Google Drive sẽ thấy xuất hiện thêm 2 file mới:
1. `ner_features_5313.csv`
2. `event_labels_1791_ontology_mapped.csv`

Bạn chỉ việc tải 2 file này về và bỏ vào thư mục `pipeline_data/` ở máy để chuẩn bị gộp vào Feature Matrix.
