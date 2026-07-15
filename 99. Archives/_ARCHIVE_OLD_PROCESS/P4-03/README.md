# P4-03 — Delivery Delay Computation

## Task
Compute per-PO delivery delay, flag late deliveries, and aggregate to weekly
granularity per (supplier_id, part_id, week_of_promised_date).

## Script
`compute_delays.py`

## Input
`P4-01\purchase_orders.parquet`

## Key Metrics
| Column | Formula |
|--------|---------|
| `delivery_delay_days` | `(receipt_date - promised_date).dt.days` (positive = late) |
| `is_late` | 1 if `delivery_delay_days > 0` else 0 |

## Output
`P4-03\delivery_delays_weekly.parquet`

Columns: `supplier_id`, `part_id`, `week_of_promised_date`, `avg_delay`,
`pct_late`, `order_count`, `total_ordered_qty`, `total_received_qty`

## Status
DONE — scripts verified against real data.

## How to run
```
cd "D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001\P4-03"
py compute_delays.py
```
