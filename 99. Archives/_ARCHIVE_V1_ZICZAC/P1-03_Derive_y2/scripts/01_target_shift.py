import pandas as pd
import os

def main():
    base_dir = r"d:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH"
    input_dir = os.path.join(base_dir, "P1-02_Feature_Matrix", "pipeline_data")
    output_dir = os.path.join(base_dir, "P1-03_Derive_y2", "pipeline_data")
    os.makedirs(output_dir, exist_ok=True)
    
    input_path = os.path.join(input_dir, "feature_matrix_weekly.parquet")
    print(f"Loading feature matrix from {input_path}...")
    df = pd.read_parquet(input_path)
    
    print(f"Initial shape: {df.shape}")
    
    # Sort the dataframe by part_id and week to ensure chronological order for shifting
    print("Sorting by part_id and week for Data Alignment...")
    df = df.sort_values(['part_id', 'week']).reset_index(drop=True)
    
    # We are using 'w1_stockout_flag' as the Operational Continuity Proxy
    # shift(-1) moves the next week's value to the current week
    print("Deriving targets: y2_shift1 (W+1) and y2_shift2 (W+2) [Lead-Time Advantage]...")
    for n in [1, 2]:
        df[f'y2_shift{n}'] = df.groupby('part_id')['w1_stockout_flag'].shift(-n)
        
    # Drop rows that are right-censored (the last 2 weeks for each part)
    print("Dropping right-censored terminal rows (Handling Data Alignment)...")
    df_train = df.dropna(subset=['y2_shift1', 'y2_shift2']).copy()
    
    print(f"Final shape after dropping NaNs: {df_train.shape}")
    
    # Verification: Check Positive Rate
    pos_rate_1 = df_train['y2_shift1'].mean() * 100
    pos_rate_2 = df_train['y2_shift2'].mean() * 100
    print(f"\nTarget Verification:")
    print(f"- y2_shift1 (W+1) Positive Rate: {pos_rate_1:.2f}%")
    print(f"- y2_shift2 (W+2) Positive Rate: {pos_rate_2:.2f}%")
    
    if pos_rate_1 < 1.0 or pos_rate_2 < 1.0:
        print("WARNING: Positive rate is extremely low. Class imbalance techniques (e.g. SMOTE or weighting) will be required.")
    
    # Visual check
    print("\nVisual Check for part_id P00001:")
    sample = df[df['part_id'] == 'P00001'][['week', 'w1_stockout_flag', 'y2_shift1', 'y2_shift2']].head(5)
    print(sample)
    
    # Save the final matrix
    output_path = os.path.join(output_dir, "feature_matrix_with_targets.parquet")
    df_train.to_parquet(output_path, index=False)
    print(f"\nSaved final training matrix to {output_path}")

if __name__ == "__main__":
    main()
