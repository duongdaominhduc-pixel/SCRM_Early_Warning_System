"""
babysit_training.py
Monitors resume_train_c1.py, auto-restarts if the process dies,
updates START_EPOCH + BEST_VAL_F1 from log each time.
Exits when P3-04/evaluation_report_C1.md appears (training fully done).
"""
import sys, time, re, subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE       = Path(r'D:\3. Research & Contest\BBKH_PAPA\drive-download-20260620T082012Z-3-001')
RESUME_PY  = BASE / 'P3-03' / 'resume_train_c1.py'
EVAL_DONE  = BASE / 'P3-04' / 'evaluation_report_C1.md'
LOG_FILE   = BASE / 'P3-03' / 'train_log_e4.txt'
ERR_FILE   = BASE / 'P3-03' / 'train_err_e4.txt'
CHECK_SEC  = 120   # check every 2 minutes

def log(msg):
    ts = time.strftime('%H:%M:%S')
    print(f"[{ts}] {msg}", flush=True)

def read_log_tail(n=60):
    if not LOG_FILE.exists():
        return ""
    lines = LOG_FILE.read_text(encoding='utf-8', errors='replace').splitlines()
    return "\n".join(lines[-n:])

def parse_best_from_log(text):
    """Return (last_completed_epoch, best_val_f1) from log text."""
    # Lines like: "Epoch 3/5 | train_loss=0.4354 | val_macro_f1=0.6599 [SAVED]"
    # or:         "Epoch 3 complete. val_macro_f1=0.6599"
    epochs_seen = []
    for m in re.finditer(
        r'Epoch\s+(\d+).*?val(?:_macro)?_f1[= ]+([0-9.]+)',
        text, re.IGNORECASE
    ):
        e, f = int(m.group(1)), float(m.group(2))
        epochs_seen.append((e, f))

    # Also look for BEST_VAL_F1 lines saved in log
    saved = re.findall(r'SAVED.*?f1[= ]+([0-9.]+)', text, re.IGNORECASE)

    if not epochs_seen:
        return None, None

    last_epoch = max(e for e, _ in epochs_seen)
    best_f1    = max(f for _, f in epochs_seen)
    return last_epoch, best_f1

def update_resume_script(start_epoch, best_f1):
    text = RESUME_PY.read_text(encoding='utf-8')
    text = re.sub(r'START_EPOCH\s*=\s*\d+', f'START_EPOCH = {start_epoch}', text)
    text = re.sub(r'BEST_VAL_F1\s*=\s*[0-9.]+', f'BEST_VAL_F1 = {best_f1}', text)
    # Also update docstring if present
    text = re.sub(
        r'(Resume fine-tuning.*?epoch\s*)\d+(.*?macro_f1=)[0-9.]+',
        rf'\g<1>{start_epoch-1}\g<2>{best_f1}',
        text, flags=re.IGNORECASE
    )
    RESUME_PY.write_text(text, encoding='utf-8')
    log(f"resume_train_c1.py updated → START_EPOCH={start_epoch}, BEST_VAL_F1={best_f1}")

def launch():
    proc = subprocess.Popen(
        [sys.executable, str(RESUME_PY)],
        stdout=open(LOG_FILE, 'a', encoding='utf-8'),
        stderr=open(ERR_FILE, 'a', encoding='utf-8'),
        cwd=str(BASE),
    )
    log(f"Training launched → PID {proc.pid}")
    return proc

# ── Main loop ─────────────────────────────────────────────────────────────────
log("=== babysit_training.py started ===")
log(f"Monitoring every {CHECK_SEC}s. Will exit when {EVAL_DONE.name} appears.")

proc = None
restarts = 0

while True:
    # 1. Check completion
    if EVAL_DONE.exists():
        log("evaluation_report_C1.md found — training COMPLETE!")
        log("=== babysit done ===")
        break

    # 2. Check if process is alive
    alive = proc is not None and proc.poll() is None

    if not alive:
        # Read log to determine where we left off
        tail = read_log_tail(100)
        last_epoch, best_f1 = parse_best_from_log(tail)

        if last_epoch is None:
            # No epochs logged yet — use defaults from script as-is
            log("No epoch data in log yet; launching with current script settings.")
        else:
            next_epoch = last_epoch + 1
            if next_epoch > 5:
                log(f"All epochs done (last={last_epoch}) but eval report missing — waiting 60s...")
                time.sleep(60)
                continue
            log(f"Process dead. Last epoch={last_epoch}, best_f1={best_f1:.4f}")
            update_resume_script(next_epoch, best_f1)

        restarts += 1
        log(f"Restart #{restarts}")
        proc = launch()

    else:
        # Still running — print last log line
        tail = read_log_tail(3)
        if tail.strip():
            for line in tail.strip().splitlines()[-1:]:
                log(f"  [log] {line}")
        else:
            log(f"  process alive (PID {proc.pid}), no output yet...")

    time.sleep(CHECK_SEC)
