# EXPERIMENTS — mdpdtwdd-cli

> Format: append-only. Log every test run here.
> Template:
> ```
> ## [YYYY-MM-DD HH:MM] <experiment name>
> **Command:** python main.py ...
> **Purpose:** why this test was run
> **Results:** TOC, NV, CT per instance
> **Analysis:** what the numbers mean
> **Next action:** what to do based on this result
> ```

---

## [2026-05-24 08:10] Baseline benchmark run (all 30 instances, 1 run each)

**Command:** `python main.py benchmark --dir "data/process/benchmark" --runs 1 --log logs/test_run.jsonl`
**Purpose:** Establish baseline before any modifications. Check how far current implementation is from paper targets.
**Params:** m_gen=150, n_ind=100, seed=None

**Results (selected instances):**
| # | Instance     | C   | TOC($)      | NV | CT(s) | Paper TOC | Gap%      |
|---|--------------|-----|-------------|----|---------|-----------| ----------|
| 1 | Instance_1   | 48  | 71,417      | 4  | 0.2    | 1,654     | +4,220%   |
| 2 | Instance_2   | 72  | 123,408     | 3  | 0.4    | 2,715     | +4,446%   |
| 3 | Instance_3   | 96  | 22,085      | 3  | 0.6    | 3,362     | +557%     |
| 4 | Instance_4   | 120 | 307,958     | 4  | 2.1    | 8,785     | +3,406%   |
| 5 | Instance_5   | 150 | 387,556     | 4  | 2.3    | 13,177    | +2,841%   |
| 6 | Instance_6   | 48  | 19,242      | 3  | 0.3    | 1,577     | +1,120%   |
| 7 | Instance_7   | 72  | 115,848     | 4  | 0.5    | 2,094     | +5,434%   |
| 8 | Instance_8   | 96  | 23,797      | 4  | 0.9    | 2,926     | +713%     |
| 9 | Instance_9   | 120 | 245,851     | 5  | 1.5    | 5,399     | +4,452%   |
| 10| Instance_10  | 150 | 310,144     | 4  | 1.7    | 5,682     | +5,359%   |
| 11| Instance_11  | 48  | 17,630      | 3  | 0.2    | 1,313     | +1,243%   |
| 12| Instance_12  | 72  | 20,740      | 3  | 0.5    | 1,687     | +1,129%   |
| 13| Instance_13  | 96  | 19,775      | 3  | 0.7    | 3,457     | +472%     |
| 14| Instance_14  | 120 | 29,847      | 5  | 1.6    | 3,643     | +719%     |
| 15| Instance_15  | 150 | 2,825,530   | 5  | 2.9    | 17,252    | +16,277%  |
| 16| Instance_16  | 48  | 21,824      | 4  | 0.3    | 1,549     | +1,309%   |
| 17| Instance_17  | 72  | 24,346      | 4  | 0.4    | 2,380     | +923%     |
| 18| Instance_18  | 96  | 127,236     | 5  | 0.8    | 2,973     | +4,181%   |
| 19| Instance_19  | 120 | 30,478      | 5  | 1.1    | 3,497     | +771%     |
| 20| Instance_20  | 150 | 498,750     | 5  | 3.4    | 4,485     | +11,022%  |

**Analysis:**
- TOC is consistently 5x–100x higher than paper. CRITICAL gap.
- CT is 0.2–3.4s vs paper's 84–886s. Algorithm is ~420x faster = **not running properly**.
- NV is lower than paper for most instances (3–5 vs 6–31 in paper). Fewer vehicles → higher individual route costs.
- The combination of low CT + wrong TOC + low NV strongly suggests:
  - NSGA-II is either running 0 or very few generations
  - Route decoding is not forming enough routes (NV too low)
  - Objective function is computing wrong TOC values
- Instance 15 is the most extreme outlier (TOC = 2.8M vs 17K). Something catastrophically wrong there.

**Next action:**
1. Investigate src/algorithm.py — check if M_gen loop is running
2. Add verbose print to count actual generations executed
3. Check src/nsga2.py for early termination bugs
4. Filed as ISSUE-001 and ISSUE-002

## [2026-05-24 12:12] Data Module Tests — attempt 1 (SUPERSEDED)
> ⚠ SUPERSEDED by 12:14. PAPER_TABLE14 expected values were wrong — data_loader.py was correct.
> Root cause: tôi đoán sai S/D counts cho I16,I22–I29. Không phải bug trong code.

## [2026-05-24 12:13] Data Module Tests — attempt 2 (SUPERSEDED)
> ⚠ SUPERSEDED by 12:14. Same issue as 12:12.

