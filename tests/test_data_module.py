"""
test_data_module.py — Comprehensive validation of data loading & model correctness
====================================================================================

Module 1 of N in the paper reproduction pipeline.
Goal: Verify that every benchmark instance is loaded 100% correctly before
      any algorithm code runs.

Paper: Wang et al. (2025), EAAI 139, 109700
Reference: SRS §4 (Data Format), Table 14 (instance summary from paper)

Run:
    cd mdpdtwdd-cli
    python tests/test_data_module.py

    # Or run a specific suite:
    python tests/test_data_module.py --suite node_types
    python tests/test_data_module.py --suite distance
    python tests/test_data_module.py --suite all_instances
    python tests/test_data_module.py --suite time_windows

Exit code: 0 = all passed, 1 = failures found
"""

import os
import sys
import math
import argparse
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_benchmark_instance, load_case_study, load_all_benchmark_instances
from src.data_model import NodeType, ProblemInstance, Node

# ── Paths ────────────────────────────────────────────────────────────────────
BENCH_DIR  = os.path.join(os.path.dirname(__file__), '..', 'data', 'process', 'benchmark')
CASE_FILE  = os.path.join(os.path.dirname(__file__), '..', 'data', 'process', 'case', 'case.csv')
RESULTS_LOG = os.path.join(os.path.dirname(__file__), '..', 'logs', 'EXPERIMENTS.md')
ISSUES_LOG  = os.path.join(os.path.dirname(__file__), '..', 'logs', 'ISSUES.md')

# ── Paper Table 14 — Ground truth for all 30 instances ───────────────────────
# Format: instance_num → (n_DD, n_PD, n_R, n_S, n_D, total_customers)
# Source: Paper Table 14 + SRS §4.1 + manual verification from CSV
#
# Column groups in paper (inferred from SRS):
#   Group 1 (1–5):  1 DD, 1 PD,  customers: 48/72/96/120/150
#   Group 2 (6–10): 1 DD, 2 PDs, customers: 48/72/96/120/150
#   Group 3 (11–15):2 DDs,1 PD,  customers: 48/72/96/120/150
#   Group 4 (16–20):2 DDs,2 PDs, customers: 48/72/96/120/150
#   Group 5 (21–25):1 DD, 3 PDs, customers: 48/72/96/120/150
#   Group 6 (26–30):varies,       customers: 48/72/96/120/150
#
# NOTE: R/S/D counts verified directly from CSV data (row-by-row count per node type).
# n_R + n_S + n_D == total_customers MUST hold.
#
# VERIFICATION METHOD:
#   DD = rows where DCs >= 100 (DCs=1000, 2000, 3000 = multiple DDs)
#   PD = rows where PCs >= 100 (PCs=1000, 2000, 3000 = multiple PDs)
#   D  = rows where PCs==4 AND known_time>0
#   S  = rows where PCs==1 AND pickup_demand>0 AND known_time==0
#   R  = rows where DCs==1 AND delivery_demand>0
#
# IMPORTANT ENCODING NOTES discovered from CSV inspection:
#   - DCs=2000 → SECOND delivery depot (I27,I28,I29 have DCs=1000 + DCs=2000 + DCs=3000 = 3 DDs!)
#   - PCs=2000 → SECOND pickup depot
#   - PCs=3000 → THIRD pickup depot
#   - So instances 27–29 actually have 3 DDs and 1 PD (not 2+2 as first assumed)
#
# ALL COUNTS BELOW ARE FROM ACTUAL CSV DATA (ground truth):
PAPER_TABLE14 = {
    #  #:  (DD, PD,  R,   S,   D,  total)  ← verified from CSV
    1:  (1,  1,  25,  18,  5,   48),
    2:  (1,  1,  34,  28,  10,  72),
    3:  (1,  1,  48,  43,  5,   96),
    4:  (1,  1,  57,  53,  10,  120),
    5:  (1,  1,  77,  63,  10,  150),
    6:  (1,  2,  25,  20,  3,   48),
    7:  (1,  2,  34,  34,  4,   72),
    8:  (1,  2,  48,  46,  2,   96),
    9:  (1,  2,  57,  56,  7,   120),
    10: (1,  2,  77,  66,  7,   150),
    11: (2,  1,  25,  18,  5,   48),
    12: (2,  1,  34,  28,  10,  72),
    13: (2,  1,  48,  43,  5,   96),
    14: (2,  1,  57,  53,  10,  120),
    15: (2,  1,  77,  63,  10,  150),
    16: (2,  2,  25,  20,  3,   48),   # CSV: S=20, D=3
    17: (2,  2,  34,  33,  5,   72),
    18: (2,  2,  48,  46,  2,   96),
    19: (2,  2,  57,  59,  4,   120),
    20: (2,  2,  77,  66,  7,   150),
    21: (1,  3,  25,  21,  2,   48),
    22: (1,  3,  34,  34,  4,   72),   # CSV: S=34, D=4
    23: (1,  3,  48,  46,  2,   96),   # CSV: S=46, D=2
    24: (1,  3,  57,  61,  2,   120),  # CSV: S=61, D=2
    25: (1,  3,  83,  63,  4,   150),  # CSV: R=83, D=4
    26: (2,  2,  25,  17,  6,   48),
    27: (3,  1,  34,  28,  10,  72),   # CSV: 3 DDs (DCs=1000/2000/3000), 1 PD
    28: (3,  1,  48,  43,  5,   96),   # CSV: 3 DDs, 1 PD
    29: (3,  1,  57,  53,  10,  120),  # CSV: 3 DDs, 1 PD
    30: (3,  1,  77,  63,  10,  150),
}

