import pandas as pd
import spacy
from pathlib import Path

ROOT = Path(r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH")
P1_01_DATA = ROOT / "P1-01_NLP_NER" / "pipeline_data"

def main():
    print("Đang nạp mô hình spaCy...")
    try:
        # Thử nạp mô hình nhỏ để test nhanh trên local
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Chưa có mô hình spaCy. Hãy chạy: python -m spacy download en_core_web_sm")
        return

    df = pd.read_csv(P1_01_DATA / "combined_5313.csv", nrows=50) # Chỉ test 50 bài đầu
    print("Đã nạp 50 bài báo đầu tiên để test NER.\n")
    
    for idx, row in df.iterrows():
        title = row['title']
        content = str(row['content'])
        
        # Lấy 500 ký tự đầu của content để test cho nhanh
        text_to_process = f"{title}. {content[:500]}..."
        
        doc = nlp(text_to_process)
        
        orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
        gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        events = [ent.text for ent in doc.ents if ent.label_ == "EVENT"]
        
        print(f"--- Bài {idx + 1} ---")
        print(f"Tiêu đề: {title}")
        print(f"🏢 Tổ chức/Công ty (ORG): {', '.join(set(orgs)) if orgs else 'Không có'}")
        print(f"🌍 Quốc gia/Địa điểm (GPE): {', '.join(set(gpes)) if gpes else 'Không có'}")
        print(f"📅 Thời gian (DATE): {', '.join(set(dates)) if dates else 'Không có'}")
        print(f"🔥 Sự kiện (EVENT): {', '.join(set(events)) if events else 'Không có'}")
        print("-" * 50)
        
        if idx >= 4: # Chỉ in ra 5 bài để xem lướt
            break
            
    print("\n✅ Test NER Tầng 1 thành công! Trên Colab chúng ta sẽ dùng mô hình en_core_web_trf (Transformer) để chính xác hơn và chạy trên toàn bộ 5,313 bài.")

if __name__ == "__main__":
    main()
