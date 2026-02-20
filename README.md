
---

## Dataset

We use the **AIDev** dataset of AI-generated pull requests.

Due to size and licensing constraints, the full dataset is **not redistributed** in this repository.

See `data/README.md` for instructions.

---

## Study Design

### RQ2 Study Pipeline

![RQ2 Study Pipeline](experiments/rq2/figures/Study_design_RQ2.png)

This figure summarizes the data collection, preparation, and analysis workflow used for RQ2.

---

## Experiments

### RQ2 — Refactoring Review Taxonomy

![Refactoring Review Taxonomy](experiments/rq2/figures/Refactoring%20review%20criteria%20in%20modern%20code%20review%20for%20RQ2.png)

### RQ2 — Review Actions by Type

![Review Actions](experiments/rq2/figures/chart_review_actions.png)

---

## Discussion & Takeaways

### RQ2 — Frequency of Reviewer Concerns

![Reviewer Concerns Frequency](experiments/rq2/figures/Frequency%20of%20reviewer%20concerns%20by%20category.png)

---

## Reproducibility

See:
- `REPRODUCIBILITY.md` — pipeline overview  
- `src/rq1/` — RQ1 implementation  
- `src/rq2/` — RQ2 implementation  

---

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
