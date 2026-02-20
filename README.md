# Replication Package — AI Refactoring PRs (AIDev)

This repository provides the replication package for our study on AI-generated refactoring pull requests and their human review outcomes in the **AIDev** dataset.

## What this repo reproduces
1. Extract refactoring action verbs from PR titles/descriptions to identify transformation patterns.
2. Classify PRs into:
   - Internal quality attributes
   - External quality attributes
   - Code smells
3. Code human review feedback using a lightweight Refactoring Review Taxonomy approximation.
4. Generate summary tables and basic plots.

## Structure
- `src/` — pipeline scripts
- `data/` — dataset instructions + sample
- `scripts/` — one-command runners
- `results/` — outputs (generated)

## Quickstart (sample)
```bash
pip install -r env/requirements.txt
bash scripts/run_all.sh --use-sample
