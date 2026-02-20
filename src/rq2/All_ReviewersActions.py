#!/usr/bin/env python3
# Extract ALL reviews for ALL strict refactor PRs (no star cutoff)
# Added: clear console progress printing at each important step

import os
import re
import html
import pandas as pd
import csv

# -----------------------------
# Utility functions
# -----------------------------
def read_first_available(paths):
    """Try each path in order until one works."""
    last_err = None
    for p in paths:
        try:
            print(f"[INFO] Trying to load: {p}")
            df = pd.read_parquet(p)
            print(f"[OK] Loaded {len(df):,} rows from {p}")
            return df
        except Exception as e:
            print(f"[WARN] Could not read {p}: {e}")
            last_err = e
    raise last_err

def clean_text(x):
    """Clean HTML and whitespace."""
    if not isinstance(x, str): return ""
    t = html.unescape(x)
    t = t.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

def to_int64(series):
    return pd.to_numeric(series, errors="coerce").astype("Int64").astype("float").astype("int64")

# -----------------------------
# 1) Load ALL tables
# -----------------------------
print("\n========== STEP 1: Loading dataset ==========\n")

PR_PATHS   = ["hf://datasets/hao-li/AIDev/all_pull_request.parquet",
              "hf://datasets/hao-li/AIDev/pull_request.parquet"]
REPO_PATHS = ["hf://datasets/hao-li/AIDev/all_repository.parquet",
              "hf://datasets/hao-li/AIDev/repository.parquet"]
REV_PATHS  = ["hf://datasets/hao-li/AIDev/all_pr_reviews.parquet",
              "hf://datasets/hao-li/AIDev/pr_reviews.parquet"]

pr_df   = read_first_available(PR_PATHS)
repo_df = read_first_available(REPO_PATHS)
reviews_df = read_first_available(REV_PATHS)

print(f"\n[INFO] Loaded PRs: {len(pr_df):,}")
print(f"[INFO] Loaded Repositories: {len(repo_df):,}")
print(f"[INFO] Loaded Reviews: {len(reviews_df):,}")

# -----------------------------
# 2) Join PRs ↔ repos
# -----------------------------
print("\n========== STEP 2: Joining PRs with repository info ==========\n")
merged_pr = pr_df.merge(
    repo_df[['id', 'full_name', 'language', 'forks', 'stars']],
    left_on='repo_id', right_on='id', how='inner'
)
print(f"[INFO] Joined PRs with repos → total rows: {len(merged_pr):,}")

# -----------------------------
# 3) Pick PR ID column
# -----------------------------
print("\n========== STEP 3: Detecting PR ID column ==========\n")
if 'id_x' in merged_pr.columns:
    pr_id_col = 'id_x'
elif 'id' in merged_pr.columns:
    pr_id_col = 'id'
else:
    raise KeyError(f"Could not find PR id column. Columns: {list(merged_pr.columns)}")

df = merged_pr.rename(columns={pr_id_col: 'pr_id'}).copy()
print(f"[INFO] Using column '{pr_id_col}' as PR id")

# Ensure title/body exist
for c in ('title','body'):
    if c not in df.columns:
        df[c] = ""

# -----------------------------
# 4) Filter ONLY Refactoring PRs
# -----------------------------
print("\n========== STEP 4: Filtering refactor PRs ==========\n")
REFAC_RE = re.compile(r"(?i)\bre[-\s]*factor\w*\b")
df['title'] = df['title'].apply(clean_text)
df['body']  = df['body'].apply(clean_text)

mask = df['title'].str.contains(REFAC_RE) | df['body'].str.contains(REFAC_RE)
ref_prs = df.loc[mask, ['pr_id','full_name','stars']].copy()
ref_prs['pr_id'] = to_int64(ref_prs['pr_id'])
print(f"[INFO] Total Refactor PRs found: {len(ref_prs):,}")

# -----------------------------
# 5) Load review actions of those PRs
# -----------------------------
print("\n========== STEP 5: Selecting review actions ==========\n")
if 'pr_id' not in reviews_df.columns:
    raise KeyError("Reviews table missing 'pr_id' column.")
reviews_df = reviews_df.copy()
reviews_df['pr_id'] = to_int64(reviews_df['pr_id'])
print(f"[INFO] Reviews table ready with {len(reviews_df):,} rows.")

# -----------------------------
# 6) Keep only reviews for those filtered PRs
# -----------------------------
print("\n========== STEP 6: Filtering reviews for refactor PRs ==========\n")
reviews_ref = reviews_df[reviews_df['pr_id'].isin(ref_prs['pr_id'])].copy()
print(f"[INFO] Matched {len(reviews_ref):,} review rows for {reviews_ref['pr_id'].nunique():,} unique refactor PRs")

# Normalize timestamp to submitted_at if needed
if 'submitted_at' not in reviews_ref.columns:
    if 'submitted' in reviews_ref.columns:
        reviews_ref = reviews_ref.rename(columns={'submitted':'submitted_at'})
    elif 'created_at' in reviews_ref.columns:
        reviews_ref = reviews_ref.rename(columns={'created_at':'submitted_at'})

# Clean body
if 'body' in reviews_ref.columns:
    reviews_ref['body'] = reviews_ref['body'].apply(clean_text)

# -----------------------------
# 7) Attach repo context to each review
# -----------------------------
print("\n========== STEP 7: Attaching repo info to reviews ==========\n")
reviews_ref = reviews_ref.merge(
    ref_prs, on='pr_id', how='left', suffixes=('', '_pr')
)
print(f"[INFO] Reviews with repo context: {len(reviews_ref):,}")

# -----------------------------
# 8) Quick console peek
# -----------------------------
print("\n========== STEP 8: Quick summary preview ==========\n")
total_ref = len(ref_prs)
covered   = reviews_ref['pr_id'].nunique()
print(f"Strict refactor PRs: {total_ref:,}")
print(f"PRs with ≥1 formal review: {covered:,} ({(covered/total_ref if total_ref else 0):.1%})")
print(f"Total review rows: {len(reviews_ref):,}\n")
peek_cols = [c for c in ['pr_id','user','state','submitted_at','full_name','stars'] if c in reviews_ref.columns]
print("Sample rows:")
print(reviews_ref[peek_cols].head(10))

# -----------------------------
# 9) Save CSV (same folder)
# -----------------------------
print("\n========== STEP 9: Saving results ==========\n")
script_dir = os.path.dirname(os.path.abspath(__file__))
out_csv = os.path.join(script_dir, "AIDev_all_refactor_PR_reviews.csv")

save_cols = [c for c in ['pr_id','user','state','submitted_at','full_name','stars','body'] if c in reviews_ref.columns]
reviews_ref[save_cols].to_csv(
    out_csv, index=False, encoding='utf-8-sig',
    lineterminator='\n', quoting=csv.QUOTE_MINIMAL
)
print(f"\n✅ Saved final dataset → {out_csv}")
print("==============================================")