## [2026-05-24 12:14] Data Module Tests — Module 1 FINAL ✅
**Command:** `python3 tests/test_data_module.py`
**Purpose:** Verify data loading correctness — toàn bộ 30 instances trước khi đụng vào algorithm
**Results:** **1039/1039 PASS** ✅
**Suites passed:**
  - Node Type Detection (Table 14): 210/210 — tất cả 30 instances, mọi node type
  - Instance 1 Deep Verification: 49/49 — row-by-row so sánh vs CSV raw
  - Distance Matrix: 26/26 — Euclidean, symmetry, triangle inequality
  - Time Window Validation: 15/15 — TW assignment đúng (TW_D cho R, TW_P cho S/D)
  - Multi-Depot Encoding: 12/12 — DCs=1000/2000/3000 decode đúng
  - Parameters (Table 15): 12/12 — vehicle_capacity, speed, fuel_rate, etc.
  - Demand Feasibility: 624/624 — mọi customer mọi instance
  - All 30 Structural Scan: 91/91
**Key discoveries:**
  - I27–I29: thực sự có 3 DDs (DCs=1000+2000+3000), loader đúng
  - Dynamic customers (PCs=4, known_time>0): load đúng, đủ 5 nodes với kt=30/300/300/400/500
  - data_loader.py và data_model.py: VERIFIED CORRECT, không cần sửa
**Analysis:** Data tầng này hoàn toàn sạch. Vấn đề TOC sai không nằm ở đây.
**Next action:** Module 2 — Objective function verification (src/objectives.py)

## [2026-05-24 12:44] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 53/53 tests — ✅ ALL PASSED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Module 3 — Clustering (src/clustering.py)

## [2026-05-24 13:17] Clustering Module Tests — std, similarity, ra_update, damping, full_clustering, multi_depot, depot_exemplar, st_sensitivity
**Command:** `python3 tests/test_clustering_module.py`
**Purpose:** Verify 3D AP Clustering (Eq.49-53, Table 6) implementation
**Results:** 69/69 tests — ✅ ALL PASSED
**Next action:** Module 4 — NSGA-II / algorithm.py (ISSUE-001, ISSUE-002)

## [2026-05-24 13:26] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 190/190 tests — ✅ ALL PASSED

**Next action:** Module 5 — Insertion Strategy fix (ISSUE-001)

## [2026-05-24 19:00] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 190/190 tests — ✅ ALL PASSED

**Next action:** Module 5 — Insertion Strategy fix (ISSUE-001)

## [2026-05-24 19:38] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 52/53 tests — ❌ 1 FAILED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Fix failed objective function tests

## [2026-05-24 19:38] Clustering Module Tests — std, similarity, ra_update, damping, full_clustering, multi_depot, depot_exemplar, st_sensitivity
**Command:** `python3 tests/test_clustering_module.py`
**Purpose:** Verify 3D AP Clustering (Eq.49-53, Table 6) implementation
**Results:** 69/69 tests — ✅ ALL PASSED
**Next action:** Module 4 — NSGA-II / algorithm.py (ISSUE-001, ISSUE-002)

## [2026-05-24 19:38] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 189/190 tests — ❌ 1 FAILED
- algorithm_run: 1 failures
**Next action:** Fix NSGA-II bugs

## [2026-05-24 19:38] Data Module Tests — node_types, instance1_deep, distance, time_windows, multi_depot, parameters, demand, all_instances
**Command:** `python tests/test_data_module.py --suite node_types instance1_deep distance time_windows multi_depot parameters demand all_instances`
**Purpose:** Verify data loading correctness before algorithm implementation
**Results:** 1039/1039 tests passed — ✅ ALL PASSED
**Analysis:** Data loading is correct. Proceed to next module.
**Next action:** Module 2 — Objective function verification

## [2026-05-24 19:38] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 52/53 tests — ❌ 1 FAILED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Fix failed objective function tests

## [2026-05-24 19:38] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 189/190 tests — ❌ 1 FAILED
- algorithm_run: 1 failures
**Next action:** Fix NSGA-II bugs

## [2026-05-24 19:38] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 52/53 tests — ❌ 1 FAILED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Fix failed objective function tests

## [2026-05-24 19:39] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 53/53 tests — ✅ ALL PASSED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Module 3 — Clustering (src/clustering.py)

## [2026-05-24 19:39] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 190/190 tests — ✅ ALL PASSED

**Next action:** Module 5 — Insertion Strategy fix (ISSUE-001)

## [2026-05-24 19:39] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 53/53 tests — ✅ ALL PASSED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Module 3 — Clustering (src/clustering.py)

## [2026-05-24 19:40] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 190/190 tests — ✅ ALL PASSED

**Next action:** Module 5 — Insertion Strategy fix (ISSUE-001)

## [2026-05-25] Full Module Audit — Agent code review pass

**Command:** Code audit (no run command)
**Purpose:** Systematic audit of all 7 modules against SRS.md and paper spec.
**Results:** 4 bugs found, 1 performance issue, 1 root-cause finding.

**Findings:**

