import os
import json
import torch
import hashlib
import pandas as pd
from tqdm import tqdm
import spacy
import pycountry
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN
# ==========================================
MODEL_PATH = "./P3-03/best_model_c1"
DATA_PATH = "./0. news data/final_supplychain_news_2015_2018.jsonl"
OUTPUT_DIR = "./P3-10"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "structured_risk_events.csv")

# ==========================================
# 1. HÀM PHỤ TRỢ
# ==========================================
def get_device():
    if torch.backends.mps.is_available():
        return torch.device("mps")
    elif torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")

def get_country_code(country_name):
    custom_map = {"US": "US", "UK": "GB", "USA": "US", "Vietnam": "VN", "South Korea": "KR", "Russia": "RU"}
    if country_name in custom_map: return custom_map[country_name]
    try:
        return pycountry.countries.search_fuzzy(country_name)[0].alpha_2
    except:
        return None

def classify_disruption_type(text):
    text = str(text).lower()
    if any(word in text for word in ["port", "congestion", "vessel", "container", "shipping"]): return "PORT_CONGESTION"
    elif any(word in text for word in ["strike", "labor", "union", "worker"]): return "LABOR_STRIKE"
    elif any(word in text for word in ["weather", "hurricane", "storm", "flood", "typhoon", "earthquake"]): return "WEATHER_EVENT"
    elif any(word in text for word in ["war", "conflict", "tariff", "sanction", "geopolitical"]): return "GEOPOLITICAL"
    elif any(word in text for word in ["bankrupt", "financial", "insolvency"]): return "SUPPLIER_FINANCIAL"
    else: return "GENERAL_DISRUPTION"

# ==========================================
# 2. CHƯƠNG TRÌNH CHÍNH
# ==========================================
def main():
    print("⏳ Đang tải AI Model (DistilBERT) và SpaCy... Vui lòng đợi!")
    device = get_device()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH).to(device)
    model.eval()
    nlp = spacy.load("en_core_web_sm")

    articles = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            try: articles.append(json.loads(line.strip()))
            except: continue
    
    results = []
    for idx, article in enumerate(tqdm(articles)):
        title = article.get("title", "")
        content = article.get("content", "")
        url = article.get("url", f"unknown_url_{idx}")
        publish_date = article.get("publish_date", "1970-01-01")

        text_input = f"{title} [SEP] {content}"
        inputs = tokenizer(text_input, padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_label = torch.argmax(probs, dim=1).item()
            predicted_prob = probs[0][predicted_label].item()

        if predicted_label == 0:
            continue

        disruption_type = classify_disruption_type(title + " " + content)

        # ---------------------------------------------------------
        # TÍNH TOÁN SEVERITY SCORE THÔNG MINH (TRICK XỬ LÝ MẤT CÂN BẰNG)
        # ---------------------------------------------------------
        # 1. Điểm cơ bản (Label 1 = 5, Label 2 = 9)
        severity_score = 9 if predicted_label == 2 else 5
        
        if predicted_label == 1:
            # 2. Bonus độ tự tin: Tự tin càng cao (gần 1.0) cộng càng nhiều điểm
            # Ví dụ: Prob = 0.9 -> Bonus = 4 điểm -> Tổng 9
            confidence_bonus = int((predicted_prob - 0.5) * 10) 
            severity_score += max(0, confidence_bonus)
            
            # 3. Bonus mức độ nghiêm trọng của phân loại rủi ro
            if disruption_type in ["GEOPOLITICAL", "SUPPLIER_FINANCIAL", "WEATHER_EVENT"]:
                severity_score += 2

        # Đảm bảo điểm không vượt quá 10 và không dưới 1
        severity_score = max(1, min(10, severity_score))
        # ---------------------------------------------------------

        doc = nlp(title + ". " + content[:2000])
        location_entities = []
        for ent in doc.ents:
            if ent.label_ == "GPE":
                code = get_country_code(ent.text)
                if code and code not in location_entities: location_entities.append(code)
        
        iso_list_str = ",".join(location_entities) if location_entities else "UNKNOWN"
        event_id = hashlib.md5(f"{url}_{publish_date}".encode()).hexdigest()[:10]

        results.append({
            "event_id": event_id,
            "publish_date": publish_date,
            "disruption_type": disruption_type,
            "location_entities": iso_list_str,
            "severity_score": severity_score,
            "predicted_label": predicted_label,
            "predicted_probability": round(predicted_prob, 4)
        })

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"🎉 HOÀN THÀNH! Đã lưu file tại: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()