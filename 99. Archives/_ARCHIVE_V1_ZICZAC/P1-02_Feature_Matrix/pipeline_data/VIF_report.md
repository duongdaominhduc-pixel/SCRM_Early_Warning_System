# Multicollinearity Report (VIF)

Features with VIF > 5 should be considered for removal or Lasso penalization.

| feature                 |     VIF |
|:------------------------|--------:|
| risk_article_count_w1   | 1.64461 |
| risk_article_count_w2   | 1.62108 |
| high_risk_count_w2      | 1.4856  |
| high_risk_count_w1      | 1.468   |
| w1_avg_actual_lead_time | 1.44182 |
| geo_match_score_w2      | 1.39951 |
| geo_match_score_w1      | 1.38282 |
| w1_on_hand_inventory    | 1.33804 |
| w1_lead_time_ratio      | 1.13234 |
| w1_pct_po_late          | 1.12276 |