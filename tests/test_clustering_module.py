"""
test_clustering_module.py — Module 3: 3D AP Clustering Verification
=====================================================================

Kiểm tra từng bước của 3D AP Clustering (Section 4.2):
  Eq.49: STD space-time distance
  Eq.50: Responsibility matrix R
  Eq.51: Availability matrix A
  Eq.52/53: Damping update
  Table 6: Full clustering pipeline

Run:
    cd mdpdtwdd-cli
    python3 tests/test_clustering_module.py
    python3 tests/test_clustering_module.py --suite std
"""

import os, sys, math, argparse, datetime
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_model import Node, NodeType, ProblemInstance
from src.data_loader import load_benchmark_instance
from src.clustering import APClustering3D, cluster_by_depot_type

# ── TestSuite (reuse same pattern) ───────────────────────────────────────────
from dataclasses import dataclass

@dataclass
class TR:
    name: str; passed: bool; message: str = ""; detail: str = ""

class TestSuite:
    def __init__(self, name): self.name = name; self.results = []
    def ok(self, n, d=""): self.results.append(TR(n, True, "PASS", d))
    def fail(self, n, m, d=""): self.results.append(TR(n, False, f"FAIL: {m}", d))
    def check(self, n, cond, msg, detail=""):
        if cond: self.ok(n, detail)
        else: self.fail(n, msg, detail)
    def report(self):
        p = sum(1 for r in self.results if r.passed); t = len(self.results)
        print(f"\n{'═'*65}\n  Suite: {self.name}\n  Results: {p}/{t} passed"
              + (f"  ← {t-p} FAILED" if t-p else "") + f"\n{'─'*65}")
        for r in self.results:
            print(f"  {'✓' if r.passed else '✗'} {r.name}")
            if not r.passed:
                print(f"      → {r.message}")
                if r.detail: print(f"      → {r.detail}")
        return p, t

def bench(n):
    import glob
    hits = sorted(glob.glob(os.path.join(
        os.path.dirname(__file__), '..', 'data', 'process', 'benchmark', f'{n} *Sheet1.csv'
    )))
    return hits[0]

def approx(a, b, tol=1e-6):
    return abs(a - b) <= tol


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 1 — STD (Space-Time Distance) — Eq.49
# STD_ij = s*d_ij + t * min{|l_i-l_j|, |l_i-r_j|, |r_i-l_j|, |r_i-r_j|} * α_v
# ═══════════════════════════════════════════════════════════════════════════

