#!/usr/bin/env python3
import os
import re
import html
import pandas as pd
import csv

# -------------------------------
# 1) Load FULL AIDev tables
# -------------------------------
def read_first_available(paths):
    last_err = None
    for p in paths:
        try:
            return pd.read_parquet(p)
        except Exception as e:
            last_err = e
    raise last_err

PR_PATHS = [
    "hf://datasets/hao-li/AIDev/all_pull_request.parquet",
    "hf://datasets/hao-li/AIDev/pull_request.parquet",
]
REPO_PATHS = [
    "hf://datasets/hao-li/AIDev/all_repository.parquet",
    "hf://datasets/hao-li/AIDev/repository.parquet",
]

pr_df = read_first_available(PR_PATHS)
repo_df = read_first_available(REPO_PATHS)

print(f"Loaded PRs: {len(pr_df):,}")
print(f"Loaded repos: {len(repo_df):,}")

# -------------------------------
# 2) Merge PRs with repos (NO STAR LIMIT)
# -------------------------------
merged = pr_df.merge(
    repo_df[['id', 'full_name', 'language', 'forks', 'stars']],
    left_on='repo_id', right_on='id', how='inner'
)

# Normalize PR id column
if 'id' in merged.columns:
    pr_id_col = 'id'
elif 'id_x' in merged.columns:
    pr_id_col = 'id_x'
else:
    raise KeyError(f"PR id column not found. Columns: {list(merged.columns)}")

df = merged.rename(columns={pr_id_col: 'pr_id'}).copy()

# Ensure title/body columns exist (as strings)
for col in ("title", "body"):
    if col not in df.columns:
        df[col] = ""

# -------------------------------
# 3) Clean text
# -------------------------------
TAG_RE = re.compile(r"<[^>]+>")
WS_RE  = re.compile(r"\s+")

def clean_text(x):
    if not isinstance(x, str):
        return ""
    t = html.unescape(x)
    t = t.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    t = TAG_RE.sub("", t)
    t = WS_RE.sub(" ", t).strip()
    return t

df["title"] = df["title"].apply(clean_text)
df["body"]  = df["body"].apply(clean_text)

# -------------------------------
# 4) Strict Refactor-only filter
# -------------------------------
REFAC_RE = re.compile(r"(?i)\bre[-\s]*factor\w*\b")

def is_refactor(s):
    return bool(REFAC_RE.search(s)) if isinstance(s, str) else False

mask = df["title"].apply(is_refactor) | df["body"].apply(is_refactor)
refactor_prs = df.loc[mask].copy()

# -------------------------------
# 5) Save CSV (same folder)
# -------------------------------
cols = [c for c in [
    'pr_id', 'number', 'title', 'state', 'created_at', 'closed_at', 'merged_at',
    'user', 'repo_id', 'full_name', 'language', 'forks', 'stars', 'html_url', 'repo_url'
] if c in refactor_prs.columns]

script_dir = os.path.dirname(os.path.abspath(__file__))
out_csv = os.path.join(script_dir, "AIDev_all_refactor_PRs.csv")

refactor_prs[cols].to_csv(
    out_csv,
    index=False,
    encoding='utf-8-sig',
    lineterminator='\n',
    quoting=csv.QUOTE_MINIMAL
)

# -------------------------------
# 6) Summary
# -------------------------------
print(f"✅ Strict refactor PRs: {len(refactor_prs):,} of {len(df):,} merged rows")
print(f"💾 Saved to: {out_csv}")
if len(refactor_prs):
    print("\nSample rows:")
    print(refactor_prs[cols].head(10))
