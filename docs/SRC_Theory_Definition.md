# Theoretical Framework: Structure-Rich Computing (SRC)

> **"Computation is the transformation of structure. If we capture the structure, we capture the computation."**

## 1. The Core Hypothesis: Dimensional Collapse

Traditional computational complexity theory treats logic problems (like 3-SAT) as symbolic manipulations in a high-dimensional combinatorial space. The **SRC (Structure-Rich Computing)** paradigm proposes a fundamental shift:

**Hypothesis (Topological Prior):**  
The computational hardness and satisfiability of a logical system are encoded in the **low-dimensional topological manifold** of its variable interactions. By projecting the high-dimensional logic space onto a lower-dimensional spectral domain, we can perform probabilistic inference with polynomial-time complexity that approximates NP-hard properties.

---

## 2. Formal Definitions

### 2.1 Problem Space

Let $\mathcal{F}$ be a Boolean formula in Conjunctive Normal Form (CNF) with $n$ variables and $m$ clauses.  
Conventionally, determining $\mathrm{SAT}(\mathcal{F})$ requires reasoning over the assignment space $\{0,1\}^n$.

### 2.2 Variable Interaction Graph (VIG)

We define a mapping
\[
  \Phi: \mathcal{F} \rightarrow G
\]
where $G = (V, E)$ is an undirected graph:

- **Vertices $V$**: variables $\{x_1, \dots, x_n\}$.
- **Edges $E$**: an edge $(x_i, x_j)$ exists if variables $x_i$ and $x_j$ co-occur in at least one clause.

The graph $G$ captures the **skeleton of constraints**, abstracting away concrete literal polarity (negation).

### 2.3 SRC Structure Kernel $\mathcal{K}$

The core innovation of SRC is to extract a **Structure Kernel** from $G$ using spectral graph theory.

Let $A$ be the adjacency matrix of $G$ and $D$ be the degree matrix. The **normalized Laplacian** is defined as:
\[
  \mathcal{L} = I - D^{-1/2} A D^{-1/2}.
\]

We then define the **SRC Kernel** as a spectral fingerprint of $\mathcal{L}$:

\[
  \mathcal{K}_{SRC}: \mathcal{F} \to \mathbb{R}^k,\quad
  \mathcal{K}_{SRC}(\mathcal{F}) = [\lambda_1, \lambda_2, \dots, \lambda_k],
\]

where $\lambda_i$ are the ordered eigenvalues of $\mathcal{L}$ (e.g., largest-$k$ or smallest-$k$), and $0 \le \lambda_i \le 2$.

In practice, $k \ll n$, so $\mathcal{K}_{SRC}$ acts as a **dimension-collapsing map** from discrete logic space to a continuous, low-dimensional structural manifold.

---

## 3. Why Spectral Features Predict Satisfiability

### 3.1 Connectivity and Hardness

The spectrum of the Laplacian encodes global connectivity patterns of $G$:

- **Small eigenvalues** (near 0) indicate loosely connected or decomposable structure (amenable to divide-and-conquer).
- **Large eigenvalues** (near 2) and spectral gaps reflect expansion, bottlenecks, and potential conflict-rich substructures.

Intuitively, **“hard” or UNSAT-like** instances tend to exhibit tightly coupled, high-expansion interaction graphs, whereas **“easy” or SAT-like** instances often decompose into more weakly connected components.

### 3.2 Phase Transition Signature

In random 3-SAT, hardness peaks around clause-to-variable ratio $\alpha \approx 4.26$.  
The SRC viewpoint conjectures that this **phase transition** is accompanied by a distinct change in the spectral distribution of the VIG.

Rather than searching the assignment space, SRC learns a **decision boundary in spectral space** that separates “typically SAT” from “typically UNSAT” based on these topological signatures.

---

## 4. SRC Model Architecture

We define the SRC predictor as:
\[
  P(\mathrm{SAT} \mid \mathcal{F}) \approx f\big(\mathcal{K}_{SRC}(\mathcal{F})\big),
\]
where:

- $\mathcal{F}$ is a 3-SAT instance,
- $\mathcal{K}_{SRC}(\mathcal{F}) \in \mathbb{R}^k$ is its spectral fingerprint,
- $f$ is a lightweight classifier (e.g., logistic regression).

### 4.1 Computational Complexity

- **Traditional SAT Solver:** worst-case exponential in $n$ (e.g. $O(2^n)$).
- **SRC Inference Pipeline:**
  - Feature extraction via eigen-decomposition of $\mathcal{L}$: $O(n^3)$ in the dense case (potentially near-linear with sparse / approximate methods).
  - Classification via $f$: typically $O(k)$.

Thus, SRC provides a **polynomial-time surrogate** for approximating SAT/UNSAT labels on random instances, purely from structural information.

---

## 5. Experimental Validation (SRC-SAT-Topology)

In the `SRC-SAT-Topology` experiments (up to $N=30{,}000$ instances), we observe:

1. **Information Retention**  
   The structure kernel $\mathcal{K}_{SRC}$ alone supports **≈84% accuracy** in distinguishing SAT vs UNSAT, far above the random baseline (50%).

2. **Robustness Across Seeds**  
   Results are stable over multiple random seeds and are invariant under variable permutations, indicating that the signal is genuinely topological rather than spurious.

3. **Convergence Behavior**  
   As the sample size increases (5k → 10k → 30k), accuracy converges rather than fluctuating wildly, suggesting that the underlying spectral–logical relationship is stable and learnable.

---

## 6. Future Directions: Average-Case Collapsibility of NP

SRC does **not** claim to exactly solve NP-complete problems in polynomial time (which would imply $P = NP$). Instead, it provides evidence that:

- For random 3-SAT in a specific regime,
- The **average-case behavior** of SAT vs UNSAT can be **partially collapsed** into a low-dimensional structural manifold.

This raises several theoretical questions:

1. Which families of NP problems admit such **structure-level surrogate predictors**?
2. Can we characterize the **topological fingerprints of truly hard instances** (e.g., worst-case UNSAT)?
3. How does SRC interact with other paradigms such as message-passing, belief propagation, or neural SAT solvers?

These questions form the next stage of the SRC research program.
