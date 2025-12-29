# 🧠 SRC-SAT-Topology

Predict SAT satisfiability using **structural topology** + **SRC (Structure-Rich Classifiers)** — without full search.

---

## 📜 Overview

This repository implements **SRC-SAT-Topology**, a lightweight spectral–topology classifier that predicts whether a random 3-SAT instance is satisfiable by analyzing only its structural graph (variable–clause topology), without running full solving.

This project accompanies the research direction:

> **SRC: Structure-Rich Computing – A Computational Paradigm for Dimensional Collapse and Structure-Level Inference**

---

## 📊 Experimental Results — Convergence Curve

Below shows our 10-round repeated experiment verifying the stability of topology-only prediction across sample size:

<img src="accuracy_curve.png" width="480">

| Sample Size | Mean Accuracy |
|-------------|---------------|
| 5,000       | 0.818 |
| 10,000      | 0.840 |
| 30,000      | 0.837 |

Baseline (random): **0.50**

---

## 🚀 How to Run

Install dependencies:

```bash
pip install -r requirements.txt
