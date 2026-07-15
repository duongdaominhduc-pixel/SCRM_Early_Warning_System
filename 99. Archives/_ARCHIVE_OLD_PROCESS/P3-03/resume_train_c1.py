"""
Resume fine-tuning từ best_model_c1 checkpoint (epoch 3, macro_f1=0.6599)
Tiếp tục train epoch 4-5, early stopping patience=3
"""

import sys, json, random
import numpy as np
import pandas as pd
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE   = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')
P2_DIR = BASE / 'P2-06'
P3_DIR = BASE / 'P3-03'

SEED = 42
random.seed(SEED); np.random.seed(SEED)

import torch
from torch.utils.data import Dataset, DataLoader
from torch import nn
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    get_linear_schedule_with_warmup,
)
from sklearn.metrics import classification_report, confusion_matrix, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {DEVICE}")

# ── Config ────────────────────────────────────────────────────────────────────
CHECKPOINT  = str(P3_DIR / 'best_model_c1')
MAX_LEN     = 512
BATCH_TRAIN = 16
BATCH_EVAL  = 32
LR          = 2e-5
START_EPOCH = 5       # resume từ epoch 4
MAX_EPOCHS  = 4
PATIENCE    = 3
BEST_VAL_F1 = 0.6686  # kết quả epoch 4

# ── Load data ─────────────────────────────────────────────────────────────────
print("Loading data...")
train_df = pd.read_csv(P2_DIR / 'train.csv')
val_df   = pd.read_csv(P2_DIR / 'val.csv')
test_df  = pd.read_csv(P2_DIR / 'test.csv')

label2_rows = train_df[train_df['label'] == 2]
factor = max(1, 25 // len(label2_rows))
oversampled = pd.concat([label2_rows] * factor, ignore_index=True)
train_df = pd.concat([train_df, oversampled], ignore_index=True).sample(
    frac=1, random_state=SEED).reset_index(drop=True)
print(f"Train after oversample: {dict(train_df['label'].value_counts().sort_index())}")

def make_text(row):
    return str(row.get('title','') or '').strip() + ' [SEP] ' + str(row.get('cleaned_content','') or '').strip()

train_texts = [make_text(r) for _, r in train_df.iterrows()]
val_texts   = [make_text(r) for _, r in val_df.iterrows()]
test_texts  = [make_text(r) for _, r in test_df.iterrows()]

# ── Tokenize ──────────────────────────────────────────────────────────────────
print(f"Loading tokenizer from checkpoint: {CHECKPOINT}")
tokenizer = DistilBertTokenizerFast.from_pretrained(CHECKPOINT)

class NewsDataset(Dataset):
    def __init__(self, texts, labels):
        self.encodings = tokenizer(texts, truncation=True, padding='max_length',
                                   max_length=MAX_LEN, return_tensors='pt')
        self.labels = torch.tensor(labels, dtype=torch.long)
    def __len__(self): return len(self.labels)
    def __getitem__(self, idx):
        return {'input_ids': self.encodings['input_ids'][idx],
                'attention_mask': self.encodings['attention_mask'][idx],
                'labels': self.labels[idx]}

print("Tokenizing...")
train_ds = NewsDataset(train_texts, train_df['label'].tolist())
val_ds   = NewsDataset(val_texts,   val_df['label'].tolist())
test_ds  = NewsDataset(test_texts,  test_df['label'].tolist())

train_loader = DataLoader(train_ds, batch_size=BATCH_TRAIN, shuffle=True)
val_loader   = DataLoader(val_ds,   batch_size=BATCH_EVAL,  shuffle=False)
test_loader  = DataLoader(test_ds,  batch_size=BATCH_EVAL,  shuffle=False)

# ── Load model từ checkpoint ──────────────────────────────────────────────────
print(f"Loading model from checkpoint: {CHECKPOINT}")
model = DistilBertForSequenceClassification.from_pretrained(CHECKPOINT).to(DEVICE)

orig_labels = pd.read_csv(P2_DIR / 'train.csv')['label'].tolist()
cw = compute_class_weight('balanced', classes=np.array([0,1,2]), y=orig_labels)
class_weights = torch.tensor(cw, dtype=torch.float).to(DEVICE)
print(f"Class weights: {cw.round(3)}")

loss_fn   = nn.CrossEntropyLoss(weight=class_weights)
optimizer = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)

