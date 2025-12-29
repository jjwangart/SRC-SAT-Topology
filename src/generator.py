"""
generator.py
--------------
3-SAT random instance generator + SAT ground-truth solver.

This script is intentionally lightweight and transparent, designed to
show that all datasets used in SRC-SAT-Topology are *real*, *randomly generated*,
and *solver-verified* — NOT manually labeled or synthetic shortcuts.
"""

import random
from typing import List, Tuple
from pysat.solvers import Glucose3


def generate_3sat_instance(n_vars: int = 50, clause_ratio: float = 4.26, seed: int = None) -> List[List[int]]:
    """
    Generate a random 3-SAT formula in CNF.

    Args:
        n_vars (int): Number of variables.
        clause_ratio (float): Clause-to-variable ratio m/n.
                              Critical phase transition ~4.26.
        seed (int): Optional random seed for reproducibility.

    Returns:
        List[List[int]]: A CNF list of clauses (each clause has exactly 3 literals).

    Example Output:
        [[1, -2, 3], [-1, 4, 5], ...]
    """
    if seed is not None:
        random.seed(seed)

    n_clauses = int(n_vars * clause_ratio)
    clauses = []

    for _ in range(n_clauses):
        clause = []
        while len(clause) < 3:
            var = random.randint(1, n_vars)
            lit = var * random.choice([1, -1])
            # prevent duplicate variables inside the same clause
            if abs(lit) not in [abs(x) for x in clause]:
                clause.append(lit)
        clauses.append(clause)

    return clauses


def solve_sat_label(clauses: List[List[int]]) -> int:
    """
    Ground-truth SAT solver — returns the REAL label (using Glucose3).

    Args:
        clauses (List[List[int]]): CNF clause list.

    Returns:
        int: 1 = SAT, 0 = UNSAT
    """
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)
    sat = g.solve()
    g.delete()
    return 1 if sat else 0


def generate_dataset(n_samples: int = 1000, n_vars: int = 50, clause_ratio: float = 4.26, seed: int = None) \
        -> Tuple[List[List[List[int]]], List[int]]:
    """
    Generate a full dataset + labels (proof of real data).

    Returns:
        formulas (List[List[List[int]]]), labels (List[int])
    """
    if seed is not None:
        random.seed(seed)

    formulas, labels = [], []
    for _ in range(n_samples):
        f = generate_3sat_instance(n_vars, clause_ratio)
        formulas.append(f)
        labels.append(solve_sat_label(f))
    return formulas, labels


if __name__ == "__main__":
    print("🔍 Testing generator...\n")
    cnf = generate_3sat_instance(n_vars=10, clause_ratio=4.0, seed=42)
    label = solve_sat_label(cnf)

    print(f"Generated clauses: {len(cnf)}")
    print(f"Example CNF: {cnf[:3]} ...")
    print(f"Ground Truth Label: {'SAT' if label else 'UNSAT'}")
