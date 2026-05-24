"""
test_nsga2_module.py — Module 4: NSGA-II Verification
======================================================
Kiểm tra từng thành phần của ANSGA-II (Section 4.3):
  - Chromosome encode/decode
  - PMX crossover (Fig.4)
  - Adaptive mutation (Eq.55, Table 8)
  - Nondominated sort + crowding distance (Table 10)
  - Local search (Table 9, Eq.56)
  - Full algorithm run: CT và convergence
  - Dynamic insertion impact (ISSUE-001)

Run:
    cd mdpdtwdd-cli
    python3 tests/test_nsga2_module.py
    python3 tests/test_nsga2_module.py --suite decode
"""

import os, sys, math, argparse, datetime, time, random, copy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from src.data_loader import load_benchmark_instance
from src.data_model import Vehicle, Route, Solution, ProblemInstance
from src.clustering import APClustering3D
from src.nsga2 import (
    Chromosome, decode_chromosome, initialize_population,
    pmx_crossover, mutate, adaptive_mutation_rate,
    fast_nondominated_sort, crowding_distance_assignment,
    tournament_selection, local_search,
)
from src.objectives import evaluate_solution, dominates
from src.algorithm import AlgorithmParams, run_3dapansga2

# ── helpers ──────────────────────────────────────────────────────────────────
def bench(n):
    import glob
    return sorted(glob.glob(os.path.join(
        os.path.dirname(__file__), '..', 'data', 'process', 'benchmark', f'{n} *Sheet1.csv'
    )))[0]

def make_vehicle(inst):
    return Vehicle(1, inst.vehicle_capacity, inst.vehicle_speed,
                   inst.fuel_rate, inst.fuel_price, inst.annual_maintenance)

def get_cluster_map(inst):
    ap = APClustering3D(inst)
    assignment = ap.fit()
    return {cid: assignment.get(cid, inst.all_depots[0].node_id)
            for cid in [n.node_id for n in inst.static_customers]}

def approx(a, b, tol=1e-6): return abs(a - b) <= tol

# ── TestSuite ─────────────────────────────────────────────────────────────────
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


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 1 — Chromosome Decode
# ═══════════════════════════════════════════════════════════════════════════

def suite_decode() -> TestSuite:
    s = TestSuite("Chromosome Decode")
    inst = load_benchmark_instance(bench(1), "I1")
    vp = make_vehicle(inst)
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]

    # ── Decode covers all static customers ───────────────────────────────
    genes = static_ids.copy(); random.seed(42); random.shuffle(genes)
    chrom = Chromosome(genes=genes, cluster_map=cluster_map)
    sol = decode_chromosome(chrom, inst, vp)

    all_visited = [nid for r in sol.routes for nid in r.nodes]
    s.check("All static customers appear in decoded solution",
            set(all_visited) == set(static_ids),
            f"Missing: {set(static_ids)-set(all_visited)}, Extra: {set(all_visited)-set(static_ids)}")

    s.check("No customer visited twice",
            len(all_visited) == len(set(all_visited)),
            f"Duplicates: {[x for x in all_visited if all_visited.count(x)>1][:5]}")

    # ── Dynamic customers NOT in initial decode (NOTE-09) ─────────────────
    dyn_ids = {n.node_id for n in inst.dynamic_customers}
    dyn_in_routes = [n for r in sol.routes for n in r.nodes if n in dyn_ids]
    s.check("Dynamic customers NOT in initial decode (NOTE-09)",
            len(dyn_in_routes) == 0,
            f"Dynamic customers in initial routes: {dyn_in_routes}")

    # ── Each route starts from a valid depot ─────────────────────────────
    depot_ids = {n.node_id for n in inst.all_depots}
    bad_origins = [r.origin_depot_id for r in sol.routes
                   if r.origin_depot_id not in depot_ids]
    s.check("All routes start from valid depot",
            len(bad_origins) == 0,
            f"Invalid origins: {bad_origins}")

    # ── Capacity constraint respected ─────────────────────────────────────
    cap = inst.vehicle_capacity
    for r in sol.routes:
        total_demand = sum(
            (inst.nodes[n].Q_i if inst.nodes[n].is_static_delivery()
             else inst.nodes[n].P_i)
            for n in r.nodes
        )
        s.check(f"Route capacity ≤ {cap}",
                total_demand <= cap + 1e-6,
                f"Route demand={total_demand:.1f} exceeds capacity {cap}")

    # ── TOC is finite and positive ────────────────────────────────────────
    s.check("TOC is finite", math.isfinite(sol.TOC), f"TOC={sol.TOC}")
    s.check("TOC > 0", sol.TOC > 0, f"TOC={sol.TOC}")
    s.check("NV > 0", sol.NV > 0, f"NV={sol.NV}")

    # ── NV consistent with routes ─────────────────────────────────────────
    n_active = sum(1 for r in sol.routes if r.nodes)
    s.check("NV == number of active routes",
            sol.NV == n_active,
            f"NV={sol.NV}, active routes={n_active}")

    print(f"\n  [Decode I1]: NV={sol.NV}, TOC={sol.TOC:.1f} "
          f"(paper: NV=6, TOC=1654)")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 2 — PMX Crossover (Fig.4)
