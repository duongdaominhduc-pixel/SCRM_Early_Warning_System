# -*- coding: utf-8 -*-
import re, sys

with open('0. project documents/SCRM_EWS_draft_article_v2.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')

# Title
title = re.sub(r'\*+', '', lines[0]).strip()
tw = title.split()
print(f"TITLE: {len(tw)} words (max 25)")
print(f"  UPPERCASE: {title == title.upper()}")
print(f"  BOLD: {'**' in lines[0]}")

# Abstract
m = re.search(r'Abstract\n\n(.+?)\n\n\*\*Keywords', text, re.DOTALL)
if m:
    aw = m.group(1).split()
    print(f"ABSTRACT: {len(aw)} words (req 150-200)")
else:
    print("ABSTRACT: pattern not found")

# Keywords
m2 = re.search(r'Keywords:\*\*\s*(.+?)(\n\n)', text, re.DOTALL)
if m2:
    kws = [k.strip() for k in m2.group(1).split(';') if k.strip()]
    print(f"KEYWORDS: {len(kws)} (req 3-5)")
else:
    print("KEYWORDS: pattern not found")

# Sections
for s in ['Introduction', 'Literature Review', 'Methodology', 'Results', 'Discussion', 'Conclusion', 'REFERENCES']:
    print(f"  {s}: {'OK' if s.lower() in text.lower() else 'MISSING'}")

# Body word count
b1 = text.find('## 1.')
b2 = text.find('## REFERENCES')
if b1 > 0 and b2 > 0:
    body = text[b1:b2]
    body = re.sub(r'!\[.*?\]\(.*?\)', '', body)
    body = re.sub(r'\|[^\n]*\|', '', body)
    body = re.sub(r'[#*_`]', '', body)
    body = re.sub(r'\$[^$]*\$', '', body)
    bw = body.split()
    print(f"BODY: {len(bw)} words (max 8000)")