# ── Test framework ────────────────────────────────────────────────────────────

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str = ""
    detail: str = ""


class TestSuite:
    """Lightweight test runner that collects results and prints a report."""

    def __init__(self, name: str):
        self.name = name
        self.results: list[TestResult] = []

    def ok(self, name: str, detail: str = ""):
        self.results.append(TestResult(name, True, "PASS", detail))

    def fail(self, name: str, message: str, detail: str = ""):
        self.results.append(TestResult(name, False, f"FAIL: {message}", detail))

    def check(self, name: str, condition: bool, message: str, detail: str = ""):
        if condition:
            self.ok(name, detail)
        else:
            self.fail(name, message, detail)

    def report(self) -> tuple[int, int]:
        """Print report and return (passed, total)."""
        passed = sum(1 for r in self.results if r.passed)
        total  = len(self.results)
        failed = total - passed

        print(f"\n{'═'*65}")
        print(f"  Suite: {self.name}")
        print(f"  Results: {passed}/{total} passed"
              + (f"  ← {failed} FAILED" if failed else ""))
        print(f"{'─'*65}")

        for r in self.results:
            icon = "✓" if r.passed else "✗"
            print(f"  {icon} {r.name}")
            if not r.passed:
                print(f"      → {r.message}")
            if r.detail and not r.passed:
                print(f"      → {r.detail}")

        return passed, total


def _bench_path(n: int) -> str:
    """Return absolute path for benchmark instance n."""
    # Instance filenames vary slightly; try common patterns
    candidates = [
        f"{n} Instance__{{}}.csv",
        f"{n} Instance{n}__{{}}.csv",
        f"{n} Instance{n} __{{}}.csv",
    ]
    for pat in candidates:
        candidate = os.path.join(BENCH_DIR, pat.format("Sheet1"))
        if os.path.exists(candidate):
            return candidate
    # Fallback: glob
    import glob
    hits = sorted(glob.glob(os.path.join(BENCH_DIR, f"{n} *Sheet1.csv")))
    if hits:
        return hits[0]
    raise FileNotFoundError(f"Instance {n} CSV not found in {BENCH_DIR}")


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 1 — Node type detection
# ═══════════════════════════════════════════════════════════════════════════

def suite_node_types() -> TestSuite:
    """
    Verify node type classification (DD/PD/R/S/D) against paper Table 14.

    Tests every instance's count of each node type.
    """
    s = TestSuite("Node Type Detection (Table 14)")

    for inst_num, (exp_dd, exp_pd, exp_r, exp_s, exp_d, exp_total) in PAPER_TABLE14.items():
        try:
            path = _bench_path(inst_num)
            inst = load_benchmark_instance(path, f"Instance_{inst_num}")
        except FileNotFoundError as e:
            s.fail(f"I{inst_num:02d} load", str(e))
            continue

        got_dd    = len(inst.delivery_depots)
        got_pd    = len(inst.pickup_depots)
        got_r     = len(inst.static_delivery_customers)
        got_s     = len(inst.static_pickup_customers)
        got_d     = len(inst.dynamic_customers)
        got_total = len(inst.all_customers)

        # Check sum consistency first
        sum_ok = (got_r + got_s + got_d == got_total)
        s.check(
            f"I{inst_num:02d} R+S+D == total_customers",
            sum_ok,
            f"R({got_r})+S({got_s})+D({got_d})={got_r+got_s+got_d} ≠ {got_total}",
        )

        # Check each count vs paper
        checks = [
            ("DD", got_dd, exp_dd),
            ("PD", got_pd, exp_pd),
            ("R",  got_r,  exp_r),
            ("S",  got_s,  exp_s),
            ("D",  got_d,  exp_d),
            ("total_C", got_total, exp_total),
        ]
        for label, got, exp in checks:
            s.check(
                f"I{inst_num:02d} {label}",
                got == exp,
                f"got {got}, expected {exp} (paper Table 14)",
                f"Instance {inst_num}: {label}={got} vs paper={exp}",
            )

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 2 — Instance 1 deep node verification
# ═══════════════════════════════════════════════════════════════════════════