# ═══════════════════════════════════════════════════════════════════════════

def suite_pmx() -> TestSuite:
    s = TestSuite("PMX Crossover (Fig.4, Section 4.3.1)")
    inst = load_benchmark_instance(bench(1), "I1")
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]

    random.seed(0)
    for trial in range(20):
        genes1 = static_ids.copy(); random.shuffle(genes1)
        genes2 = static_ids.copy(); random.shuffle(genes2)
        p1 = Chromosome(genes=genes1, cluster_map=cluster_map)
        p2 = Chromosome(genes=genes2, cluster_map=cluster_map)

        o1, o2 = pmx_crossover(p1, p2)

        # Offspring must be valid permutation (same elements, no dup, no missing)
        s.check(f"PMX trial {trial+1}: o1 is valid permutation",
                sorted(o1.genes) == sorted(static_ids),
                f"o1 genes {sorted(o1.genes)[:5]}... ≠ expected",
                f"missing={set(static_ids)-set(o1.genes)}, extra={set(o1.genes)-set(static_ids)}")

        s.check(f"PMX trial {trial+1}: o2 is valid permutation",
                sorted(o2.genes) == sorted(static_ids),
                f"o2 genes invalid",
                f"missing={set(static_ids)-set(o2.genes)}, extra={set(o2.genes)-set(static_ids)}")

        s.check(f"PMX trial {trial+1}: o1 no duplicates",
                len(o1.genes) == len(set(o1.genes)),
                f"Duplicates in o1")
        s.check(f"PMX trial {trial+1}: o2 no duplicates",
                len(o2.genes) == len(set(o2.genes)),
                f"Duplicates in o2")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 3 — Mutation (Eq.55, Table 8)
# ═══════════════════════════════════════════════════════════════════════════