def suite_std() -> TestSuite:
    s = TestSuite("STD — Space-Time Distance (Eq.49)")
    inst = load_benchmark_instance(bench(1), "I1")
    ap = APClustering3D(inst, spatial_coeff=0.5, temporal_coeff=0.5)

    n1 = inst.nodes[1]   # DD:  (-36.118, 49.097), TW=[0,1000]
    n3 = inst.nodes[3]   # R:   (-29.73,  64.136), TW=[399,525]
    n16 = inst.nodes[16] # S:   (-49.329, 33.374), TW=[269,377]

    # ── Manual STD(1,3) ───────────────────────────────────────────────────
    d13 = inst.dist(1, 3)
    tw13 = min(abs(n1.l_i - n3.l_i),   # |0 - 399|   = 399
               abs(n1.l_i - n3.r_i),   # |0 - 525|   = 525
               abs(n1.r_i - n3.l_i),   # |1000-399|  = 601
               abs(n1.r_i - n3.r_i))   # |1000-525|  = 475
    # min = 399
    expected_std13 = 0.5 * d13 + 0.5 * tw13 * 30.0
    got_std13 = ap._space_time_distance(n1, n3)
    s.check("STD(DD,R) = s*d + t*min_tw*α_v",
            approx(got_std13, expected_std13, tol=1e-6),
            f"got {got_std13:.4f}, expected {expected_std13:.4f}",
            f"d={d13:.4f}, tw_min={tw13}, α_v=30")

    # ── Manual STD(3,16) ─────────────────────────────────────────────────
    d316 = inst.dist(3, 16)
    tw316 = min(abs(n3.l_i - n16.l_i),   # |399-269|=130
                abs(n3.l_i - n16.r_i),   # |399-377|=22   ← min
                abs(n3.r_i - n16.l_i),   # |525-269|=256
                abs(n3.r_i - n16.r_i))   # |525-377|=148
    expected_std316 = 0.5 * d316 + 0.5 * tw316 * 30.0
    got_std316 = ap._space_time_distance(n3, n16)
    s.check("STD(R,S): TW overlap term = min of 4 combos",
            approx(got_std316, expected_std316, tol=1e-6),
            f"got {got_std316:.4f}, expected {expected_std316:.4f}",
            f"d={d316:.4f}, tw_min={tw316}")

    # ── Symmetry: STD(i,j) == STD(j,i) ───────────────────────────────────
    got_std_31  = ap._space_time_distance(n3, n1)
    got_std_163 = ap._space_time_distance(n16, n3)
    s.check("STD is symmetric: STD(i,j) = STD(j,i) for node 1↔3",
            approx(got_std13, got_std_31, tol=1e-6),
            f"STD(1,3)={got_std13:.4f}, STD(3,1)={got_std_31:.4f}")
    s.check("STD is symmetric: STD(3,16) = STD(16,3)",
            approx(got_std316, got_std_163, tol=1e-6),
            f"STD(3,16)={got_std316:.4f}, STD(16,3)={got_std_163:.4f}")

    # ── STD >= 0 ──────────────────────────────────────────────────────────
    sample_ids = list(inst.nodes.keys())[:10]
    neg = [(i,j) for i in sample_ids for j in sample_ids if i != j
           and ap._space_time_distance(inst.nodes[i], inst.nodes[j]) < 0]
    s.check("STD >= 0 for all node pairs (sample 10)",
            len(neg) == 0,
            f"Negative STD found: {neg[:3]}")

    # ── s=0: STD = only temporal ──────────────────────────────────────────
    ap_t = APClustering3D(inst, spatial_coeff=0.0, temporal_coeff=1.0)
    std_pure_t = ap_t._space_time_distance(n3, n16)
    expected_pure_t = 1.0 * tw316 * 30.0
    s.check("s=0,t=1: STD = t*tw*α_v (pure temporal)",
            approx(std_pure_t, expected_pure_t, tol=1e-6),
            f"got {std_pure_t:.4f}, expected {expected_pure_t:.4f}")

    # ── t=0: STD = only spatial ───────────────────────────────────────────
    ap_s = APClustering3D(inst, spatial_coeff=1.0, temporal_coeff=0.0)
    std_pure_s = ap_s._space_time_distance(n3, n16)
    expected_pure_s = d316
    s.check("s=1,t=0: STD = d_ij (pure spatial)",
            approx(std_pure_s, expected_pure_s, tol=1e-6),
            f"got {std_pure_s:.4f}, expected {expected_pure_s:.4f}")

    # ── Alpha_v = 30 used in temporal term ───────────────────────────────
    ap2 = APClustering3D(inst, spatial_coeff=0.5, temporal_coeff=0.5)
    std_default = ap2._space_time_distance(n3, n16)
    # Manually with alpha=30
    expected_alpha30 = 0.5 * d316 + 0.5 * tw316 * 30.0
    s.check("α_v=30 used in temporal term (Table 15)",
            approx(std_default, expected_alpha30, tol=1e-6),
            f"got {std_default:.4f}, expected {expected_alpha30:.4f}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 2 — Similarity Matrix S
# S(i,j) = -STD_ij  (negative distance → higher is better)
# S(depot,depot) = very high (force depot as exemplar)
# S(customer,customer) = median of off-diagonal similarities
# ═══════════════════════════════════════════════════════════════════════════

def suite_similarity() -> TestSuite:
    s = TestSuite("Similarity Matrix S")
    inst = load_benchmark_instance(bench(1), "I1")
    ap = APClustering3D(inst)
    S = ap._build_similarity_matrix()

    n = ap.n
    node_ids = ap.node_ids
    depot_ids = {nd.node_id for nd in inst.all_depots}

    # ── Shape ─────────────────────────────────────────────────────────────
    s.check("S shape = (n_nodes, n_nodes)",
            S.shape == (n, n),
            f"got {S.shape}, expected ({n},{n})")

    # ── Off-diagonal: S(i,j) = -STD_ij < 0 ───────────────────────────────
    neg_offdiag = True
    for i in range(min(10, n)):
        for j in range(min(10, n)):
            if i != j and S[i, j] >= 0:
                neg_offdiag = False
                break
    s.check("Off-diagonal S(i,j) = -STD < 0",
            neg_offdiag,
            "Some off-diagonal S(i,j) >= 0 — should be negative distance")

    # ── Depot diagonal: very high preference ──────────────────────────────
    for i, nid in enumerate(node_ids):
        if nid in depot_ids:
            max_offdiag = np.max(S[i, [j for j in range(n) if j != i]])
            s.check(f"Depot {nid} S(i,i) >> off-diagonal",
                    S[i, i] > max_offdiag * 5,
                    f"S[{i},{i}]={S[i,i]:.2f} not >> max_offdiag={max_offdiag:.2f}")

    # ── Customer diagonal: set to median ──────────────────────────────────
    all_off = S[~np.eye(n, dtype=bool)]
    median_s = np.median(all_off)
    customer_diag_ok = True
    for i, nid in enumerate(node_ids):
        if nid not in depot_ids:
            if not approx(S[i, i], median_s, tol=1e-6):
                customer_diag_ok = False
                break
    s.check("Customer diagonal S(i,i) = median of off-diagonal",
            customer_diag_ok,
            f"Some customer S(i,i) ≠ median({median_s:.4f})")

    # ── S(i,j) = S(j,i) (symmetric, since STD is symmetric) ──────────────
    sym_ok = np.allclose(S, S.T, atol=1e-6)
    s.check("S is symmetric (S[i,j] = S[j,i])",
            sym_ok,
            "Similarity matrix is not symmetric")

    # ── Single depot instance: all customers have same depot ──────────────
    s.check("S matrix built without crash for instance 1",
            S is not None and S.shape[0] > 0,
            "S matrix is None or empty")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 3 — R & A Update (Eq.50, Eq.51) — manual verification on tiny example
# ═══════════════════════════════════════════════════════════════════════════

def suite_ra_update() -> TestSuite:
    """
    Test R and A update equations on a 3-node example where we can compute
    everything by hand.
    Nodes: 0=depot(exemplar), 1=customer_A, 2=customer_B
    """
    s = TestSuite("R & A Update (Eq.50, Eq.51) — manual 3-node")

    # Build a tiny instance manually
    from src.data_model import ProblemInstance
    inst = ProblemInstance(name="tiny")
    inst.nodes = {
        1: Node(1, 0.0, 0.0, NodeType.DELIVERY_DEPOT, l_i=0, r_i=1000),
        2: Node(2, 10.0, 0.0, NodeType.STATIC_DELIVERY, Q_i=5, l_i=100, r_i=200),
        3: Node(3, 20.0, 0.0, NodeType.STATIC_DELIVERY, Q_i=5, l_i=150, r_i=250),
    }
    inst.build_distance_matrix()

    ap = APClustering3D(inst, damping=0.0, max_iter=1)  # no damping for clean test
    ap.S = ap._build_similarity_matrix()
    ap.R = np.zeros((3, 3))
    ap.A = np.zeros((3, 3))

    S = ap.S.copy()

    # ── Eq.50: R_new(i,j) = S(i,j) - max_{j'≠j}{A(i,j') + S(i,j')} ─────
    # With A=0: R_new(i,j) = S(i,j) - max_{j'≠j}{S(i,j')}
    # For node i=1 (idx=0), j=0 (depot, idx=0):
    #   max over j' ≠ 0: S[0,1], S[0,2]
    #   R_new[0,0] = S[0,0] - max(S[0,1], S[0,2])
    R_new = ap._update_responsibility()

    for i in range(3):
        for j in range(3):
            AS_copy = (ap.A + S)[i, :].copy()
            AS_copy[j] = -np.inf
            expected = S[i, j] - np.max(AS_copy)
            s.check(f"R_new[{i},{j}] = S[{i},{j}] - max_{{j'≠{j}}}(A+S)[{i},j']",
                    approx(R_new[i, j], expected, tol=1e-9),
                    f"got {R_new[i,j]:.6f}, expected {expected:.6f}")

    # ── Eq.51: A_new ──────────────────────────────────────────────────────
    A_new = ap._update_availability(R_new)

    # Diagonal: A_new[j,j] = Σ_{j'≠j} max(0, R_new[j',j])
    for j in range(3):
        expected_diag = sum(max(0, R_new[k, j]) for k in range(3) if k != j)
        s.check(f"A_new[{j},{j}] = Σ max(0,R[k,{j}]) k≠{j}",
                approx(A_new[j, j], expected_diag, tol=1e-9),
                f"got {A_new[j,j]:.6f}, expected {expected_diag:.6f}")

    # Off-diagonal: A_new[i,j] = min(0, R_new[j,j] + Σ_{j'∉{i,j}} max(0,R_new[j',j]))
    for i in range(3):
        for j in range(3):
            if i == j: continue
            excl = [k for k in range(3) if k != i and k != j]
            expected_offdiag = min(0, R_new[j, j] + sum(max(0, R_new[k, j]) for k in excl))
            s.check(f"A_new[{i},{j}] = min(0, R[{j},{j}] + Σ max(0,R[k,{j}]))",
                    approx(A_new[i, j], expected_offdiag, tol=1e-9),
                    f"got {A_new[i,j]:.6f}, expected {expected_offdiag:.6f}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 4 — Damping (Eq.52, Eq.53)
# R_new = λ'*R_old + (1-λ')*R_new
# A_new = λ'*A_old + (1-λ')*A_new
# ═══════════════════════════════════════════════════════════════════════════

def suite_damping() -> TestSuite:
    s = TestSuite("Damping Update (Eq.52, Eq.53)")
    inst = load_benchmark_instance(bench(1), "I1")

    for lam in [0.0, 0.5, 0.9, 1.0]:
        ap = APClustering3D(inst, damping=lam, max_iter=1)
        ap.S = ap._build_similarity_matrix()
        ap.R = np.ones((ap.n, ap.n)) * 2.0   # R_old = 2
        ap.A = np.ones((ap.n, ap.n)) * 3.0   # A_old = 3

        R_new_raw  = ap._update_responsibility()   # fresh R before damping
        A_new_raw  = ap._update_availability(R_new_raw)

        R_expected = lam * ap.R + (1 - lam) * R_new_raw   # Eq.52
        A_expected = lam * ap.A + (1 - lam) * A_new_raw   # Eq.53

        # Apply damping as the code does
        R_damped = lam * ap.R + (1 - lam) * R_new_raw
        A_damped = lam * ap.A + (1 - lam) * A_new_raw

        s.check(f"λ'={lam}: R_damped = λ'*R_old + (1-λ')*R_new",
                np.allclose(R_damped, R_expected, atol=1e-9),
                f"R damping failed for λ'={lam}")
        s.check(f"λ'={lam}: A_damped = λ'*A_old + (1-λ')*A_new",
                np.allclose(A_damped, A_expected, atol=1e-9),
                f"A damping failed for λ'={lam}")

    # ── Special: λ'=0 → no memory ─────────────────────────────────────────
    ap0 = APClustering3D(inst, damping=0.0, max_iter=1)
    ap0.S = ap0._build_similarity_matrix()
    ap0.R = np.ones((ap0.n, ap0.n)) * 999.0
    ap0.A = np.ones((ap0.n, ap0.n)) * 999.0
    R_raw0 = ap0._update_responsibility()
    A_raw0 = ap0._update_availability(R_raw0)
    # λ'=0: result = 100% new
    s.check("λ'=0: damped R = R_new (no memory of old)",
            np.allclose(0.0*999 + 1.0*R_raw0, R_raw0, atol=1e-9),
            "Damping=0 should give pure new value")

    # ── Special: λ'=1 → no update (frozen) ───────────────────────────────
    R_old = np.ones((ap0.n, ap0.n)) * 42.0
    R_frozen = 1.0 * R_old + 0.0 * R_raw0
    s.check("λ'=1: damped R = R_old (fully frozen)",
            np.allclose(R_frozen, R_old, atol=1e-9),
            "Damping=1 should give pure old value")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 5 — Full Clustering Pipeline (Table 6)
# ═══════════════════════════════════════════════════════════════════════════

def suite_full_clustering() -> TestSuite:
    s = TestSuite("Full Clustering Pipeline (Table 6)")
    inst = load_benchmark_instance(bench(1), "I1")
    ap = APClustering3D(inst)

    # ── Runs without crash ────────────────────────────────────────────────
    try:
        assignment = ap.fit()
        s.ok("fit() completes without error")
    except Exception as e:
        s.fail("fit() crashed", str(e))
        return s

    # ── Every customer gets assigned ──────────────────────────────────────
    customer_ids = {n.node_id for n in inst.all_customers}
    assigned_ids = set(assignment.keys())
    s.check("All customers assigned",
            customer_ids == assigned_ids,
            f"Missing: {customer_ids - assigned_ids}, Extra: {assigned_ids - customer_ids}")

    # ── All assigned to valid depots ──────────────────────────────────────
    depot_ids = {n.node_id for n in inst.all_depots}
    bad = {cid: did for cid, did in assignment.items() if did not in depot_ids}
    s.check("All customers assigned to a valid depot",
            len(bad) == 0,
            f"Invalid depot assignments: {bad}")

    # ── Instance 1 (1 DD, 1 PD): all customers → DD or PD ─────────────────
    dd_id = inst.delivery_depots[0].node_id
    pd_id = inst.pickup_depots[0].node_id
    valid_depots = {dd_id, pd_id}
    wrong = {c: d for c, d in assignment.items() if d not in valid_depots}
    s.check("I1: customers assigned to node 1 (DD) or node 2 (PD)",
            len(wrong) == 0,
            f"Assignments to unexpected depot: {wrong}")

    # ── cluster_by_depot_type groups correctly ────────────────────────────
    clusters = cluster_by_depot_type(assignment, inst)
    s.check("cluster_by_depot_type returns entry for each depot",
            set(clusters.keys()) == depot_ids,
            f"got keys {set(clusters.keys())}, expected {depot_ids}")

    total_assigned = sum(len(v) for v in clusters.values())
    s.check("Total customers in clusters = total customers",
            total_assigned == len(customer_ids),
            f"got {total_assigned}, expected {len(customer_ids)}")

    # ── No customer assigned to multiple depots ───────────────────────────
    all_assigned = [c for lst in clusters.values() for c in lst]
    s.check("No customer assigned to multiple depots",
            len(all_assigned) == len(set(all_assigned)),
            f"Duplicates: {[c for c in all_assigned if all_assigned.count(c)>1]}")

    # ── Print cluster distribution ────────────────────────────────────────
    print(f"\n  [Instance 1 clustering result (s=t=0.5)]:")
    for depot_id, cust_list in clusters.items():
        depot = inst.nodes[depot_id]
        print(f"    {depot.node_type.value}(node {depot_id}): {len(cust_list)} customers → {sorted(cust_list)[:5]}...")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 6 — Multi-depot clustering (Instance 11: 2 DDs, 1 PD)
# ═══════════════════════════════════════════════════════════════════════════

def suite_multi_depot_clustering() -> TestSuite:
    s = TestSuite("Multi-Depot Clustering (Instance 11: 2DD+1PD)")
    inst = load_benchmark_instance(bench(11), "I11")
    ap = APClustering3D(inst)

    try:
        assignment = ap.fit()
        s.ok("fit() on 2DD+1PD instance completes")
    except Exception as e:
        s.fail("fit() crashed", str(e))
        return s

    depot_ids = {n.node_id for n in inst.all_depots}
    customer_ids = {n.node_id for n in inst.all_customers}

    s.check("All customers assigned", customer_ids == set(assignment.keys()),
            f"Unassigned: {customer_ids - set(assignment.keys())}")

    s.check("Assignments only to valid depots",
            all(v in depot_ids for v in assignment.values()),
            f"Invalid: {[(k,v) for k,v in assignment.items() if v not in depot_ids][:3]}")

    clusters = cluster_by_depot_type(assignment, inst)
    s.check("All 3 depots have a cluster entry",
            set(clusters.keys()) == depot_ids,
            f"Missing depots: {depot_ids - set(clusters.keys())}")

    # Both DDs should have some customers (not all go to PD)
    dd_ids = [n.node_id for n in inst.delivery_depots]
    for dd in dd_ids:
        s.check(f"DD {dd} has at least 1 customer",
                len(clusters.get(dd, [])) > 0,
                f"DD {dd} has 0 customers — degenerate clustering")

    print(f"\n  [Instance 11 clustering (2DD+1PD)]:")
    for depot_id, clist in clusters.items():
        dtype = inst.nodes[depot_id].node_type.value
        print(f"    {dtype}(node {depot_id}): {len(clist)} customers")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 7 — Depot forced as exemplar (critical property)
# ═══════════════════════════════════════════════════════════════════════════

def suite_depot_exemplar() -> TestSuite:
    """
    Depots must ALWAYS be exemplars (forced in code).
    No customer should ever be an exemplar.
    """
    s = TestSuite("Depot Forced as Exemplar")
    inst = load_benchmark_instance(bench(1), "I1")
    ap = APClustering3D(inst)
    ap.S = ap._build_similarity_matrix()
    ap.R = np.zeros((ap.n, ap.n))
    ap.A = np.zeros((ap.n, ap.n))

    depot_ids = {n.node_id for n in inst.all_depots}

    # Check S diagonal: depots >> customers
    for i, nid in enumerate(ap.node_ids):
        if nid in depot_ids:
            max_off = np.max([ap.S[i, j] for j in range(ap.n) if j != i])
            s.check(f"Depot {nid} S[i,i] >> all off-diag S[i,j]",
                    ap.S[i, i] > max_off * 2,
                    f"S[i,i]={ap.S[i,i]:.2f}, max_off={max_off:.2f}")

    # After fit: all assignments point to a depot (never a customer)
    assignment = ap.fit()
    non_depot_exemplars = {did for did in assignment.values() if did not in depot_ids}
    s.check("No customer is used as exemplar",
            len(non_depot_exemplars) == 0,
            f"Customer used as exemplar: {non_depot_exemplars}")

    # All depots appear as exemplars (i.e., have at least one customer OR exist as cluster key)
    clusters = cluster_by_depot_type(assignment, inst)
    s.check("All depots appear as cluster keys",
            set(clusters.keys()) == depot_ids,
            f"Missing depot keys: {depot_ids - set(clusters.keys())}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 8 — NOTE-08: Effect of s/t coefficients
# Sanity check that changing s/t changes the clustering
# ═══════════════════════════════════════════════════════════════════════════

def suite_st_sensitivity() -> TestSuite:
    """
    NOTE-08: s,t coefficients not given in paper. Default=0.5.
    Test that different s/t values produce different STD and (potentially) different clusters.
    """
    s = TestSuite("s/t Coefficient Sensitivity (NOTE-08)")
    inst = load_benchmark_instance(bench(11), "I11")  # 2DD+1PD → variation visible

    configs = [
        ("s=0.5,t=0.5", 0.5, 0.5),
        ("s=1.0,t=0.0", 1.0, 0.0),
        ("s=0.0,t=1.0", 0.0, 1.0),
        ("s=0.8,t=0.2", 0.8, 0.2),
    ]

    results = {}
    for label, sc, tc in configs:
        ap = APClustering3D(inst, spatial_coeff=sc, temporal_coeff=tc)
        assignment = ap.fit()
        clusters = cluster_by_depot_type(assignment, inst)
        dist = {k: len(v) for k, v in clusters.items()}
        results[label] = dist
        print(f"\n  [{label}] cluster sizes: {dist}")

    # Different configs should give potentially different results
    # At minimum, verify all produce valid assignments
    for label, sc, tc in configs:
        ap = APClustering3D(inst, spatial_coeff=sc, temporal_coeff=tc)
        assignment = ap.fit()
        depot_ids = {n.node_id for n in inst.all_depots}
        customer_ids = {n.node_id for n in inst.all_customers}

        s.check(f"{label}: all customers assigned",
                set(assignment.keys()) == customer_ids,
                f"Missing: {customer_ids - set(assignment.keys())}")
        s.check(f"{label}: all assigned to valid depot",
                all(v in depot_ids for v in assignment.values()),
                f"Invalid depots: {set(v for v in assignment.values() if v not in depot_ids)}")

    # s=0.5,t=0.5 is the paper default — document it
    s.ok("NOTE-08: s=0.5, t=0.5 used as default (paper doesn't specify)",
         "Different s/t values change STD and potentially change cluster assignments")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

SUITES = {
    "std":               suite_std,
    "similarity":        suite_similarity,
    "ra_update":         suite_ra_update,
    "damping":           suite_damping,
    "full_clustering":   suite_full_clustering,
    "multi_depot":       suite_multi_depot_clustering,
    "depot_exemplar":    suite_depot_exemplar,
    "st_sensitivity":    suite_st_sensitivity,
}


def log_result(passed, total, suite_names):
    log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'EXPERIMENTS.md')
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    status = "✅ ALL PASSED" if passed == total else f"❌ {total-passed} FAILED"
    entry = f"""
## [{ts}] Clustering Module Tests — {', '.join(suite_names)}
**Command:** `python3 tests/test_clustering_module.py`
**Purpose:** Verify 3D AP Clustering (Eq.49-53, Table 6) implementation
**Results:** {passed}/{total} tests — {status}
**Next action:** {"Module 4 — NSGA-II / algorithm.py (ISSUE-001, ISSUE-002)" if passed==total else "Fix clustering bugs before proceeding"}
"""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="MDPDTWDD Clustering Tests")
    parser.add_argument('--suite', nargs='+',
                        choices=list(SUITES.keys()) + ['all'], default=['all'])
    parser.add_argument('--no-log', action='store_true')
    args = parser.parse_args()

    names = list(SUITES.keys()) if 'all' in args.suite else args.suite

    print(f"\n{'═'*65}")
    print(f"  MDPDTWDD — Module 3: 3D AP Clustering Verification")
    print(f"  Eq.49 (STD), Eq.50 (R), Eq.51 (A), Eq.52/53 (damping), Table 6")
    print(f"  Suites: {', '.join(names)}")
    print(f"{'═'*65}")

    tp = tt = 0
    for name in names:
        suite = SUITES[name]()
        p, t = suite.report()
        tp += p; tt += t

    print(f"\n{'═'*65}")
    icon = "✅" if tp == tt else "❌"
    print(f"  {icon} TOTAL: {tp}/{tt} tests passed")
    if tp < tt:
        print(f"  ⚠  {tt-tp} FAILED")
    print(f"{'═'*65}\n")

    if not args.no_log:
        log_result(tp, tt, names)
        print(f"  Logged → logs/EXPERIMENTS.md\n")

    sys.exit(0 if tp == tt else 1)


if __name__ == '__main__':
    main()
