# P4-02 — Time-to-Survive (TTS) Computation

## Task
Compute daily burn rate via a rolling 4-week window, derive TTS_days per
(part_id, site_id), then aggregate to weekly granularity.

## Script
`compute_tts.py`

## Input
`P4-01\supply_chain_history.parquet`

## Key Metrics
| Column | Formula |
|--------|---------|
| `burn_rate_daily` | rolling 4-week mean of `consumption_qty` / 7 |
| `TTS_days` | `on_hand_qty / burn_rate_daily` (NaN when burn_rate == 0) |

## Output
`P4-02\tts_weekly.parquet`

Columns: `part_id`, `site_id`, `week`, `mean_TTS_days`, `mean_burn_rate_daily`,
`on_hand_qty_mean`, `rows`

## Status
DONE — scripts verified against real data.

## How to run
```
cd "D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001\P4-02"
py compute_tts.py
```