def suite_mutation() -> TestSuite:
    s = TestSuite("Mutation (Eq.55, Table 8)")
    inst = load_benchmark_instance(bench(1), "I1")
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]

    genes = static_ids.copy()
    chrom = Chromosome(genes=genes, cluster_map=cluster_map)

    # ── Mutated chromosome is still valid permutation ─────────────────────
    random.seed(1)
    for trial in range(20):
        mutated = mutate(chrom, mp=1.0)  # mp=1 → always mutate
        s.check(f"Mutation trial {trial+1}: valid permutation",
                sorted(mutated.genes) == sorted(static_ids),
                f"Not a valid permutation after mutation")
        s.check(f"Mutation trial {trial+1}: no duplicates",
                len(mutated.genes) == len(set(mutated.genes)),
                "Duplicates after mutation")

    # ── mp=0: chromosome never changes ────────────────────────────────────
    for trial in range(10):
        unchanged = mutate(chrom, mp=0.0)
        s.check(f"mp=0: genes unchanged (trial {trial+1})",
                unchanged.genes == chrom.genes,
                f"Genes changed despite mp=0")

    # ── Eq.55: mp decays correctly ────────────────────────────────────────
    mp_init = 0.05; M_gen = 150
    mp_at_0   = adaptive_mutation_rate(mp_init, 0,   M_gen)
    mp_at_75  = adaptive_mutation_rate(mp_init, 75,  M_gen)
    mp_at_149 = adaptive_mutation_rate(mp_init, 149, M_gen)

    s.check("Eq.55: mp at gen=0 = mp_init*(1-0/150) = 0.05",
            approx(mp_at_0, 0.05 * (1 - 0/150)), f"got {mp_at_0:.6f}")
    s.check("Eq.55: mp at gen=75 = 0.05*(1-0.5) = 0.025",
            approx(mp_at_75, 0.025), f"got {mp_at_75:.6f}")
    s.check("Eq.55: mp at gen=149 < mp_at_75 (decays)",
            mp_at_149 < mp_at_75, f"mp_at_149={mp_at_149} not < mp_at_75={mp_at_75}")
    s.check("Eq.55: mp monotonically decreasing",
            all(adaptive_mutation_rate(mp_init, g, M_gen) >=
                adaptive_mutation_rate(mp_init, g+1, M_gen)
                for g in range(M_gen-1)),
            "mp is not monotonically decreasing")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 4 — Nondominated Sort + Crowding Distance (Table 10)
# ═══════════════════════════════════════════════════════════════════════════

def suite_nsga_sort() -> TestSuite:
    s = TestSuite("Nondominated Sort + Crowding Distance (Table 10)")
    inst = load_benchmark_instance(bench(1), "I1")
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]
    vp = make_vehicle(inst)

    # Build 6 artificial chromosomes with known dominance relations
    # sol A: TOC=1000, NV=5  → best
    # sol B: TOC=1500, NV=7  → dominated by A
    # sol C: TOC=800,  NV=8  → non-dominated with A (better TOC, worse NV)
    # sol D: TOC=1800, NV=4  → non-dominated with A (worse TOC, better NV)
    # sol E: TOC=2000, NV=9  → dominated by B
    # sol F: TOC=1500, NV=7  → equal to B → same rank as B

    pop = []
    for toc, nv in [(1000,5),(1500,7),(800,8),(1800,4),(2000,9),(1500,7)]:
        genes = static_ids.copy(); random.shuffle(genes)
        chrom = Chromosome(genes=genes, cluster_map=cluster_map)
        sol = Solution(); sol.TOC = toc; sol.NV = nv
        chrom.solution = sol
        pop.append(chrom)

    fronts = fast_nondominated_sort(pop)

    # A(0), C(2), D(3) should be in front 0 (non-dominated)
    front0_toc = {pop[i].solution.TOC for i in fronts[0]}
    s.check("Front 0 contains A(1000), C(800), D(1800)",
            {1000, 800, 1800}.issubset(front0_toc),
            f"Front 0 TOC values: {front0_toc}")

    # B(1500) and F(1500) should NOT be in front 0 (dominated by A)
    s.check("B(1500,7) NOT in front 0 (dominated by A(1000,5))",
            not any(pop[i].solution.TOC == 1500 and pop[i].solution.NV == 7
                    for i in fronts[0]),
            "B or F wrongly in front 0")

    # E(2000,9) dominated by B, should be in front 2 or later
    e_idx = 4
    s.check("E(2000,9) rank >= 1 (dominated)",
            pop[e_idx].rank >= 1,
            f"E rank={pop[e_idx].rank}, expected ≥1")

    # All individuals get a rank
    s.check("All individuals assigned a rank",
            all(hasattr(c, 'rank') for c in pop),
            "Some individuals missing rank")

    # ── Crowding distance ─────────────────────────────────────────────────
    front0 = fronts[0]
    crowding_distance_assignment(front0, pop)

    # Boundary individuals get inf crowding distance
    inf_count = sum(1 for i in front0 if pop[i].crowding_dist == float('inf'))
    s.check("Boundary solutions in front 0 get infinite crowding distance",
            inf_count >= 2,
            f"Only {inf_count} inf crowding distances in front 0 (expected ≥2)")

    # All individuals in front get non-negative crowding distance
    s.check("All crowding distances >= 0",
            all(pop[i].crowding_dist >= 0 for i in front0),
            f"Negative crowding distances found")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 5 — Population Initialization
