import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import precision_score, recall_score, f1_score, fbeta_score
import xgboost as xgb
import json
import warnings
warnings.filterwarnings('ignore')

def load_data():
    base_dir = r"d:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH"
    targets_dir = os.path.join(base_dir, "P1-03_Derive_y2", "pipeline_data")
    nlp_dir = os.path.join(base_dir, "P1-04_Geo_Join", "pipeline_data")
    
    df_ops = pd.read_parquet(os.path.join(targets_dir, "feature_matrix_with_targets.parquet"))
    df_nlp = pd.read_parquet(os.path.join(nlp_dir, "news_supplier_joined.parquet"))
    
    nlp_agg = df_nlp.groupby(['date_week', 'part_id'])['weighted_risk_score'].sum().reset_index()
    nlp_agg.rename(columns={'weighted_risk_score': 'nlp_risk_score'}, inplace=True)
    
    df_merged = pd.merge(df_ops, nlp_agg, left_on=['week', 'part_id'], right_on=['date_week', 'part_id'], how='left')
    df_merged['nlp_risk_score'] = df_merged['nlp_risk_score'].fillna(0)
    
    df_merged = df_merged.sort_values(by=['week', 'part_id']).reset_index(drop=True)
    return df_merged

def main():
    print("Loading datasets...")
    df = load_data()
    
    base_dir = r"d:\3. Research & Contest\BBKH_PAPA\BBKH\BBKH"
    out_dir = os.path.join(base_dir, "P2-01_Threshold", "results")
    os.makedirs(out_dir, exist_ok=True)
    
    exclude_cols = ['part_id', 'week', 'w1_stockout_flag', 'w2_stockout_flag', 'y2_shift1', 'y2_shift2', 'date_week', 'dominant_event_type_w1', 'dominant_event_type_w2']
    baseline_features = [c for c in df.columns if c not in exclude_cols and c != 'nlp_risk_score']
    features = baseline_features + ['nlp_risk_score']
    
    targets = ['y2_shift1', 'y2_shift2']
    results_summary = {}
    
    for target in targets:
        print(f"\n--- Threshold Optimization for Target: {target} ---")
        df_target = df.dropna(subset=[target]).copy()
        
        X = df_target[features]
        y = df_target[target].astype(int)
        
        positive_rate = y.mean()
        scale_pos_weight = (len(y) - y.sum()) / y.sum()
        
        print(f"Positive Rate: {positive_rate:.4f}")
        
        model = xgb.XGBClassifier(
            scale_pos_weight=scale_pos_weight, 
            random_state=42,
            eval_metric='logloss',
            use_label_encoder=False
        )
        
        tscv = TimeSeriesSplit(n_splits=5, gap=2)
        
        y_true_all = []
        y_prob_all = []
        
        for train_index, test_index in tscv.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]
            
            model.fit(X_train, y_train)
            probs = model.predict_proba(X_test)[:, 1]
            
            y_true_all.extend(y_test.values)
            y_prob_all.extend(probs)
            
        y_true_all = np.array(y_true_all)
        y_prob_all = np.array(y_prob_all)
        
        thresholds = np.arange(0.05, 0.96, 0.05)
        
        records = []
        for t in thresholds:
            y_pred_t = (y_prob_all >= t).astype(int)
            prec = precision_score(y_true_all, y_pred_t, zero_division=0)
            rec = recall_score(y_true_all, y_pred_t, zero_division=0)
            f1 = f1_score(y_true_all, y_pred_t, zero_division=0)
            f05 = fbeta_score(y_true_all, y_pred_t, beta=0.5, zero_division=0)
            records.append({'Threshold': round(t, 2), 'Precision': prec, 'Recall': rec, 'F1': f1, 'F0.5': f05})
            
        df_thresh = pd.DataFrame(records)
        
        plt.figure(figsize=(10, 6))
        plt.plot(df_thresh['Threshold'], df_thresh['Precision'], label='Precision (Tránh Báo động giả)', color='blue', linewidth=2)
        plt.plot(df_thresh['Threshold'], df_thresh['Recall'], label='Recall (Bắt Đứt gãy)', color='red', linewidth=2)
        plt.plot(df_thresh['Threshold'], df_thresh['F1'], label='F1-Score (Cân bằng)', color='green', linewidth=2, linestyle='--')
        plt.plot(df_thresh['Threshold'], df_thresh['F0.5'], label='F0.5-Score (Thiên về Precision)', color='purple', linewidth=2, linestyle='-.')
        
        best_row = df_thresh.loc[df_thresh['F1'].idxmax()]
        best_t = best_row['Threshold']
        
        plt.axvline(x=best_t, color='black', linestyle=':', label=f'Managerial Sweet Spot (T={best_t:.2f})')
        
        plt.title(f'Threshold Sensitivity Analysis (Target: {target})\nCân bằng giữa Alert Fatigue và Risk Catching', fontsize=14, fontweight='bold')
        plt.xlabel('Decision Threshold (Ngưỡng cảnh báo)', fontsize=12)
        plt.ylabel('Score (Điểm)', fontsize=12)
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plot_path = os.path.join(out_dir, f'threshold_tuning_{target}.png')
        plt.savefig(plot_path)
        plt.close()
        
        print(f"Plot saved to {plot_path}")
        print(f"Optimal Threshold (Max F1): {best_t:.2f} (Precision: {best_row['Precision']:.3f}, Recall: {best_row['Recall']:.3f})")
        
        results_summary[target] = {
            'optimal_threshold': float(best_t),
            'precision': float(best_row['Precision']),
            'recall': float(best_row['Recall']),
            'f1_score': float(best_row['F1']),
            'f0.5_score': float(best_row['F0.5'])
        }
        
        df_thresh.to_csv(os.path.join(out_dir, f'threshold_metrics_{target}.csv'), index=False)
        
    with open(os.path.join(out_dir, 'optimal_thresholds.json'), 'w') as f:
        json.dump(results_summary, f, indent=4)
        
    print("\nOptimization complete. Results saved to JSON.")

if __name__ == "__main__":
    main()