remaining_epochs = MAX_EPOCHS - START_EPOCH + 1
total_steps = len(train_loader) * remaining_epochs
scheduler = get_linear_schedule_with_warmup(optimizer,
    num_warmup_steps=0, num_training_steps=total_steps)

# ── Eval helper ───────────────────────────────────────────────────────────────
def eval_model(loader, split_name):
    model.eval()
    all_preds, all_labels, all_probs = [], [], []
    total_loss = 0
    with torch.no_grad():
        for batch in loader:
            ids  = batch['input_ids'].to(DEVICE)
            mask = batch['attention_mask'].to(DEVICE)
            lbls = batch['labels'].to(DEVICE)
            out  = model(input_ids=ids, attention_mask=mask)
            loss = loss_fn(out.logits, lbls)
            total_loss += loss.item()
            probs = torch.softmax(out.logits, dim=1).cpu().numpy()
            all_preds.extend(np.argmax(probs, axis=1).tolist())
            all_labels.extend(lbls.cpu().tolist())
            all_probs.extend(probs.tolist())
    avg_loss    = total_loss / len(loader)
    macro_f1    = f1_score(all_labels, all_preds, average='macro',    zero_division=0)
    weighted_f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
    print(f"  {split_name}: loss={avg_loss:.4f}  macro_f1={macro_f1:.4f}  weighted_f1={weighted_f1:.4f}")
    return avg_loss, macro_f1, weighted_f1, all_preds, all_labels, all_probs

# ── Resume training loop ──────────────────────────────────────────────────────
print(f"\nResuming from epoch {START_EPOCH} (best so far: macro_f1={BEST_VAL_F1})")
best_val_f1 = BEST_VAL_F1
best_epoch  = START_EPOCH - 1
no_improve  = 0
history     = []

for epoch in range(START_EPOCH, MAX_EPOCHS + 1):
    model.train()
    total_train_loss = 0
    for i, batch in enumerate(train_loader):
        ids  = batch['input_ids'].to(DEVICE)
        mask = batch['attention_mask'].to(DEVICE)
        lbls = batch['labels'].to(DEVICE)
        optimizer.zero_grad()
        out  = model(input_ids=ids, attention_mask=mask)
        loss = loss_fn(out.logits, lbls)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        total_train_loss += loss.item()
        if (i+1) % 10 == 0:
            print(f"  step {i+1}/{len(train_loader)}  loss={loss.item():.4f}", flush=True)
    avg_train = total_train_loss / len(train_loader)
    print(f"\nEpoch {epoch}/{MAX_EPOCHS}  train_loss={avg_train:.4f}", flush=True)

    _, val_f1, val_wf1, _, _, _ = eval_model(val_loader, 'val')
    history.append({'epoch': epoch, 'train_loss': avg_train,
                    'val_macro_f1': val_f1, 'val_weighted_f1': val_wf1})

    if val_f1 > best_val_f1:
        best_val_f1 = val_f1
        best_epoch  = epoch
        no_improve  = 0
        model.save_pretrained(str(P3_DIR / 'best_model_c1'))
        tokenizer.save_pretrained(str(P3_DIR / 'best_model_c1'))
        print(f"  New best (macro_f1={val_f1:.4f}) — checkpoint saved", flush=True)
    else:
        no_improve += 1
        print(f"  No improvement ({no_improve}/{PATIENCE})", flush=True)
        if no_improve >= PATIENCE:
            print(f"  Early stopping at epoch {epoch}")
            break

print(f"\nBest val macro_f1={best_val_f1:.4f} at epoch {best_epoch}")

