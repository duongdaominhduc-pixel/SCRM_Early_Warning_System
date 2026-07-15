# Hướng dẫn Huấn luyện (Fine-tune) DistilBERT trên Google Colab

Tài liệu này hướng dẫn chi tiết từng bước để huấn luyện mô hình `distilbert-base-uncased` trên tập dữ liệu "Gold Label" (2,309 bài) và dùng mô hình đó gán nhãn tự động (Pseudo-labeling) cho ~5,040 bài báo thô còn lại.

---

## BƯỚC 1: Chuẩn bị Môi trường trên Google Colab

1. Truy cập [Google Colab](https://colab.research.google.com/).
2. Tạo một sổ tay mới (New Notebook).
3. Đổi tên sổ tay thành `SCRM_Pseudo_Labeling.ipynb`.
4. Bật GPU: 
   - Trên thanh menu, chọn **Runtime** (Thời gian chạy) -> **Change runtime type** (Thay đổi loại thời gian chạy).
   - Ở mục **Hardware accelerator** (Trình tăng tốc phần cứng), chọn **T4 GPU** và bấm **Save**.

---

## BƯỚC 2: Cài đặt Thư viện và Mount Google Drive

Trên Colab, mỗi đoạn code (block) tương ứng với 1 cell. Bạn hãy copy code dưới đây vào từng cell và bấm nút **Play** (hoặc `Shift + Enter`) để chạy.

**Cell 1: Cài đặt các thư viện cần thiết của HuggingFace**
```python
!pip install -q transformers datasets evaluate scikit-learn
```

**Cell 2: Kết nối (Mount) với Google Drive của bạn**
*Để dữ liệu không bị mất khi đóng Colab, chúng ta sẽ đọc/ghi thẳng lên Drive.*
```python
from google.colab import drive
drive.mount('/content/drive')
```
*(Colab sẽ hiện ra một popup yêu cầu cấp quyền truy cập Drive, bạn cứ bấm "Allow" nhé).*

---

## BƯỚC 3: Upload File Lên Google Drive và Đọc Dữ liệu

1. Bạn hãy vào Google Drive của mình, tạo một thư mục tên là `SCRM_Data`.
2. Upload 2 file lên thư mục này:
   - File nhãn vàng của nhóm: `manual_combined_2309.csv`
   - File chứa ~5,040 bài báo chưa có nhãn: `unlabeled_news_5040.csv` *(Bạn tự chuẩn bị file này có định dạng tương tự nhé)*.

**Cell 3: Code load dữ liệu bằng thư viện Datasets và Pandas**
```python
import pandas as pd
from datasets import Dataset

# Cập nhật lại đường dẫn tới thư mục SCRM_Data trên Drive của bạn
DATA_DIR = "/content/drive/MyDrive/SCRM_Data"

# 1. Đọc tập Gold Label (để Train/Test)
df_gold = pd.read_csv(f"{DATA_DIR}/manual_combined_2309.csv")
# Xử lý: Nối tiêu đề (title) và nội dung (content) bằng token [SEP] để DistilBERT hiểu rõ ranh giới
df_gold['text'] = df_gold['title'].astype(str) + " [SEP] " + df_gold['content'].astype(str)
# Chỉ giữ lại cột text và label
df_gold = df_gold[['text', 'label']]
# Ép kiểu nhãn về số nguyên (0, 1, 2)
df_gold['label'] = df_gold['label'].astype(int)

# Chia tập Gold ra làm Train (80%), Validation (10%) và Test (10%) để đánh giá
from sklearn.model_selection import train_test_split

# Đầu tiên tách 20% cho tập tạm (Temp = Val + Test)
df_train, df_temp = train_test_split(df_gold, test_size=0.2, random_state=42, stratify=df_gold['label'])

# Tiếp theo tách đôi tập Temp (20%) thành Validation (10%) và Test (10%)
df_val, df_test = train_test_split(df_temp, test_size=0.5, random_state=42, stratify=df_temp['label'])

# 2. Đọc tập Unlabeled (để máy tự gán nhãn sau khi train xong)
df_unlabeled = pd.read_csv(f"{DATA_DIR}/unlabeled_news_5040.csv")
# Nối tiêu đề và nội dung bằng token [SEP] tương tự như tập Gold
df_unlabeled['text'] = df_unlabeled['title'].astype(str) + " [SEP] " + df_unlabeled['content'].astype(str)

# Chuyển đổi DataFrame sang định dạng Dataset của HuggingFace
train_dataset = Dataset.from_pandas(df_train)
val_dataset = Dataset.from_pandas(df_val)
test_dataset = Dataset.from_pandas(df_test)

print("Số lượng Train:", len(train_dataset))
print("Số lượng Validation:", len(val_dataset))
print("Số lượng Test:", len(test_dataset))
```

---

## BƯỚC 4: Tiền xử lý văn bản (Tokenization)

Máy học không hiểu chữ cái, nó chỉ hiểu con số. Tokenizer sẽ băm văn bản ra và chuyển thành mã số.

**Cell 4: Tải Tokenizer và map qua dữ liệu**
```python
from transformers import AutoTokenizer

model_checkpoint = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

def tokenize_function(examples):
    # Cắt ngắt ở 512 token (giới hạn của BERT)
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

# Xử lý song song trên tập Train, Val và Test
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_val = val_dataset.map(tokenize_function, batched=True)
tokenized_test = test_dataset.map(tokenize_function, batched=True)
```

---

## BƯỚC 5: Fine-tune Mô hình DistilBERT

Chúng ta sẽ dùng API `Trainer` - cực kỳ tối ưu và dễ dùng.

**Cell 5: Khai báo Mô hình và Khai báo hàm đánh giá độ chính xác (Accuracy, F1)**
```python
import numpy as np
import evaluate
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

# Chúng ta có 3 nhãn (0, 1, 2)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint, num_labels=3)

accuracy_metric = evaluate.load("accuracy")
f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    
    acc = accuracy_metric.compute(predictions=predictions, references=labels)
    # Vì bài toán có 3 nhãn, dùng average='weighted' hoặc 'macro'
    f1 = f1_metric.compute(predictions=predictions, references=labels, average="weighted")
    
    return {"accuracy": acc["accuracy"], "f1": f1["f1"]}
```

**Cell 6: Cấu hình siêu tham số (Hyperparameters) và Bắt đầu Train!**
*(Quá trình này tốn khoảng 5 - 10 phút)*
```python
import torch
from torch import nn
from sklearn.utils.class_weight import compute_class_weight

# Tính toán Class Weights dựa trên phân bố của tập Train
labels = df_train['label'].values
class_weights = compute_class_weight(class_weight='balanced', classes=np.unique(labels), y=labels)
class_weights_tensor = torch.tensor(class_weights, dtype=torch.float32).to('cuda' if torch.cuda.is_available() else 'cpu')

# Kế thừa lớp Trainer để nạp Class Weights vào hàm Loss
class CustomTrainer(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = nn.CrossEntropyLoss(weight=class_weights_tensor)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

training_args = TrainingArguments(
    output_dir=f"{DATA_DIR}/distilbert-scrm-risk",
    eval_strategy="steps",            # Đánh giá theo từng bước nhỏ
    eval_steps=50,                    # Mỗi 50 bước đánh giá 1 lần
    logging_strategy="steps",
    logging_steps=50,
    save_strategy="steps",            # Lưu model khớp với lúc đánh giá
    save_steps=50,
    save_total_limit=2,               # Tự động xóa checkpoint cũ, chỉ giữ 2 cái gần nhất
    learning_rate=1e-5,               # Thích ứng miền thận trọng (Conservative Domain Adaptation)
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,               
    weight_decay=0.1,                 # Phạt mạnh (L2 Regularization = 0.1) chống học vẹt
    warmup_ratio=0.1,                 # Khởi động mềm 10% chặng đường
    load_best_model_at_end=True,      
)

trainer = CustomTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
)

# Kích nổ quá trình huấn luyện
trainer.train()

# BẮT BUỘC: Lưu lại phiên bản mô hình xịn nhất (Best Model) ra thư mục gốc
trainer.save_model(f"{DATA_DIR}/distilbert-scrm-risk")
tokenizer.save_pretrained(f"{DATA_DIR}/distilbert-scrm-risk")

# Đánh giá mô hình trên tập Test hoàn toàn mới (Giai đoạn 1 - Human Baseline)
print("---")
print("Kết quả đánh giá GIAI ĐOẠN 1 trên tập Test (Unseen Data):")
test_results = trainer.evaluate(eval_dataset=tokenized_test)
print(test_results)
```

**Cell 6.5: Vẽ biểu đồ Loss và F1-Score (Bằng chứng cho Bài báo Khoa học)**
```python
import matplotlib.pyplot as plt

# Lấy lịch sử log của Trainer
log_history = trainer.state.log_history
# Phải đảm bảo lấy những log có chứa cả eval_loss và eval_f1
val_logs = [x for x in log_history if 'eval_loss' in x and 'eval_f1' in x]

# Loại bỏ điểm đánh giá cuối cùng trên tập Test (nếu có, điểm này thường dư ra ở cuối)
if len(val_logs) > 1 and val_logs[-1].get('step') == val_logs[-2].get('step'):
    val_logs = val_logs[:-1]
elif len(val_logs) > (5 * len(train_dataset) // 16 // 50): # Ước lượng số log hợp lý
    val_logs = val_logs[:-1]

steps = [x['step'] for x in val_logs]
val_loss = [x['eval_loss'] for x in val_logs]
val_f1 = [x['eval_f1'] for x in val_logs]

fig, ax1 = plt.subplots(figsize=(10, 6))

# Vẽ đường Validation Loss (Trục Y bên trái, màu đỏ)
color1 = 'tab:red'
ax1.set_xlabel('Training Steps')
ax1.set_ylabel('Validation Loss', color=color1)
ax1.plot(steps, val_loss, 'ro-', label='Validation Loss')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True)

# Vẽ đường F1-Score (Trục Y bên phải, màu xanh)
ax2 = ax1.twinx()  
color2 = 'tab:blue'
ax2.set_ylabel('Validation F1-Score', color=color2)  
ax2.plot(steps, val_f1, 'bs-', label='F1-Score')
ax2.tick_params(axis='y', labelcolor=color2)

# Fix giới hạn trục Y cho F1-Score (0.5 đến 0.8) để biểu đồ phản ánh đúng độ ổn định
ax2.set_ylim(0.5, 0.8)

fig.tight_layout()  
plt.title('Validation Loss vs F1-Score (Weighted Stochastic Turbulence)')
plt.show()
print("Lưu biểu đồ kép siêu xịn này lại để dán vào bài báo khoa học nhé!")
```

---

## BƯỚC 6: Pseudo-labeling (Máy tự gán nhãn cho tập thô)

Sau khi model đã khôn lên, chúng ta bắt nó đi đọc 5,040 bài báo còn lại để gán nhãn.
*Nhớ là ta có cổng gác: Chỉ lấy bài nào model tự tin $\ge 0.85$*

**Cell 7: Inference (Dự đoán)**
```python
import torch
import torch.nn.functional as F

# Chuyển model sang chế độ evaluate và ném lên GPU
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

pseudo_labels = []
confidence_scores = []
texts = df_unlabeled['text'].tolist() # Dùng cột text đã được nối từ title và content

# Chạy theo từng batch nhỏ (ví dụ 32) để tránh hết RAM
batch_size = 32
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i : i+batch_size]
    
    # Tokenize batch
    inputs = tokenizer(batch_texts, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    # Tính ra phần trăm tự tin (Softmax probabilities)
    probs = F.softmax(outputs.logits, dim=-1)
    
    # Lấy nhãn có xác suất cao nhất và điểm số tương ứng
    max_probs, preds = torch.max(probs, dim=-1)
    
    pseudo_labels.extend(preds.cpu().numpy())
    confidence_scores.extend(max_probs.cpu().numpy())

# Cập nhật kết quả vào DataFrame
df_unlabeled['machine_label'] = pseudo_labels
df_unlabeled['confidence'] = confidence_scores
```

**Cell 8: Tách dữ liệu theo ngưỡng Confidence = 0.85 và Xuất file CSV**
```python
# Lọc ra những bài tự tin cao
df_high_conf = df_unlabeled[df_unlabeled['confidence'] >= 0.85]

# Lọc ra những bài tự tin thấp (Cần con người duyệt lại hoặc bỏ qua)
df_low_conf = df_unlabeled[df_unlabeled['confidence'] < 0.85]

# Xuất ra file
df_high_conf.to_csv(f"{DATA_DIR}/pseudo_labeled_5040.csv", index=False)
df_low_conf.to_csv(f"{DATA_DIR}/low_confidence_queue.csv", index=False)

print(f"Số bài đạt chuẩn (>= 0.85): {len(df_high_conf)}")
print(f"Số bài dưới chuẩn (< 0.85): {len(df_low_conf)}")
print(f"Đã lưu thành công vào Google Drive của bạn!")
```

**Cell 8.5: Chiến lược Hậu kiểm Đa tầng (Multi-layered Post-processing)**
```python
import pandas as pd
import spacy

print("Đang tải mô hình NER (spaCy)...")
# Tải mô hình tiếng Anh (Colab đã cài sẵn)
import spacy.cli
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')

# Đã bổ sung thêm một số từ khóa thị trường gây nhiễu
negative_keywords = ['cut forecast', 'short of plan', 'import fewer', 'demand forecast', 'market analysis', 'stock price', 'earnings', 'revenue', 'sales expectations', 'profit margin', 'economic conditions']
disruption_keywords = ['delay', 'disruption', 'shortage', 'strike', 'congestion', 'port closed', 'halt', 'cyberattack', 'cyber attack']

survivors = []

print("Đang chạy Màng Lọc Heuristics...")
for idx, row in df_high_conf.iterrows():
    machine = int(row['machine_label'])
    conf = float(row['confidence'])
    text_lower = str(row['text']).lower()
    
    keep = True
    
    # LUẬT THRESHOLD TỐI ƯU (Đã qua Grid Search)
    if machine == 0 and conf < 0.85: keep = False
    elif machine == 1 and conf < 0.87: keep = False
    elif machine == 2 and conf < 0.88: keep = False
        
    if not keep: continue
    
    # LUẬT TỪ KHÓA CHO NHÃN 1
    if machine == 1:
        has_negative = any(kw in text_lower for kw in negative_keywords)
        has_disruption = any(kw in text_lower for kw in disruption_keywords)
        # Nếu chỉ bàn chuyện tài chính thị trường mà không có đứt gãy vật lý -> XÓA
        if has_negative and not has_disruption:
            keep = False
            
    # LUẬT THỜI GIAN NER CHO NHÃN 2
    if machine == 2:
        doc = nlp(str(row['text']))
        date_ents = [ent.text.lower() for ent in doc.ents if ent.label_ == 'DATE']
        
        has_past_time = False
        for d in date_ents:
            if '2020' in d or '2021' in d or '2022' in d or 'last year' in d or 'previous year' in d:
                has_past_time = True
                break
        
        if 'cyberattack' in text_lower:
            has_past_time = True
            
        if has_past_time:
            keep = False
            
    if keep:
        survivors.append(row)

df_refined = pd.DataFrame(survivors)
print(f"Tổng số bài SỐNG SÓT sau màng lọc: {len(df_refined)}")
if len(df_refined) > 0:
    print(df_refined['machine_label'].value_counts())

# Lưu lại file
output_file = f"{DATA_DIR}/pseudo_labeled_refined.csv"
df_refined.to_csv(output_file, index=False)
print(f"\nĐã lưu tập Refined siêu tinh khiết tại: {output_file}")
```

---

## BƯỚC 7: Two-Stage Evaluation (Kiểm định lại)

Để chứng minh tính khoa học, bạn cần huấn luyện lại mô hình lần thứ 2 (Giai đoạn 2).

**Cell 9: Gộp Data và Huấn luyện lại để đánh giá Giai đoạn 2**
```python
# 1. Gộp tập Train cũ với tập Pseudo-label tinh khiết (df_refined)
df_refined_clean = df_refined[['text', 'machine_label']].rename(columns={'machine_label': 'label'})
df_train_combined = pd.concat([df_train, df_refined_clean])

# 2. Tokenize lại tập Train mới
train_combined_dataset = Dataset.from_pandas(df_train_combined)
tokenized_train_combined = train_combined_dataset.map(tokenize_function, batched=True)

# 3. Tính toán lại Class Weights cho tập dữ liệu lai (Quan trọng!)
labels_stage2 = df_train_combined['label'].values
class_weights_stage2 = compute_class_weight(class_weight='balanced', classes=np.unique(labels_stage2), y=labels_stage2)
class_weights_tensor_stage2 = torch.tensor(class_weights_stage2, dtype=torch.float32).to(device)

class CustomTrainerStage2(Trainer):
    def compute_loss(self, model, inputs, return_outputs=False, **kwargs):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits
        loss_fct = nn.CrossEntropyLoss(weight=class_weights_tensor_stage2)
        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))
        return (loss, outputs) if return_outputs else loss

# 4. Warm Start: Kế thừa mô hình xịn nhất từ Giai đoạn 1 (thay vì học lại từ đầu)
# Trainer tự động lưu mô hình xịn nhất vào output_dir sau Giai đoạn 1
model_stage2 = AutoModelForSequenceClassification.from_pretrained(f"{DATA_DIR}/distilbert-scrm-risk", num_labels=3)
model_stage2.to(device)

# 5. Điều chỉnh siêu tham số: Học nhẹ nhàng (Micro-Learning Rate) để không hỏng kiến thức cũ
training_args_stage2 = TrainingArguments(
    output_dir=f"{DATA_DIR}/distilbert-scrm-risk-stage2",
    eval_strategy="steps",
    eval_steps=50,
    logging_strategy="steps",
    logging_steps=50,
    save_strategy="steps",
    save_steps=50,
    save_total_limit=2,               # Tự động xóa checkpoint cũ, chỉ giữ 2 cái gần nhất
    learning_rate=1e-5,               # Giảm một nửa tốc độ học
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=2,               # Chỉ tinh chỉnh 2 vòng là đủ
    weight_decay=0.1,                 # Giữ nguyên mức phạt chống học vẹt
    warmup_ratio=0.1,
    load_best_model_at_end=True,
)

trainer_stage2 = CustomTrainerStage2(
    model=model_stage2,
    args=training_args_stage2,
    train_dataset=tokenized_train_combined,
    eval_dataset=tokenized_val, # Vẫn dùng tập Val cũ
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
)

print("Đang tinh chỉnh (Fine-tune) Giai đoạn 2...")
trainer_stage2.train()

# 6. Đánh giá trên tập TEST CŨ (10% Gold Test Set)
print("---")
print("Kết quả đánh giá GIAI ĐOẠN 2 trên tập Test cũ (Để chứng minh Data Augmentation Gain):")
test_results_stage2 = trainer_stage2.evaluate(eval_dataset=tokenized_test)
print(test_results_stage2)
```
*(Nếu F1-score ở Giai đoạn 2 cao hơn Giai đoạn 1, bạn đã có bằng chứng toán học tuyệt đối cho bài báo khoa học của mình!)*

---
**🎉 CHÚC MỪNG!** Bạn đã hoàn thành toàn bộ bước huấn luyện AI (Phase 0) trong đồ án. File `pseudo_labeled_5040.csv` tạo ra sẽ là input để kết hợp ngược lại với tập "Gold Label" dùng cho Phase 1 (Đặc trưng tuần & chuỗi thời gian).
