import random
from pysat.solvers import Glucose3

def generate_3sat_instance(n_vars=50, clause_ratio=4.26):
    """
    Generates a random 3-SAT instance.
    
    Args:
        n_vars (int): Number of variables (default: 50)
        clause_ratio (float): Ratio of clauses to variables (m/n). 
                              Hardest region is around 4.26.
    
    Returns:
        list: A list of clauses, where each clause is a list of 3 integers.
              e.g., [[1, -2, 3], [-1, 4, 5], ...]
    """
    n_clauses = int(n_vars * clause_ratio)
    clauses = []
    
    for _ in range(n_clauses):
        # Generate a clause with 3 distinct variables
        # Randomly assign negation (positive or negative)
        clause = []
        while len(clause) < 3:
            var = random.randint(1, n_vars)
            literal = var * random.choice([1, -1])
            if abs(literal) not in [abs(l) for l in clause]:
                clause.append(literal)
        clauses.append(clause)
        
    return clauses

def solve_sat_label(clauses):
    """
    Uses a standard solver (Glucose3) to determine the ground truth label.
    
    Args:
        clauses (list): The 3-SAT formula.
        
    Returns:
        int: 1 if Satisfiable, 0 if Unsatisfiable.
    """
    g = Glucose3()
    for c in clauses:
        g.add_clause(c)
    is_sat = g.solve()
    g.delete()
    return 1 if is_sat else 0

if __name__ == "__main__":
    # Test block: verifying generation works
    print("Testing generator...")
    sample_clauses = generate_3sat_instance(n_vars=10, clause_ratio=4.0)
    label = solve_sat_label(sample_clauses)
    print(f"Generated {len(sample_clauses)} clauses.")
    print(f"Ground Truth Label: {'SAT' if label else 'UNSAT'}")
