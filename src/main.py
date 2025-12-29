import time
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from generator import generate_3sat_instance, solve_sat_label


def extract_topology_features(n_vars, clauses):
    """
    SRC 核心：将 3-SAT 的变量共现结构抽象为
    变量交互图的归一化拉普拉斯谱指纹。
    """
    G = nx.Graph()
    G.add_nodes_from(range(1, n_vars + 1))

    for c in clauses:
        vars_in_clause = [abs(l) for l in c]
        if len(vars_in_clause) != 3:
            continue
        u, v, w = vars_in_clause
        G.add_edge(u, v)
        G.add_edge(v, w)
        G.add_edge(u, w)

    try:
        L = nx.normalized_laplacian_matrix(G).todense()
        eigenvalues = np.linalg.eigvalsh(L)
        k = 30
        fingerprint = sorted(eigenvalues, reverse=True)[:k]
        if len(fingerprint) < k:
            fingerprint += [0.0] * (k - len(fingerprint))
    except Exception:
        fingerprint = [0.0] * 30

    return fingerprint


def run_experiment(sample_size, n_rounds=10):
    """
    对给定样本量 N，重复 n_rounds 次实验，返回均值和方差。
    """
    print(f"评估样本量: {sample_size} | 进行 {n_rounds} 轮测试...")
    round_accs = []

    for r in range(n_rounds):
        seed = 42 + r * 100
        np.random.seed(seed)
        random.seed(seed)

        X, y = [], []

        for _ in range(sample_size):
            clauses = generate_3sat_instance(n_vars=50, clause_ratio=4.26)
            label = solve_sat_label(clauses)
            feats = extract_topology_features(50, clauses)
            X.append(feats)
            y.append(label)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2
        )

        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)

        acc = accuracy_score(y_test, clf.predict(X_test))
        round_accs.append(acc)
        print(
            f"  Round {r+1}/{n_rounds}: Acc = {acc:.4%}",
            end="\r"
        )

    mean_acc = float(np.mean(round_accs))
    std_acc = float(np.std(round_accs))
    print(f"  Done! Mean: {mean_acc:.4%} | Std: {std_acc:.4%}")
    return mean_acc, std_acc


def main():
    print("🚀 Starting SRC-SAT-Topology Large Scale Experiment...")
    start_time = time.time()

    sample_targets = [5000, 10000, 30000]
    results = {}

    for size in sample_targets:
        results[size] = run_experiment(size, n_rounds=10)

    end_time = time.time()

    print("\n" + "=" * 60)
    print(
        f"🔬 SRC-SAT-Topology Final Report "
        f"(Total Time: {(end_time - start_time) / 60:.2f} min)"
    )
    print("=" * 60)
    print(f"{'Sample Size (N)':<20} | {'Mean Acc':<20} | {'Std Dev':<20}")
    print("-" * 60)

    for size in sample_targets:
        if size in results:
            m, s = results[size]
            print(f"{size:<20} | {m:<20.4%} | ±{s:<10.4%}")

    print("=" * 60)

    # 绘图
    sizes = list(results.keys())
    means = [results[s][0] for s in sizes]
    stds = [results[s][1] for s in sizes]

    plt.figure(figsize=(8, 5))
    plt.errorbar(
        sizes,
        means,
        yerr=stds,
        fmt="-o",
        capsize=5,
        ecolor="red",
        label="SRC-SAT Accuracy",
    )
    plt.axhline(
        0.5, linestyle="--", color="gray", label="Random Baseline (0.50)"
    )
    plt.xscale("log")
    plt.xticks(sizes, ["5k", "10k", "30k"])
    plt.xlabel("Sample Size (N)")
    plt.ylabel("Accuracy")
    plt.title("SRC-SAT-Topology Convergence Curve (10 runs per N)")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # 保存到 assets 目录，跟 README 对齐
    plt.savefig("assets/benchmark_convergence.png", dpi=200)
    print("📌 Plot saved to assets/benchmark_convergence.png")


if __name__ == "__main__":
    main()
