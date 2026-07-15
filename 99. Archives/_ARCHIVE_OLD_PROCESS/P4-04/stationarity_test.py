import sys
sys.stdout.reconfigure(encoding='utf-8')

import subprocess
from pathlib import Path

BASE = Path(r'/Users/lelinh/Documents/BBKH')
TTS_FILE = BASE / 'P4-02' / 'tts_weekly.parquet'
DELAYS_FILE = BASE / 'P4-03' / 'delivery_delays_weekly.parquet'
OUT_DIR = BASE / 'P4-04'
OUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Ensure dependencies
# ---------------------------------------------------------------------------
try:
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.stattools import adfuller, kpss
    import pyarrow  # noqa: F401
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'pyarrow', 'numpy', 'statsmodels'])
    import pandas as pd
    import numpy as np
    from statsmodels.tsa.stattools import adfuller, kpss

from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Loading parquet files ...")
tts = pd.read_parquet(TTS_FILE)
delays = pd.read_parquet(DELAYS_FILE)

# ---------------------------------------------------------------------------
# Build weekly time series aggregated across all parts / suppliers
# ---------------------------------------------------------------------------

# TTS: aggregate mean_TTS_days across all (part_id, site_id) per week
tts_ts = (
    tts.groupby('week')['mean_TTS_days']
    .mean()
    .dropna()
    .sort_index()
    .values
)

# Delays: aggregate avg_delay across all (supplier_id, part_id) per week
delays_ts = (
    delays.groupby('week_of_promised_date')['avg_delay']
    .mean()
    .dropna()
    .sort_index()
    .values
)

print(f"  TTS series length: {len(tts_ts)}")
print(f"  Delays series length: {len(delays_ts)}")

# ---------------------------------------------------------------------------
# Run ADF + KPSS in parallel
# ---------------------------------------------------------------------------

def run_tests(name: str, series: 'np.ndarray'):
    """Returns dict with ADF and KPSS results."""
    adf_result = adfuller(series, autolag='AIC')
    adf_stat = adf_result[0]
    adf_pvalue = adf_result[1]

    # KPSS — nlags='auto' avoids deprecation warning
    try:
        kpss_result = kpss(series, regression='c', nlags='auto')
    except Exception:
        kpss_result = kpss(series, regression='c')
    kpss_stat = kpss_result[0]
    kpss_pvalue = kpss_result[1]

    # Interpret
    adf_stationary = adf_pvalue < 0.05
    kpss_stationary = kpss_pvalue > 0.05  # high p → fail to reject H0 (stationary)

    if adf_stationary and kpss_stationary:
        overall = 'Stationary'
    elif (not adf_stationary) and (not kpss_stationary):
        overall = 'Non-stationary'
    else:
        overall = 'Ambiguous'

    return {
        'feature': name,
        'ADF_stat': round(adf_stat, 4),
        'ADF_pvalue': round(adf_pvalue, 4),
        'ADF_conclusion': 'Stationary' if adf_stationary else 'Non-stationary',
        'KPSS_stat': round(kpss_stat, 4),
        'KPSS_pvalue': round(kpss_pvalue, 4),
        'KPSS_conclusion': 'Stationary' if kpss_stationary else 'Non-stationary',
        'Overall': overall,
    }

tasks = [
    ('TTS_days (all parts)', tts_ts),
    ('avg_delay (all suppliers)', delays_ts),
]

print("\nRunning ADF + KPSS tests in parallel ...")

with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {executor.submit(run_tests, name, series): name for name, series in tasks}
    results = []
    for future in futures:
        results.append(future.result())

results.sort(key=lambda r: r['feature'])

# ---------------------------------------------------------------------------
# Print result table
# ---------------------------------------------------------------------------
print("\n=== Stationarity Test Results ===")
header = f"{'Feature':<35} {'ADF p':>9} {'ADF concl':>15} {'KPSS stat':>10} {'KPSS concl':>14} {'Overall':>14}"
print(header)
print('-' * len(header))
for r in results:
    print(
        f"{r['feature']:<35} {r['ADF_pvalue']:>9.4f} {r['ADF_conclusion']:>15} "
        f"{r['KPSS_stat']:>10.4f} {r['KPSS_conclusion']:>14} {r['Overall']:>14}"
    )

# ---------------------------------------------------------------------------
# Save CSV
# ---------------------------------------------------------------------------
import csv

OUT_FILE = OUT_DIR / 'stationarity_results.csv'
fieldnames = ['feature', 'ADF_stat', 'ADF_pvalue', 'ADF_conclusion',
              'KPSS_stat', 'KPSS_pvalue', 'KPSS_conclusion', 'Overall']

with open(OUT_FILE, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"\nSaved: {OUT_FILE}")
print("=== DONE ===")
