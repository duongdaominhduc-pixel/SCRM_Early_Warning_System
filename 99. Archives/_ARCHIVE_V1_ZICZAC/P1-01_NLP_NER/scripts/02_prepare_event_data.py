import pandas as pd
from pathlib import Path

ROOT = Path(r"D:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH")
P1_01_DATA = ROOT / "P1-01_NLP_NER" / "pipeline_data"

def main():
    print("Đang nạp tập dữ liệu nền tảng (5,313 bài)...")
    df = pd.read_csv(P1_01_DATA / "combined_5313.csv")
    
    # Lọc ra các bài có rủi ro (Nhãn 1 và Nhãn 2)
    df_risk = df[df['final_label'].isin([1, 2])].copy()
    
    print(f"Số lượng bài báo rủi ro (Nhãn 1 + Nhãn 2): {len(df_risk)}")
    
    # Lưu lại để chuẩn bị cho Zero-Shot Labeling trên Colab
    out_path = P1_01_DATA / "event_classification_input_1791.csv"
    df_risk.to_csv(out_path, index=False, encoding='utf-8')
    
    print(f"Đã lưu tập dữ liệu {len(df_risk)} bài tại: {out_path}")
    print("Sẵn sàng mang lên Colab để chạy Zero-Shot Event Labeling và Fine-tune!")

if __name__ == "__main__":
    main()
