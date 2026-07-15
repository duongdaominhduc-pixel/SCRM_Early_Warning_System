import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
import re
import pandas as pd

BASE = Path(r'/Users/lelinh/Documents/BBKH')

# ---------------------------------------------------------------------------
# Keyword definitions for each disruption category
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS = {
    'PORT_CONGESTION': [
        'port congestion', 'terminal congestion', 'berth delay', 'vessel delay',
        'shipping backlog', 'dock congestion', 'port backup', 'port delay',
        'container backlog', 'terminal backup', 'port closure',
        'port', 'terminal', 'congestion', 'dock', 'berth',
    ],
    'GEOPOLITICAL': [
        'export control', 'import restriction', 'trade war', 'trade dispute',
        'geopolitical risk', 'geopolitical tension',
        'sanction', 'tariff', 'embargo', 'ban', 'geopolitical',
    ],
    'WEATHER_DISASTER': [
        'natural disaster', 'hurricane', 'typhoon', 'flood', 'earthquake',
        'storm', 'wildfire', 'drought', 'tsunami', 'tornado', 'cyclone',
        'blizzard', 'mudslide', 'landslide',
    ],
    'LABOR_DISPUTE': [
        'labor dispute', 'labour dispute', 'worker protest', 'worker strike',
        'union strike', 'industrial action',
        'strike', 'walkout', 'lockout', 'union', 'shutdown',
    ],
    'SUPPLIER_FINANCIAL': [
        'chapter 11', 'financial distress', 'financial crisis',
        'bankruptcy', 'insolvency', 'liquidation', 'default', 'restructuring',
    ],
}

# Ordered by specificity — multi-word phrases first, then single words
# Already ordered above (longer phrases at the beginning of each list)


def _count_keyword_hits(text: str, keywords: list) -> int:
    """Count how many distinct keywords appear in the lowercased text."""
    text_lower = text.lower()
    hits = 0
    for kw in keywords:
        # Use word-boundary match to avoid false positives
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text_lower):
            hits += 1
    return hits


def _best_category(scores: dict) -> str:
    """Return the category with the highest score, or GENERAL_DISRUPTION on tie/zero."""
    if not scores:
        return 'GENERAL_DISRUPTION'
    max_score = max(scores.values())
    if max_score == 0:
        return 'GENERAL_DISRUPTION'
    winners = [cat for cat, score in scores.items() if score == max_score]
    if len(winners) == 1:
        return winners[0]
    # Tie → GENERAL_DISRUPTION
    return 'GENERAL_DISRUPTION'


def classify_disruption_type(title: str, content: str) -> str:
    """
    Classify an article into one of 6 disruption categories using keyword rules.

    Priority:
      1. If title alone matches exactly one category → return that category.
      2. Combine title (weight=3) + content (weight=1) keyword scores → pick winner.
      3. If tie or no match → GENERAL_DISRUPTION.

    Parameters
    ----------
    title : str
        Article headline / title text.
    content : str
        Article body text (cleaned_content).

    Returns
    -------
    str
        One of: PORT_CONGESTION, GEOPOLITICAL, WEATHER_DISASTER,
                LABOR_DISPUTE, SUPPLIER_FINANCIAL, GENERAL_DISRUPTION
    """
    title = title or ''
    content = content or ''

    # Step 1: title-only scan
    title_scores = {
        cat: _count_keyword_hits(title, kws)
        for cat, kws in CATEGORY_KEYWORDS.items()
    }
    title_nonzero = {cat: s for cat, s in title_scores.items() if s > 0}

    if len(title_nonzero) == 1:
        # Unambiguous title match
        return list(title_nonzero.keys())[0]

    if len(title_nonzero) > 1:
        # Multiple title categories — see if one dominates clearly
        max_title = max(title_nonzero.values())
        title_winners = [c for c, s in title_nonzero.items() if s == max_title]
        if len(title_winners) == 1:
            return title_winners[0]

    # Step 2: Weighted combined score (title weight=3, content weight=1)
    combined_scores = {}
    for cat, kws in CATEGORY_KEYWORDS.items():
        t_hits = _count_keyword_hits(title, kws)
        c_hits = _count_keyword_hits(content, kws)
        combined_scores[cat] = t_hits * 3 + c_hits

    return _best_category(combined_scores)


# ---------------------------------------------------------------------------
# Main: apply to P2-06 CSVs and save results
# ---------------------------------------------------------------------------

def process_csv(src_path: Path, dst_path: Path) -> pd.Series:
    """Load a CSV, apply classifier, save to dst_path, return distribution."""
    df = pd.read_csv(src_path)
    df['disruption_type'] = df.apply(
        lambda row: classify_disruption_type(
            str(row.get('title', '') or ''),
            str(row.get('cleaned_content', '') or ''),
        ),
        axis=1,
    )
    df.to_csv(dst_path, index=False, encoding='utf-8')
    return df['disruption_type'].value_counts()


def main():
    out_dir = BASE / 'P3-08'
    out_dir.mkdir(exist_ok=True)

    splits = ['train', 'val', 'test']
    for split in splits:
        src = BASE / 'P2-06' / f'{split}.csv'
        dst = out_dir / f'{split}_with_disruption_type.csv'
        print(f'\n--- {split.upper()} ({src.name}) ---')
        dist = process_csv(src, dst)
        print(dist.to_string())
        print(f'Saved → {dst}')


if __name__ == '__main__':
    main()