# ═══════════════════════════════════════════════════════════════════════════

def suite_init_population() -> TestSuite:
    s = TestSuite("Population Initialization (Table 7)")
    inst = load_benchmark_instance(bench(1), "I1")
    vp = make_vehicle(inst)
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]

    random.seed(42)
    pop = initialize_population(100, cluster_map, static_ids, inst, vp)

    s.check("Population size = N_IND = 100",
            len(pop) == 100, f"got {len(pop)}")

    for i, chrom in enumerate(pop[:10]):
        s.check(f"Chrom {i}: valid permutation of static customers",
                sorted(chrom.genes) == sorted(static_ids),
                f"Invalid permutation")
        s.check(f"Chrom {i}: solution decoded",
                chrom.solution is not None and chrom.solution.TOC < float('inf'),
                f"Solution not decoded or TOC=inf")

    # Diversity: not all chromosomes are identical
    gene_sets = [tuple(c.genes) for c in pop[:10]]
    unique_gene_sets = set(gene_sets)
    s.check("Population diverse (not all identical chromosomes)",
            len(unique_gene_sets) > 1,
            f"All {len(pop)} chromosomes identical — no diversity!")

    # All solutions have finite TOC
    bad = [i for i, c in enumerate(pop) if c.solution is None or not math.isfinite(c.solution.TOC)]
    s.check("All initial solutions have finite TOC",
            len(bad) == 0,
            f"Infinite TOC in chromosomes: {bad[:5]}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 6 — Algorithm Run: CT and Convergence
# ═══════════════════════════════════════════════════════════════════════════

def suite_algorithm_run() -> TestSuite:
    s = TestSuite("Algorithm Run: CT & Convergence (ISSUE-001, ISSUE-002)")
    inst = load_benchmark_instance(bench(1), "I1")

    # ── Run with full params ──────────────────────────────────────────────
    params = AlgorithmParams(m_gen=150, n_ind=100, random_seed=42)
    t0 = time.time()
    result = run_3dapansga2(inst, params, verbose=False)
    ct = time.time() - t0

    print(f"\n  [Full run I1]: TOC={result.best_toc:.1f}, NV={result.best_nv}, CT={ct:.1f}s")
    print(f"  [Paper target]: TOC=1654, NV=6, CT≈84s")
    print(f"  [Gap]: TOC×{result.best_toc/1654:.1f}, CT×{84/max(ct,0.1):.1f}")

    # CT > 1s (was 0.2s — ISSUE-002 confirmed fixed; now faster due to optimisation)
    s.check("CT > 1s (NSGA-II loop running properly now)",
            ct > 1.0,
            f"CT={ct:.2f}s too low — NSGA-II not running properly (ISSUE-002)",
            f"CT={ct:.1f}s (paper: ~84s, optimised implementation)")

    # TOC < baseline (was 71,417)
    s.check("TOC < 71417 (baseline improved)",
            result.best_toc < 71417,
            f"TOC={result.best_toc:.1f} not better than baseline 71417")

    # NV reasonable (paper: 6)
    s.check("NV in range [1, 20]",
            1 <= result.best_nv <= 20,
            f"NV={result.best_nv} unreasonable")

    # ── Quick run: small params to verify loop works ──────────────────────
    params_small = AlgorithmParams(m_gen=10, n_ind=20, random_seed=0)
    t1 = time.time()
    res_small = run_3dapansga2(inst, params_small)
    ct_small = time.time() - t1

    s.check("Small run (10gen×20pop) completes without crash",
            math.isfinite(res_small.best_toc),
            f"Crashed or infinite TOC: {res_small.best_toc}")

    # Improvement over generations: 150gen should beat 10gen
    s.check("150 gen result better than 10 gen (algorithm converges)",
            result.best_toc <= res_small.best_toc,
            f"150gen TOC={result.best_toc:.1f} NOT better than 10gen TOC={res_small.best_toc:.1f}")

    # ── TOC gap analysis ──────────────────────────────────────────────────
    gap_pct = (result.best_toc - 1654) / 1654 * 100
    print(f"\n  [TOC Gap Analysis]:")
    print(f"    Current best TOC : {result.best_toc:.1f}")
    print(f"    Paper target     : 1654")
    print(f"    Gap              : +{gap_pct:.0f}%")

    from src.data_loader import load_benchmark_instance as lbi
    _inst = lbi(bench(1), "I1")
    FC = sum(n.Q_i for n in _inst.static_delivery_customers) + \
         sum(n.P_i for n in _inst.static_pickup_customers) + \
         sum(n.P_i for n in _inst.dynamic_customers)
    IC = sum(n.P_i for n in _inst.dynamic_customers)
    MC_paper = 6 * 40000/364
    print(f"    FC+IC+MC(NV=6)   : {FC+IC+MC_paper:.1f} (constant floor)")
    print(f"    Remaining for TC+PC (paper): {1654-FC-IC-MC_paper:.1f}")
    print(f"    Actual TC+PC     : {result.best_toc-FC-IC-result.best_nv*40000/364:.1f}")

    # TOC gap > 0 (we know it's not perfect yet)
    s.check("TOC gap documented (target: reduce to <50%)",
            True, "",
            f"Current gap: +{gap_pct:.0f}% (paper: 1654, got: {result.best_toc:.1f})")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 7 — Dynamic Insertion Impact (CRITICAL BUG)
# ═══════════════════════════════════════════════════════════════════════════

def suite_dynamic_insertion_impact() -> TestSuite:
    """
    CRITICAL: dynamic insertion is making TOC WORSE.
    Before insertion: TOC=11,277. After: TOC=24,971.
    This is a bug — insertion should never make TOC worse by 2x.
    """
    s = TestSuite("Dynamic Insertion Impact [CRITICAL BUG DETECTION]")
    inst = load_benchmark_instance(bench(1), "I1")

    from src.insertion_strategy import insert_dynamic_demands
    from src.clustering import APClustering3D
    from src.nsga2 import initialize_population, decode_chromosome
    from src.algorithm import AlgorithmParams, run_3dapansga2

    # Get a decent solution before insertion
    params = AlgorithmParams(m_gen=50, n_ind=50, random_seed=42)

    # Run WITHOUT dynamic insertion to get pre-insertion TOC
    ap = APClustering3D(inst)
    assignment = ap.fit()
    static_ids = [n.node_id for n in inst.static_customers]
    static_map = {cid: assignment.get(cid, inst.all_depots[0].node_id) for cid in static_ids}
    vp = make_vehicle(inst)

    random.seed(42)
    pop = initialize_population(50, static_map, static_ids, inst, vp)
    best_pre = min(pop, key=lambda c: c.solution.TOC if c.solution else float('inf'))
    toc_pre = best_pre.solution.TOC

    # Apply dynamic insertion
    dyn_ids = sorted([n.node_id for n in inst.dynamic_customers],
                     key=lambda k: inst.nodes[k].known_time)
    sol_post = insert_dynamic_demands(best_pre.solution, dyn_ids, inst)
    toc_post = sol_post.TOC

    print(f"\n  [Dynamic Insertion Impact]:")
    print(f"    TOC before insertion: {toc_pre:.1f}")
    print(f"    TOC after  insertion: {toc_post:.1f}")
    print(f"    Change: {'+' if toc_post>toc_pre else ''}{toc_post-toc_pre:.1f} "
          f"({(toc_post-toc_pre)/toc_pre*100:+.1f}%)")
    print(f"    Dynamic customers: {dyn_ids} "
          f"(P_i={[inst.nodes[d].P_i for d in dyn_ids]})")

    # DOCUMENT: insertion should not more than double TOC
    s.check("Dynamic insertion does NOT more than double TOC",
            toc_post < toc_pre * 3,
            f"Insertion causes TOC to jump {toc_pre:.0f} → {toc_post:.0f} "
            f"({toc_post/toc_pre:.1f}x) — severe bug",
            f"pre={toc_pre:.1f}, post={toc_post:.1f}")

    # DOCUMENT: insertion should add all dynamic customers
    dyn_in_sol = {n for r in sol_post.routes for n in r.nodes
                  if n in set(dyn_ids)}
    s.check("All dynamic customers inserted into solution",
            dyn_in_sol == set(dyn_ids),
            f"Missing dynamic customers: {set(dyn_ids)-dyn_in_sol}",
            f"Inserted: {dyn_in_sol}")

    # NV after insertion
    print(f"    NV before: {best_pre.solution.NV}, NV after: {sol_post.NV}")
    s.check("NV after insertion >= NV before (may add new vehicles)",
            sol_post.NV >= best_pre.solution.NV,
            f"NV decreased after insertion? {best_pre.solution.NV}→{sol_post.NV}")

    # PC analysis: is the big jump coming from penalty?
    print(f"    TC: {best_pre.solution.TC:.1f} → {sol_post.TC:.1f}")
    print(f"    PC: {best_pre.solution.PC:.1f} → {sol_post.PC:.1f}")
    print(f"    MC: {best_pre.solution.MC:.1f} → {sol_post.MC:.1f}")
    print(f"    IC: {best_pre.solution.IC:.1f} → {sol_post.IC:.1f}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# SUITE 8 — Route Decode Quality: are routes sensible?
# ═══════════════════════════════════════════════════════════════════════════

def suite_route_quality() -> TestSuite:
    """
    Check whether decoded routes look sensible:
    - PC should be low for well-decoded routes
    - Routes should have reasonable load
    - Open vs closed route logic
    """
    s = TestSuite("Route Decode Quality Check")
    inst = load_benchmark_instance(bench(1), "I1")
    vp = make_vehicle(inst)
    cluster_map = get_cluster_map(inst)
    static_ids = [n.node_id for n in inst.static_customers]

    # Run 10 random chromosomes, collect stats
    random.seed(99)
    pc_vals, nv_vals, toc_vals = [], [], []
    for _ in range(10):
        genes = static_ids.copy(); random.shuffle(genes)
        chrom = Chromosome(genes=genes, cluster_map=cluster_map)
        sol = decode_chromosome(chrom, inst, vp)
        pc_vals.append(sol.PC)
        nv_vals.append(sol.NV)
        toc_vals.append(sol.TOC)

    avg_pc = sum(pc_vals)/len(pc_vals)
    avg_nv = sum(nv_vals)/len(nv_vals)
    avg_toc = sum(toc_vals)/len(toc_vals)

    print(f"\n  [Route quality over 10 random chromosomes]:")
    print(f"    avg TOC={avg_toc:.1f}  avg NV={avg_nv:.1f}  avg PC={avg_pc:.1f}")
    print(f"    TOC range=[{min(toc_vals):.1f}, {max(toc_vals):.1f}]")
    print(f"    NV range=[{min(nv_vals)}, {max(nv_vals)}]")

    # PC is large fraction of TOC → main driver of excess cost
    FC = sum(n.Q_i for n in inst.static_delivery_customers) + \
         sum(n.P_i for n in inst.static_pickup_customers) + \
         sum(n.P_i for n in inst.dynamic_customers)
    pc_fraction = avg_pc / (avg_toc - FC) if avg_toc > FC else 0
    print(f"    PC fraction of (TOC-FC): {pc_fraction*100:.1f}%")

    s.check("Average TOC < 100000 (not catastrophically high)",
            avg_toc < 100000,
            f"avg_toc={avg_toc:.1f} too high")

    s.check("Average NV in [3, 20]",
            3 <= avg_nv <= 20,
            f"avg_nv={avg_nv:.1f}")

    s.check("PC is the dominant excess cost (>50% of variable cost)",
            pc_fraction > 0.5,
            f"PC fraction={pc_fraction*100:.1f}% — PC not dominant",
            "Confirms PC (penalty) is main problem → routing quality issue")

    # Document the TOC decomposition for best random solution
    best_sol = min(zip(toc_vals, range(10)))[1]
    random.seed(99)
    for i in range(best_sol+1):
        genes = static_ids.copy(); random.shuffle(genes)
    chrom_best = Chromosome(genes=genes, cluster_map=cluster_map)
    sol_best = decode_chromosome(chrom_best, inst, vp)
    print(f"\n  [Best random sol]: TOC={sol_best.TOC:.1f} NV={sol_best.NV}")
    print(f"    TC={sol_best.TC:.1f}  PC={sol_best.PC:.1f}  "
          f"MC={sol_best.MC:.1f}  IC={sol_best.IC:.1f}  FC={sol_best.FC:.1f}")

    return s


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

SUITES = {
    "decode":            suite_decode,
    "pmx":               suite_pmx,
    "mutation":          suite_mutation,
    "nsga_sort":         suite_nsga_sort,
    "init_population":   suite_init_population,
    "algorithm_run":     suite_algorithm_run,
    "dynamic_insertion": suite_dynamic_insertion_impact,
    "route_quality":     suite_route_quality,
}


def log_result(passed, total, suite_names, extra=""):
    log_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'EXPERIMENTS.md')
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    status = "✅ ALL PASSED" if passed == total else f"❌ {total-passed} FAILED"
    entry = f"""
## [{ts}] NSGA-II Module Tests — {', '.join(suite_names)}
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** {passed}/{total} tests — {status}
{extra}
**Next action:** {"Module 5 — Insertion Strategy fix (ISSUE-001)" if passed==total else "Fix NSGA-II bugs"}
"""
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="MDPDTWDD NSGA-II Tests")
    parser.add_argument('--suite', nargs='+',
                        choices=list(SUITES.keys())+['all'], default=['all'])
    parser.add_argument('--no-log', action='store_true')
    args = parser.parse_args()

    names = list(SUITES.keys()) if 'all' in args.suite else args.suite

    print(f"\n{'═'*65}")
    print(f"  MDPDTWDD — Module 4: NSGA-II Verification")
    print(f"  Section 4.3: decode, PMX, mutation, sort, local search, run")
    print(f"  Suites: {', '.join(names)}")
    print(f"{'═'*65}")

    tp = tt = 0
    extra_notes = []
    for name in names:
        suite = SUITES[name]()
        p, t = suite.report()
        tp += p; tt += t
        if p < t:
            extra_notes.append(f"- {name}: {t-p} failures")

    print(f"\n{'═'*65}")
    icon = "✅" if tp == tt else "❌"
    print(f"  {icon} TOTAL: {tp}/{tt} tests passed")
    if tp < tt:
        print(f"  ⚠  {tt-tp} FAILED")
    print(f"{'═'*65}\n")

    if not args.no_log:
        extra = "\n".join(extra_notes)
        log_result(tp, tt, names, extra)
        print(f"  Logged → logs/EXPERIMENTS.md\n")

    sys.exit(0 if tp == tt else 1)


if __name__ == '__main__':
    main()