# ── Test evaluation ───────────────────────────────────────────────────────────
print("\n--- Test set evaluation ---")
best_model = DistilBertForSequenceClassification.from_pretrained(
    str(P3_DIR / 'best_model_c1')).to(DEVICE)
_, _, _, all_preds, all_labels, all_probs = eval_model(test_loader, 'test')

print(classification_report(all_labels, all_preds,
    labels=[0, 1, 2],
    target_names=['SAFE(0)','LOW_RISK(1)','HIGH_RISK(2)'], zero_division=0))

macro_f1    = f1_score(all_labels, all_preds, average='macro',    zero_division=0)
weighted_f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
cm = confusion_matrix(all_labels, all_preds)
print(f"Confusion matrix:\n{cm}")

try:
    auc = roc_auc_score(all_labels, np.array(all_probs), multi_class='ovr', average='macro')
    print(f"AUC-ROC={auc:.4f}")
except Exception as e:
    print(f"AUC skipped: {e}"); auc = None

# ── Save reports ──────────────────────────────────────────────────────────────
eval_out = BASE / 'P3-04'
eval_out.mkdir(exist_ok=True)

report_dict = classification_report(all_labels, all_preds,
    labels=[0, 1, 2],
    target_names=['SAFE(0)','LOW_RISK(1)','HIGH_RISK(2)'], zero_division=0, output_dict=True)

with open(eval_out / 'evaluation_report_C1.md', 'w', encoding='utf-8') as f:
    f.write("# Evaluation Report — Classifier C1 (DistilBERT)\n\n")
    f.write(f"**Best checkpoint:** Epoch {best_epoch} (val macro_f1={best_val_f1:.4f})\n")
    f.write(f"**Config:** lr={LR}, batch={BATCH_TRAIN}, max_len={MAX_LEN}, class_weight=balanced, Label2 oversample {factor}x\n\n")
    f.write("## Test Set Results\n\n| Metric | Value |\n|---|---|\n")
    f.write(f"| Macro F1 | {macro_f1:.4f} |\n| Weighted F1 | {weighted_f1:.4f} |\n")
    if auc: f.write(f"| AUC-ROC (macro OvR) | {auc:.4f} |\n")
    f.write("\n## Per-class F1\n\n| Class | Precision | Recall | F1 | Support |\n|---|---|---|---|---|\n")
    for cls in ['SAFE(0)','LOW_RISK(1)','HIGH_RISK(2)']:
        if cls in report_dict:
            r = report_dict[cls]
            f.write(f"| {cls} | {r['precision']:.3f} | {r['recall']:.3f} | {r['f1-score']:.3f} | {r['support']} |\n")
    f.write(f"\n## Confusion Matrix\n\n```\n{cm}\n```\n\n")
    f.write("## Training History\n\n| Epoch | Train Loss | Val Macro F1 | Val Weighted F1 |\n|---|---|---|---|\n")
    prev = [{'epoch':1,'train_loss':1.0189,'val_macro_f1':0.2828,'val_weighted_f1':0.5818},
            {'epoch':2,'train_loss':0.6270,'val_macro_f1':0.5749,'val_weighted_f1':0.6741}]
    for h in prev + history:
        f.write(f"| {h['epoch']} | {h['train_loss']:.4f} | {h['val_macro_f1']:.4f} | {h['val_weighted_f1']:.4f} |\n")

pred_df = test_df.copy()
pred_df['pred_label'] = all_preds
pred_df['prob_0'] = [p[0] for p in all_probs]
pred_df['prob_1'] = [p[1] for p in all_probs]
pred_df['prob_2'] = [p[2] for p in all_probs]
pred_df.to_csv(eval_out / 'test_predictions.csv', index=False, encoding='utf-8-sig')

with open(P3_DIR / 'training_history.json', 'w') as f:
    json.dump({'history': prev + history, 'best_epoch': best_epoch,
               'best_val_macro_f1': best_val_f1, 'test_macro_f1': macro_f1,
               'test_weighted_f1': weighted_f1}, f, indent=2)

print("\nDone. Outputs saved to P3-04/")
