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
