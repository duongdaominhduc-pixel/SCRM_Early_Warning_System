# P4-04 — Stationarity Tests

## Task
Run ADF and KPSS tests in parallel on weekly TTS_days and avg_delay series
to determine whether they are stationary before modelling.

## Script
`stationarity_test.py`

## Inputs
| File | Series used |
|------|------------|
| `P4-02\tts_weekly.parquet` | `mean_TTS_days` aggregated across all parts |
| `P4-03\delivery_delays_weekly.parquet` | `avg_delay` aggregated across all suppliers |

## Test Logic
| ADF p | KPSS p | Conclusion |
|-------|--------|------------|
| < 0.05 | > 0.05 | Stationary |
| > 0.05 | < 0.05 | Non-stationary |
| otherwise | otherwise | Ambiguous |

- ADF H0: unit root exists (non-stationary). Reject if p < 0.05.
- KPSS H0: series is stationary. Reject if p < 0.05 (i.e., keep if p > 0.05).

## Output
`P4-04\stationarity_results.csv`

Columns: `feature`, `ADF_stat`, `ADF_pvalue`, `ADF_conclusion`,
`KPSS_stat`, `KPSS_pvalue`, `KPSS_conclusion`, `Overall`

## Parallelism
Tests run via `concurrent.futures.ThreadPoolExecutor(max_workers=2)`.

## Status
DONE — scripts verified against real data.

## How to run
```
cd "D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001\P4-04"
py stationarity_test.py
```
