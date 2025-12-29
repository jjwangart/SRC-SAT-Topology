🧠 SRC-SAT-Topology

Predict SAT satisfiability using structural topology + SRC (Structure-Rich Classifiers) — without full search.

🔥 Key Result

🔥 Result: Predict SAT satisfiability without solving — achieves 0.84 accuracy using only structure topology (baseline = 0.50).

Even without calling a SAT solver at inference time, SRC-SAT predicts satisfiability purely from graph structure, reaching performance far above the random baseline (0.50).

📜 Overview

This repository implements SRC-SAT-Topology, a lightweight spectral–topology classifier that predicts whether a random 3-SAT instance is satisfiable by analyzing only its variable–clause interaction graph, without running full search during inference.

This project is part of the broader research direction:

SRC: Structure-Rich Computing – A Computational Paradigm for Dimensional Collapse and Structure-Level Inference

Core idea:

Turn each 3-SAT instance into a variable interaction graph

Compute a spectral fingerprint (eigenvalues of the normalized Laplacian)

Use a simple classifier on top of these spectral features to approximate SAT/UNSAT

📊 Experimental Results — Convergence Curve

All reported numbers are averaged over 10 independent runs (10 seeds) per sample size.

<img src="assets/benchmark_convergence.png" width="480">
Sample Size (N)	Mean Accuracy
5,000	0.818
10,000	0.840
30,000	0.837

Baseline (random guess): 0.50

The curve shows that the SRC-SAT-Topology classifier:

Stabilizes around ≈0.84 accuracy as N grows

Is structurally robust: no catastrophic degradation at larger sample sizes

Works purely from topology + spectrum, without using solver internals at test time

🧩 Method Summary

At a high level:

3-SAT Generation

Random 3-SAT formulas with fixed number of variables (e.g., 50)

Clause-to-variable ratio sampled in a critical range (e.g., 3.5–5.5)

Topology Construction

Build an undirected graph over variables

Add edges between variables that co-occur in the same clause

This yields a variable interaction graph capturing structural difficulty

Spectral Fingerprint (SRC Topology Kernel)

Compute the normalized Laplacian 
𝐿
L of the graph

Extract top-k eigenvalues (e.g., 30) as a “fingerprint” of the instance

This acts as a low-dimensional structure kernel for SRC

Classifier

Train a simple Logistic Regression on these fingerprints

Evaluate test accuracy on held-out SAT / UNSAT labels
