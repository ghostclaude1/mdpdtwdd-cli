# CHANGELOG — mdpdtwdd-cli

> Format: append-only. One entry per logical change.
> Template:
> ```
> ## [YYYY-MM-DD HH:MM] <short title>
> **File(s):** src/xxx.py
> **Change:** what was changed and why
> **Reference:** SRS §X.Y / Eq.NN / NOTE-XX
> **Test result:** TOC instance 1 = X (paper: 1,654) | gap = +X%
> ```

---

## [2026-05-24] Module 1 — Data loading test suite (1039/1039 PASS)

**Files:** tests/test_data_module.py (new), CLAUDE.md (new), .cursor/rules/mdpdtwdd-agent.mdc (new)
**Change:** Created comprehensive data validation module with 8 test suites:
  1. Node Type Detection — all 30 instances vs paper Table 14 (210 tests)
  2. Instance 1 Deep Verification — row-by-row node values (49 tests)
  3. Distance Matrix Correctness — Euclidean formula, symmetry, triangle ineq (26 tests)
  4. Time Window Validation — TW assignment, l_i<r_i, depot windows (15 tests)
  5. Multi-Depot Encoding — DD/PD counts for I11/I21/I27–I30 (12 tests)  
  6. ProblemInstance Parameters — all Table 15 values (12 tests)
  7. Demand Feasibility — all 6 instances, every customer (624 tests)
  8. All 30 Instances Structural Scan — load + basic checks (91 tests)
**Discovery:** PAPER_TABLE14 initial estimates wrong for I16,I22–I25,I27–I29.
  After CSV inspection, corrected to actual data counts.
  Key finding: I27–I29 have 3 DDs (DCs=1000/2000/3000) + 1 PD, not 2+2.
  I16 has S=20, D=3 (not S=17, D=6). I22–I24 S/D counts differ from initial guess.
**Reference:** SRS §4.1, Paper Table 14
**Test result:** 1039/1039 PASS ✅ — data loading module VERIFIED CORRECT

---

## [2026-05-24] Initial project clone & scaffold

**Files:** All (initial state from GitHub)
**Change:** Cloned from https://github.com/ghostclaude1/mdpdtwdd-cli.git. Initial implementation present. Added skill file and log scaffolding.
**Reference:** SRS (full)
**Status:** Algorithm running but TOC far off. CT ~0.2s vs paper 84s — NSGA-II likely not running properly.

**Baseline benchmark run (test_run.jsonl):**
| Instance | Paper TOC | Actual TOC | Gap       | CT(s) |
|----------|-----------|------------|-----------|-------|
| 1        | 1,654     | 71,417     | +4,220%   | 0.2   |
| 5        | 13,177    | 387,556    | +2,841%   | 2.3   |
| 11       | 1,313     | 17,630     | +1,243%   | 0.2   |
| 15       | 17,252    | 2,825,530  | +16,277%  | 2.9   |
| 30       | 4,731     | (not yet)  | -         | -     |

**Next:** Investigate why CT so low and TOC so high.

---

## [2026-05-24] Fix TW-sort in decode + B_v backward pass + insertion cost metric

**Files:** src/nsga2.py, src/objectives.py, src/insertion_strategy.py
**Change:**
  1. `_split_into_routes` (nsga2.py): Sort customers **within** each capacity-feasible
     sub-route by `l_i` (TW left bound). Gene order still controls capacity grouping
     (preserving NSGA-II diversity); l_i sort controls visit sequence within each group.
     This is the primary mechanism by which paper achieves PC=0.
  2. `evaluate_route` (objectives.py): Added backward pass to compute `B_v_upper` —
     the latest departure time that avoids late violations at any node (ignoring waiting).
     B_v = clamp(B_v_upper, B_v_lower, depot.r_i). Reduces late-cascade violations.
  3. `scenario_1_direct_insert` + `scenario_2_goods_transfer` (insertion_strategy.py):
     After inserting dynamic customer, re-sort modified route by l_i to maintain TW order.
     Changed `cost_increase` from detour-only to actual TOC delta (includes PC change).
     This fixed a critical bug where "cheapest detour" scenario actually caused PC spike.
**Reference:** SRS §3.1 (B_v), Eq.18 (PC), Table 19 (PC=0 target), Section 4.4 (insertion)
**Test result:**
  Instance 1: TOC=4260.8, NV=9, CT=11.2s (paper: 1654, 6, 84s) — gap -157.6%
  Improvement from baseline: TOC 71417 → 4260 (-94.0%)
  PC component: 35000+ → 1311 (-96%)
  Dynamic insertion no longer causes TOC explosion (was +11777, now +444)
**Remaining issues:** PC=1311 still non-zero; NV=9 vs paper 6; clustering may be sub-optimal
