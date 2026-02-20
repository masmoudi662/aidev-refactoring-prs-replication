# AI-Generated Refactoring Pull Requests — Replication Package

This repository provides the replication package for our study on **AI-generated refactoring pull requests** in the AIDev dataset.

The study investigates:

- how autonomous coding agents describe refactoring changes,
- what refactoring transformation patterns they produce,
- how human reviewers evaluate these pull requests,
- and why many AI-generated refactorings are not integrated.

---

## Research Questions

### RQ1 — Refactoring Patterns
Analyzes refactoring action verbs and transformation patterns used by AI agents and classifies pull requests into:

- Internal quality attributes  
- External quality attributes  
- Code smells  

Implementation: `src/rq1/`

---

### RQ2 — Review Analysis
Examines how human reviewers respond to AI-generated refactoring PRs using the Refactoring Review Taxonomy.

Implementation: `src/rq2/`

---

## Repository Structure

```
src/
  rq1/        # Refactoring pattern mining (RQ1)
  rq2/        # Review analysis (RQ2)

results/
  rq1/        # Generated outputs for RQ1
  rq2/        # Generated outputs for RQ2
```

## Dataset

We use the **AIDev** dataset of AI-generated pull requests.

Due to size and licensing constraints, the full dataset is **not redistributed** in this repository.

See `data/README.md` for instructions.

---
---

## Visual Overview

### Study Design (RQ2)

![RQ2 Study Pipeline](experiments/rq2/figures/Study_design_RQ2.png)

---

### Refactoring Review Taxonomy

![Refactoring Review Taxonomy](experiments/rq2/figures/Refactoring%20review%20criteria%20in%20modern%20code%20review%20for%20RQ2.png)

---

### Review Actions by Type

![Review Actions](experiments/rq2/figures/chart_review_actions.png)

## Requirements

- Python 3.10+
- pandas
- numpy
- regex
- matplotlib
- tqdm

---

## License

MIT License