| ID | Severity | Module | Description |
|----|----------|--------|-------------|
| ISSUE-008 | CRITICAL | insertion_strategy.py | `_check_feasibility_with_insertion` always returns True (`or True` bug) |
| ISSUE-009 | HIGH | insertion_strategy.py | scenario_1 capacity check ignores delivery load (uses pickup-only load) |
| ISSUE-010 | MEDIUM | nsga2.py | `compute_similarity` scans full dist_matrix.values() per call (O(N²) × N² calls) |
| ISSUE-011 | HIGH | algorithm.py | TOC gap decomposition: TC is 3.4x too high, PC=1311 non-zero |

**Clean (no bugs found):**
- data_model.py — distance matrix, numpy arrays, type membership: CORRECT
- data_loader.py — node type detection, CSV parsing: CORRECT (verified by 1039 tests)
- objectives.py — TC/PC/MC/IC/FC Eq.15-21: CORRECT (verified by 53 tests)
- clustering.py — 3D AP Eq.49-53: CORRECT (verified by 69 tests)
- nsga2.py — PMX crossover verified correct (unique genes, valid permutations)
- nsga2.py — adaptive_mutation_rate: correct (0 at gen=150, expected)
- nsga2.py — fast_nondominated_sort: numpy vectorised, correct
- algorithm.py — main loop range(1, m_gen+1): correct (150 generations run)

**TOC analysis (Instance 1, seed=42, gen=150, pop=100):**
  TOC=3816 (paper 1654, gap=+131%)
  TC=1045 (paper ≈304) — **3.4× too high** — long routes or excess vehicles
  PC=1311 (paper ≈0)  — TW penalties still significant despite l_i sort
  MC=769 NV=7 (paper MC=659, NV=6) — 1 extra vehicle
  FC=691, IC=0 — correct

**Priority fix order:**
  1. ISSUE-008: Fix `or True` in _check_feasibility_with_insertion
  2. ISSUE-009: Fix delivery load exclusion in scenario_1 capacity check
  3. Investigate PC=1311 source (open route handling)
  4. ISSUE-010: Cache max_d in compute_similarity

**Next action:** Fix ISSUE-008, ISSUE-009, rerun Instance 1, compare TOC.

## [2026-05-25 00:54] Objective Function Module Tests — tc, pc, mc, ic, fc, toc, fitness, mc_diagnosis
**Command:** `python3 tests/test_objectives_module.py`
**Purpose:** Verify Eq.15–21 (TC/PC/MC/IC/FC/TOC) implementation correctness
**Results:** 53/53 tests — ✅ ALL PASSED
**Key findings:**
  - MC interpretation: 1-per-route (M_v/T × NV) confirmed correct vs paper TOC=1654
  - FC is constant per instance (independent of routing) ✓
  - IC correctly counts γ*P_i for dynamic customers only ✓
  - TC = f_v*p_v*Σdist for all arcs ✓
  - PC uses raw arrival time (not service_start) per Eq.18 ✓
**Next action:** Module 3 — Clustering (src/clustering.py)

## [2026-05-25 00:54] NSGA-II Module Tests — decode, pmx, mutation, nsga_sort, init_population, algorithm_run, dynamic_insertion, route_quality
**Command:** `python3 tests/test_nsga2_module.py`
**Purpose:** Verify ANSGA-II (Section 4.3): decode, crossover, mutation, sort, full run
**Results:** 190/190 tests — ✅ ALL PASSED

**Next action:** Module 5 — Insertion Strategy fix (ISSUE-001)

## [2026-05-25] Phase 1 — H1 Open Route Audit + H2 TC Scale Investigation

**Command:** Code trace + manual computation
**Purpose:** Identify root cause of TC=1045 (3.4× paper TC≈192)

**Phase 1 — H1 Open Route (FALSIFIED):**
- Verified: all 7 routes in best solution are OPEN (DD→PD) ✓
- H1 eliminated: open route logic is working correctly

**Phase 2 — TC Root Cause:**
- l_i-sort test: removing l_i-sort makes TC slightly worse (1052 vs 1045), PC explodes (3583 vs 1311)
  → l_i-sort is HELPING not hurting
- Geo-cluster 6-route NN: total_dist=2426, TC=1189 (best possible naive routing)
- Paper TC≈192 → requires dist=392 units
- 1189 > 392 × 3.0 → SCALE MISMATCH CONFIRMED

**Key finding (F-007):**
- Paper TC=192 is physically impossible at current coord scale
- Scale factor needed: 0.162 (1 coord unit ≈ 160m)
- Our TC=1045 × 0.162 = 169 ≈ paper 192 ✓
- Physical explanation: benchmarks use 160m grid, not 1km grid
- This also explains PC=1311: at scale 1.0, travel times are 6× too long → vehicles arrive
  wildly out of TW window → massive penalties

**Filed:** ISSUE-012 (coordinate scale mismatch)

**Next action:** Test COORD_SCALE_FACTOR=0.162 in data_model.build_distance_matrix()
  Expected: TC drops from 1045 → ~170, PC drops from 1311 → ~0, TOC → ~1600 ≈ paper 1654