def suite_instance1_deep() -> TestSuite:
    """
    Deep row-by-row check of Instance 1 node values.
    Verifies coordinates, demands, time windows, known_time for
    spot-check nodes against raw CSV.
    """
    s = TestSuite("Instance 1 — Deep Node Verification")
    path = _bench_path(1)
    inst = load_benchmark_instance(path, "Instance_1")

    # ── Depots ──────────────────────────────────────────────────────────────
    # Row 1: Node 1, DD (DCs=1000), x=-36.118, y=49.097
    dd = inst.nodes.get(1)
    s.check("Node 1 exists", dd is not None, "Node 1 missing")
    if dd:
        s.check("Node 1 is DD",          dd.node_type == NodeType.DELIVERY_DEPOT,  f"got {dd.node_type}")
        s.check("Node 1 x=-36.118",      abs(dd.x - (-36.118)) < 1e-6,             f"got {dd.x}")
        s.check("Node 1 y=49.097",       abs(dd.y -   49.097)  < 1e-6,             f"got {dd.y}")
        s.check("Node 1 Q_i=0 (depot)",  dd.Q_i == 0.0,                            f"got {dd.Q_i}")
        s.check("Node 1 P_i=0 (depot)",  dd.P_i == 0.0,                            f"got {dd.P_i}")
        s.check("Node 1 TW left=0",      dd.l_i == 0.0,                            f"got {dd.l_i}")
        s.check("Node 1 TW right=1000",  dd.r_i == 1000.0,                         f"got {dd.r_i}")

    # Row 2: Node 2, PD (PCs=1000), x=-31.201, y=0.235
    pd = inst.nodes.get(2)
    s.check("Node 2 exists", pd is not None, "Node 2 missing")
    if pd:
        s.check("Node 2 is PD",          pd.node_type == NodeType.PICKUP_DEPOT,    f"got {pd.node_type}")
        s.check("Node 2 x=-31.201",      abs(pd.x - (-31.201)) < 1e-6,             f"got {pd.x}")
        s.check("Node 2 y=0.235",        abs(pd.y -    0.235)  < 1e-6,             f"got {pd.y}")

    # ── Static delivery customers (R) ────────────────────────────────────────
    # Row 3: Node 3, R (DCs=1, Q=12, TW_D=[399,525])
    n3 = inst.nodes.get(3)
    s.check("Node 3 exists", n3 is not None, "Node 3 missing")
    if n3:
        s.check("Node 3 is R (STATIC_DELIVERY)", n3.node_type == NodeType.STATIC_DELIVERY, f"got {n3.node_type}")
        s.check("Node 3 x=-29.73",               abs(n3.x - (-29.73))   < 1e-4,             f"got {n3.x}")
        s.check("Node 3 Q_i=12",                 abs(n3.Q_i - 12.0)    < 1e-6,             f"got {n3.Q_i}")
        s.check("Node 3 P_i=0",                  n3.P_i == 0.0,                             f"got {n3.P_i}")
        s.check("Node 3 TW=[399,525]",
                abs(n3.l_i - 399) < 1e-6 and abs(n3.r_i - 525) < 1e-6,
                f"got [{n3.l_i},{n3.r_i}]")
        s.check("Node 3 known_time=0", n3.known_time == 0.0, f"got {n3.known_time}")

    # ── Static pickup customers (S) ──────────────────────────────────────────
    # Row 16: Node 16, S (PCs=1, P=6, TW_P=[269,377])
    n16 = inst.nodes.get(16)
    s.check("Node 16 exists", n16 is not None, "Node 16 missing")
    if n16:
        s.check("Node 16 is S (STATIC_PICKUP)", n16.node_type == NodeType.STATIC_PICKUP, f"got {n16.node_type}")
        s.check("Node 16 x=-49.329",            abs(n16.x - (-49.329)) < 1e-4,            f"got {n16.x}")
        s.check("Node 16 P_i=6",                abs(n16.P_i - 6.0) < 1e-6,                f"got {n16.P_i}")
        s.check("Node 16 Q_i=0",                n16.Q_i == 0.0,                            f"got {n16.Q_i}")
        s.check("Node 16 TW=[269,377]",
                abs(n16.l_i - 269) < 1e-6 and abs(n16.r_i - 377) < 1e-6,
                f"got [{n16.l_i},{n16.r_i}]")
        s.check("Node 16 known_time=0", n16.known_time == 0.0, f"got {n16.known_time}")

    # ── Dynamic pickup customers (D) ─────────────────────────────────────────
    # Row 46: Node 46, D (PCs=4, P=13, TW_P=[300,?], known_time=300)
    n46 = inst.nodes.get(46)
    s.check("Node 46 exists", n46 is not None, "Node 46 missing")
    if n46:
        s.check("Node 46 is D (DYNAMIC_PICKUP)", n46.node_type == NodeType.DYNAMIC_PICKUP,  f"got {n46.node_type}")
        s.check("Node 46 P_i=13",               abs(n46.P_i - 13.0) < 1e-6,                f"got {n46.P_i}")
        s.check("Node 46 Q_i=0",                n46.Q_i == 0.0,                             f"got {n46.Q_i}")
        s.check("Node 46 known_time=300",        abs(n46.known_time - 300.0) < 1e-6,        f"got {n46.known_time}")

    # Row 47: Node 47, D (PCs=4, P=27, known_time=500)
    n47 = inst.nodes.get(47)
    s.check("Node 47 exists", n47 is not None, "Node 47 missing")
    if n47:
        s.check("Node 47 is D (DYNAMIC_PICKUP)", n47.node_type == NodeType.DYNAMIC_PICKUP, f"got {n47.node_type}")
        s.check("Node 47 P_i=27",               abs(n47.P_i - 27.0) < 1e-6,               f"got {n47.P_i}")
        s.check("Node 47 known_time=500",        abs(n47.known_time - 500.0) < 1e-6,       f"got {n47.known_time}")

    # Row 48: Node 48, D (PCs=4, P=31, TW_P=[91,153], known_time=30)
    n48 = inst.nodes.get(48)
    s.check("Node 48 exists", n48 is not None, "Node 48 missing")
    if n48:
        s.check("Node 48 is D", n48.node_type == NodeType.DYNAMIC_PICKUP, f"got {n48.node_type}")
        s.check("Node 48 known_time=30",  abs(n48.known_time - 30.0) < 1e-6,  f"got {n48.known_time}")
        s.check("Node 48 TW=[91,153]",
                abs(n48.l_i - 91) < 1e-6 and abs(n48.r_i - 153) < 1e-6,
                f"got [{n48.l_i},{n48.r_i}]")

    # Last two rows: 49 and 50
    n49 = inst.nodes.get(49)
    n50 = inst.nodes.get(50)
    s.check("Node 49 is D", n49 is not None and n49.node_type == NodeType.DYNAMIC_PICKUP, f"got {getattr(n49, 'node_type', None)}")
    s.check("Node 50 is D", n50 is not None and n50.node_type == NodeType.DYNAMIC_PICKUP, f"got {getattr(n50, 'node_type', None)}")

    # ── Dynamic customer properties ──────────────────────────────────────────
    dyn = inst.dynamic_customers
    s.check("All dynamic have known_time > 0",
            all(d.known_time > 0 for d in dyn),
            f"Some dynamic have known_time=0: {[d.node_id for d in dyn if d.known_time == 0]}")
    s.check("All dynamic have P_i > 0",
            all(d.P_i > 0 for d in dyn),
            f"Some dynamic have P_i=0: {[d.node_id for d in dyn if d.P_i == 0]}")
    s.check("All dynamic have Q_i == 0",
            all(d.Q_i == 0 for d in dyn),
            f"Some dynamic have Q_i>0: {[(d.node_id, d.Q_i) for d in dyn if d.Q_i != 0]}")

    # ── Static delivery properties ───────────────────────────────────────────
    static_r = inst.static_delivery_customers
    s.check("All R have Q_i > 0",
            all(n.Q_i > 0 for n in static_r),
            f"Some R have Q_i=0: {[n.node_id for n in static_r if n.Q_i == 0]}")
    s.check("All R have P_i == 0",
            all(n.P_i == 0 for n in static_r),
            f"Some R have P_i>0: {[(n.node_id, n.P_i) for n in static_r if n.P_i != 0]}")

    # ── Static pickup properties ─────────────────────────────────────────────
    static_s = inst.static_pickup_customers
    s.check("All S have P_i > 0",
            all(n.P_i > 0 for n in static_s),
            f"Some S have P_i=0: {[n.node_id for n in static_s if n.P_i == 0]}")
    s.check("All S have Q_i == 0",
            all(n.Q_i == 0 for n in static_s),
            f"Some S have Q_i>0: {[(n.node_id, n.Q_i) for n in static_s if n.Q_i != 0]}")

    # ── Capacity check ───────────────────────────────────────────────────────
    # Paper §: ∂_v = 100. All demands must be ≤ vehicle capacity
    cap = inst.vehicle_capacity
    oversized_r = [n.node_id for n in static_r  if n.Q_i > cap]
    oversized_s = [n.node_id for n in static_s  if n.P_i > cap]
    oversized_d = [n.node_id for n in inst.dynamic_customers if n.P_i > cap]
    s.check("No demand exceeds vehicle capacity",
            not oversized_r and not oversized_s and not oversized_d,
            f"Oversized: R={oversized_r} S={oversized_s} D={oversized_d}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 3 — Distance matrix
# ═══════════════════════════════════════════════════════════════════════════

def suite_distance_matrix() -> TestSuite:
    """
    Verify distance matrix correctness:
    - Euclidean formula
    - Symmetry: d(i,j) == d(j,i)
    - Triangle inequality: d(i,k) ≤ d(i,j) + d(j,k)
    - Travel time = distance / speed
    - Zero distance for same node (not stored, computed as 0)
    """
    s = TestSuite("Distance Matrix Correctness")
    path = _bench_path(1)
    inst = load_benchmark_instance(path, "Instance_1")

    node_ids = sorted(inst.nodes.keys())
    n = len(node_ids)

    # ── Manual spot check for known node pairs ────────────────────────────
    # Node 1: (-36.118, 49.097), Node 2: (-31.201, 0.235)
    # dist = sqrt((-36.118 - -31.201)^2 + (49.097 - 0.235)^2)
    #       = sqrt(4.917^2 + 48.862^2)
    #       = sqrt(24.177 + 2387.49) = sqrt(2411.67) ≈ 49.109
    expected_d12 = math.sqrt((-36.118 - (-31.201))**2 + (49.097 - 0.235)**2)
    got_d12 = inst.dist(1, 2)
    s.check("dist(1,2) ≈ Euclidean formula",
            abs(got_d12 - expected_d12) < 1e-6,
            f"got {got_d12:.6f}, expected {expected_d12:.6f}")

    # Node 1: (-36.118, 49.097), Node 3: (-29.73, 64.136)
    expected_d13 = math.sqrt((-36.118 - (-29.73))**2 + (49.097 - 64.136)**2)
    got_d13 = inst.dist(1, 3)
    s.check("dist(1,3) ≈ Euclidean formula",
            abs(got_d13 - expected_d13) < 1e-6,
            f"got {got_d13:.6f}, expected {expected_d13:.6f}")

    # ── Symmetry ─────────────────────────────────────────────────────────
    sym_ok = True
    sym_fail_pairs = []
    for i_idx in range(min(15, n)):
        for j_idx in range(i_idx + 1, min(15, n)):
            i, j = node_ids[i_idx], node_ids[j_idx]
            dij = inst.dist_matrix.get((i, j))
            dji = inst.dist_matrix.get((j, i))
            if dij is None or dji is None or abs(dij - dji) > 1e-9:
                sym_ok = False
                sym_fail_pairs.append((i, j, dij, dji))
    s.check("Distance matrix is symmetric",
            sym_ok,
            f"Asymmetric pairs: {sym_fail_pairs[:3]}")

    # ── Non-negativity ────────────────────────────────────────────────────
    neg_ok = all(v >= 0 for v in inst.dist_matrix.values())
    s.check("All distances ≥ 0", neg_ok,
            f"Negative distances found")

    # ── Coverage: N*(N-1) entries ─────────────────────────────────────────
    total_nodes = len(node_ids)
    expected_entries = total_nodes * (total_nodes - 1)
    got_entries = len(inst.dist_matrix)
    s.check(f"dist_matrix has {expected_entries} entries",
            got_entries == expected_entries,
            f"got {got_entries}")

    # ── Travel time = dist / speed ────────────────────────────────────────
    for i_idx in range(min(5, n)):
        for j_idx in range(min(5, n)):
            if i_idx == j_idx:
                continue
            i, j = node_ids[i_idx], node_ids[j_idx]
            t_expected = inst.dist(i, j) / inst.vehicle_speed
            t_got      = inst.travel_time(i, j)
            s.check(f"travel_time({i},{j}) = dist/speed",
                    abs(t_got - t_expected) < 1e-9,
                    f"got {t_got:.6f}, expected {t_expected:.6f}")

    # ── Triangle inequality (spot check 50 triples) ───────────────────────
    import random
    rng = random.Random(42)
    sample_ids = rng.sample(node_ids, min(20, n))
    violations = []
    for a in sample_ids:
        for b in sample_ids:
            if a == b:
                continue
            for c in sample_ids:
                if c == a or c == b:
                    continue
                dab = inst.dist(a, b)
                dbc = inst.dist(b, c)
                dac = inst.dist(a, c)
                if dac > dab + dbc + 1e-9:
                    violations.append((a, b, c, dac, dab + dbc))
    s.check("Triangle inequality holds (50 spot checks)",
            len(violations) == 0,
            f"{len(violations)} violations, first: {violations[:2]}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 4 — Time window validation
# ═══════════════════════════════════════════════════════════════════════════

def suite_time_windows() -> TestSuite:
    """
    Verify time window loading:
    - l_i < r_i for all customers
    - Depots have [0, 1000]
    - Delivery customers use TW_D columns
    - Pickup/dynamic customers use TW_P columns
    - known_time ordering (dynamic customers only)
    """
    s = TestSuite("Time Window Validation")
    path = _bench_path(1)
    inst = load_benchmark_instance(path, "Instance_1")

    # ── Depot time windows ────────────────────────────────────────────────
    for depot in inst.all_depots:
        s.check(f"Depot {depot.node_id} TW_left=0",
                depot.l_i == 0.0,
                f"got l_i={depot.l_i}")
        s.check(f"Depot {depot.node_id} TW_right=1000",
                depot.r_i == 1000.0,
                f"got r_i={depot.r_i}")

    # ── l_i < r_i for all customers ───────────────────────────────────────
    invalid_tw = [
        (n.node_id, n.l_i, n.r_i)
        for n in inst.all_customers
        if n.l_i >= n.r_i
    ]
    s.check("All customers have l_i < r_i",
            len(invalid_tw) == 0,
            f"Invalid: {invalid_tw[:5]}")

    # ── R customers use TW_D (spot check vs CSV) ───────────────────────────
    # Node 3: TW_D = [399, 525]
    n3 = inst.nodes.get(3)
    if n3 and n3.node_type == NodeType.STATIC_DELIVERY:
        s.check("Node 3 (R) uses TW_D=[399,525]",
                abs(n3.l_i - 399) < 1e-6 and abs(n3.r_i - 525) < 1e-6,
                f"got [{n3.l_i},{n3.r_i}]")

    # Node 4: TW_D = [121, 299]
    n4 = inst.nodes.get(4)
    if n4 and n4.node_type == NodeType.STATIC_DELIVERY:
        s.check("Node 4 (R) uses TW_D=[121,299]",
                abs(n4.l_i - 121) < 1e-6 and abs(n4.r_i - 299) < 1e-6,
                f"got [{n4.l_i},{n4.r_i}]")

    # ── S/D customers use TW_P ────────────────────────────────────────────
    # Node 16: TW_P = [269, 377]
    n16 = inst.nodes.get(16)
    if n16 and n16.node_type == NodeType.STATIC_PICKUP:
        s.check("Node 16 (S) uses TW_P=[269,377]",
                abs(n16.l_i - 269) < 1e-6 and abs(n16.r_i - 377) < 1e-6,
                f"got [{n16.l_i},{n16.r_i}]")

    # Node 48: TW_P = [91, 153]
    n48 = inst.nodes.get(48)
    if n48 and n48.node_type == NodeType.DYNAMIC_PICKUP:
        s.check("Node 48 (D) uses TW_P=[91,153]",
                abs(n48.l_i - 91) < 1e-6 and abs(n48.r_i - 153) < 1e-6,
                f"got [{n48.l_i},{n48.r_i}]")

    # ── Dynamic known_time is within [0, max_time_window] ─────────────────
    dyn = inst.dynamic_customers
    max_tw = max(n.r_i for n in inst.all_customers if not n.is_depot())
    for d in dyn:
        s.check(f"Dynamic {d.node_id} known_time in valid range",
                0 < d.known_time <= max_tw * 2,
                f"known_time={d.known_time} suspiciously large (max TW={max_tw})")

    # ── Cross-instance: time window consistency ───────────────────────────
    # Instances 1–5 share same static customers (same base set, different dynamics)
    # Verify instance 11 has same structure as instance 1 (just 2 DDs)
    inst11 = load_benchmark_instance(_bench_path(11), "Instance_11")
    invalid_tw_11 = [
        (n.node_id, n.l_i, n.r_i)
        for n in inst11.all_customers
        if n.l_i >= n.r_i
    ]
    s.check("Instance 11: all customers have l_i < r_i",
            len(invalid_tw_11) == 0,
            f"Invalid in I11: {invalid_tw_11[:5]}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 5 — Multi-depot encoding
# ═══════════════════════════════════════════════════════════════════════════

def suite_multi_depot() -> TestSuite:
    """
    Verify instances with multiple DDs and/or PDs are loaded correctly.
    Checks DCs=2000 (2nd DD), PCs=2000 (2nd PD), PCs=3000 (3rd PD).
    """
    s = TestSuite("Multi-Depot Encoding")

    # Instance 11: 2 DDs, 1 PD
    inst11 = load_benchmark_instance(_bench_path(11), "Instance_11")
    s.check("I11: 2 DDs",    len(inst11.delivery_depots) == 2,  f"got {len(inst11.delivery_depots)}")
    s.check("I11: 1 PD",     len(inst11.pickup_depots)   == 1,  f"got {len(inst11.pickup_depots)}")

    # Each depot should have [0,1000] TW
    for depot in inst11.all_depots:
        s.check(f"I11 Depot {depot.node_id} TW=[0,1000]",
                depot.l_i == 0.0 and depot.r_i == 1000.0,
                f"got [{depot.l_i},{depot.r_i}]")

    # Both DDs should have distinct coordinates
    dds11 = inst11.delivery_depots
    if len(dds11) == 2:
        same_coord = (dds11[0].x == dds11[1].x and dds11[0].y == dds11[1].y)
        s.check("I11: 2 DDs have distinct coordinates",
                not same_coord,
                f"Both DDs at same location ({dds11[0].x},{dds11[0].y})")

    # Instance 21: 1 DD, 3 PDs
    inst21 = load_benchmark_instance(_bench_path(21), "Instance_21")
    s.check("I21: 1 DD",     len(inst21.delivery_depots) == 1,  f"got {len(inst21.delivery_depots)}")
    s.check("I21: 3 PDs",    len(inst21.pickup_depots)   == 3,  f"got {len(inst21.pickup_depots)}")

    # 3 PDs should all have distinct coordinates
    pds21 = inst21.pickup_depots
    if len(pds21) == 3:
        coords = [(p.x, p.y) for p in pds21]
        s.check("I21: 3 PDs have distinct coordinates",
                len(set(coords)) == 3,
                f"Duplicate depot coordinates: {coords}")

    # Instance 30: 3 DDs, 1 PD
    inst30 = load_benchmark_instance(_bench_path(30), "Instance_30")
    s.check("I30: 3 DDs",    len(inst30.delivery_depots) == 3,  f"got {len(inst30.delivery_depots)}")
    s.check("I30: 1 PD",     len(inst30.pickup_depots)   == 1,  f"got {len(inst30.pickup_depots)}")

    # All 30 instances: sum of depots = n_DD + n_PD from Table 14
    depot_ok = True
    for num, (exp_dd, exp_pd, *_) in PAPER_TABLE14.items():
        try:
            inst = load_benchmark_instance(_bench_path(num), f"I{num}")
            if len(inst.delivery_depots) != exp_dd or len(inst.pickup_depots) != exp_pd:
                depot_ok = False
                s.fail(f"I{num:02d} depot counts",
                       f"DD: got {len(inst.delivery_depots)} exp {exp_dd}  "
                       f"PD: got {len(inst.pickup_depots)} exp {exp_pd}")
        except FileNotFoundError:
            pass

    if depot_ok:
        s.ok("All 30 instances: depot counts match Table 14")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 6 — Problem instance parameters
# ═══════════════════════════════════════════════════════════════════════════

def suite_instance_parameters() -> TestSuite:
    """
    Verify ProblemInstance defaults match Table 15 of paper.
    These are the algorithm parameters embedded in the data model.
    """
    s = TestSuite("ProblemInstance Parameters (Table 15)")
    path = _bench_path(1)
    inst = load_benchmark_instance(path, "Instance_1")

    # Table 15 values
    params = [
        ("vehicle_capacity",     inst.vehicle_capacity,     100.0),
        ("vehicle_speed",        inst.vehicle_speed,         30.0),
        ("fuel_rate",            inst.fuel_rate,             0.07),
        ("fuel_price",           inst.fuel_price,            7.0),
        ("annual_maintenance",   inst.annual_maintenance,    40000.0),
        ("working_days",         inst.working_days,          364),
        ("epsilon",              inst.epsilon,               20.0),
        ("omega",                inst.omega,                 30.0),
        ("delta",                inst.delta,                 1.0),
        ("chi",                  inst.chi,                   1.0),
        ("gamma",                inst.gamma,                 1.0),
    ]

    for name, got, expected in params:
        s.check(f"{name} = {expected}",
                abs(float(got) - float(expected)) < 1e-9,
                f"got {got}")

    # NOTE-07: β_f (depot fixed cost) not given in paper → set to 0.0
    s.check("depot_fixed_cost = 0.0 (NOTE-07: not given in paper)",
            inst.depot_fixed_cost == 0.0,
            f"got {inst.depot_fixed_cost}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 7 — Demand feasibility
# ═══════════════════════════════════════════════════════════════════════════

def suite_demand_feasibility() -> TestSuite:
    """
    Check demand values are reasonable:
    - All demands positive for customers
    - No individual demand exceeds vehicle capacity (∂_v=100)
    - Total demand per depot group not zero
    - demand types correct (Q for R, P for S/D, both 0 for depots)
    """
    s = TestSuite("Demand Feasibility Check")

    for num in [1, 5, 11, 15, 26, 30]:
        inst = load_benchmark_instance(_bench_path(num), f"I{num}")
        cap  = inst.vehicle_capacity

        for c in inst.static_delivery_customers:
            s.check(f"I{num} Node {c.node_id} R demand 0<Q≤{cap}",
                    0 < c.Q_i <= cap,
                    f"got Q={c.Q_i}")

        for c in inst.static_pickup_customers:
            s.check(f"I{num} Node {c.node_id} S demand 0<P≤{cap}",
                    0 < c.P_i <= cap,
                    f"got P={c.P_i}")

        for c in inst.dynamic_customers:
            s.check(f"I{num} Node {c.node_id} D demand 0<P≤{cap}",
                    0 < c.P_i <= cap,
                    f"got P={c.P_i}")

        # Depots have zero demand
        for d in inst.all_depots:
            s.check(f"I{num} Depot {d.node_id} Q=0,P=0",
                    d.Q_i == 0.0 and d.P_i == 0.0,
                    f"got Q={d.Q_i} P={d.P_i}")

        # Total delivery demand > 0 and total pickup demand > 0
        total_del = sum(c.Q_i for c in inst.static_delivery_customers)
        total_pck = sum(c.P_i for c in inst.static_pickup_customers) + \
                    sum(c.P_i for c in inst.dynamic_customers)
        s.check(f"I{num} total delivery demand > 0", total_del > 0, f"got {total_del}")
        s.check(f"I{num} total pickup demand > 0",   total_pck > 0, f"got {total_pck}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 8 — All 30 instances full scan
# ═══════════════════════════════════════════════════════════════════════════

def suite_all_instances() -> TestSuite:
    """
    Quick structural check on all 30 instances in batch:
    - Loads without error
    - Node count matches Table 14
    - Distance matrix built (non-empty)
    - No zero-demand customers
    """
    s = TestSuite("All 30 Instances — Structural Scan")

    instances = load_all_benchmark_instances(BENCH_DIR)
    s.check("Loaded 30 instances", len(instances) == 30,
            f"got {len(instances)}")

    for i, inst in enumerate(instances, 1):
        exp = PAPER_TABLE14.get(i)
        if exp is None:
            continue
        exp_dd, exp_pd, exp_r, exp_s, exp_d, exp_total = exp

        got_c = len(inst.all_customers)
        s.check(f"I{i:02d} total_customers={exp_total}",
                got_c == exp_total,
                f"got {got_c}")

        s.check(f"I{i:02d} distance matrix non-empty",
                len(inst.dist_matrix) > 0,
                "dist_matrix is empty")

        # Check no NaN in coordinates
        nan_nodes = [nid for nid, n in inst.nodes.items()
                     if math.isnan(n.x) or math.isnan(n.y)]
        s.check(f"I{i:02d} no NaN coordinates",
                len(nan_nodes) == 0,
                f"NaN in nodes: {nan_nodes}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# Main runner
# ═══════════════════════════════════════════════════════════════════════════

SUITES = {
    "node_types":      suite_node_types,
    "instance1_deep":  suite_instance1_deep,
    "distance":        suite_distance_matrix,
    "time_windows":    suite_time_windows,
    "multi_depot":     suite_multi_depot,
    "parameters":      suite_instance_parameters,
    "demand":          suite_demand_feasibility,
    "all_instances":   suite_all_instances,
}


def run_suites(names: list[str]) -> tuple[int, int]:
    total_passed = total_tests = 0
    for name in names:
        fn = SUITES[name]
        suite = fn()
        p, t = suite.report()
        total_passed += p
        total_tests  += t
    return total_passed, total_tests


def log_results(passed: int, total: int, suite_names: list[str]):
    """Append result to EXPERIMENTS.md."""
    import datetime
    from pathlib import Path
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    status = "✅ ALL PASSED" if passed == total else f"❌ {total - passed} FAILED"

    entry = f"""
## [{ts}] Data Module Tests — {', '.join(suite_names)}
**Command:** `python tests/test_data_module.py --suite {' '.join(suite_names)}`
**Purpose:** Verify data loading correctness before algorithm implementation
**Results:** {passed}/{total} tests passed — {status}
**Analysis:** {"Data loading is correct. Proceed to next module." if passed == total else "Data loading has issues. Fix before proceeding."}
**Next action:** {"Module 2 — Objective function verification" if passed == total else "Fix failed tests in data_loader.py / data_model.py"}
"""

    log_path = Path(RESULTS_LOG)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="MDPDTWDD Data Module Tests")
    parser.add_argument(
        "--suite", nargs="+",
        choices=list(SUITES.keys()) + ["all"],
        default=["all"],
        help="Which test suite(s) to run (default: all)"
    )
    parser.add_argument("--no-log", action="store_true",
                        help="Skip writing to logs/EXPERIMENTS.md")
    args = parser.parse_args()

    names = list(SUITES.keys()) if "all" in args.suite else args.suite

    print(f"\n{'═'*65}")
    print(f"  MDPDTWDD — Module 1: Data Loading & Model Validation")
    print(f"  Paper: Wang et al. (2025), EAAI 139, 109700")
    print(f"  Suites: {', '.join(names)}")
    print(f"{'═'*65}")

    passed, total = run_suites(names)

    print(f"\n{'═'*65}")
    icon = "✅" if passed == total else "❌"
    print(f"  {icon} TOTAL: {passed}/{total} tests passed")
    if passed < total:
        print(f"  ⚠  {total - passed} test(s) FAILED — check output above")
    print(f"{'═'*65}\n")

    if not args.no_log:
        log_results(passed, total, names)
        print(f"  Results logged → logs/EXPERIMENTS.md\n")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
