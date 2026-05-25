# ISSUES — mdpdtwdd-cli

> Format: append-only. Update status in-place for existing issues.
> Status: OPEN | IN_PROGRESS | CLOSED | WONTFIX

---

## [ISSUE-001] TOC values 10x–100x higher than paper targets
**Status:** OPEN
**Priority:** CRITICAL
**Opened:** 2026-05-24
**Description:**
All 30 instances produce TOC values massively higher than Table 16 of the paper.
Instance 1: paper=1,654, actual=71,417 (+4,220%).
Instance 15: paper=17,252, actual=2,825,530 (+16,277%).
**Hypothesis (in priority order):**
1. NSGA-II main loop not running full 150 generations — CT is 0.2s vs paper's 84s
2. Route decoding is wrong — open/closed route logic not correct
3. Objective function coefficients wrong (Eq.17-21)
4. STD spatial/temporal coefficients s=t=0.5 incorrect (NOTE-08)
**Affected files:** src/nsga2.py, src/algorithm.py, src/objectives.py, src/clustering.py
**Linked notes:** NOTE-07, NOTE-08, NOTE-09 in SRS.md

---

## [ISSUE-002] CT (computation time) far below paper values
**Status:** OPEN
**Priority:** HIGH
**Opened:** 2026-05-24
**Description:**
Instance 1: paper CT=84s, actual=0.2s. This 420x difference strongly suggests
the NSGA-II evolution loop is either not running at all or terminating after
very few generations.
**Hypothesis:** Early termination condition triggers too soon, or M_gen is not
being passed correctly, or the loop logic has a bug.
**Affected files:** src/nsga2.py, src/algorithm.py

---

## [ISSUE-003] NOTE-08 — s, t STD coefficients not given in paper
**Status:** OPEN
**Priority:** HIGH
**Opened:** 2026-05-24
**Description:**
SRS §3.1 notes that spatial (s) and temporal (t) coefficients in STD (Eq.49)
are inferred as 0.5/0.5 since the paper does not specify them.
These directly affect clustering quality, which affects all downstream results.
**Affected files:** src/clustering.py
**Action needed:** After fixing ISSUE-001 and ISSUE-002, tune s and t values
and compare TOC gap.

---

## [ISSUE-004] NOTE-09 — Chromosome length L ambiguity
**Status:** OPEN
**Priority:** MEDIUM
**Opened:** 2026-05-24
**Description:**
SRS §3.2 notes chromosome length L is unclear. Current implementation uses
L = |R| + |S| (static customers only). Dynamic customers are handled via
insertion strategy. Need to verify this is consistent with PMX crossover
and the paper's Fig.4 description.
**Affected files:** src/nsga2.py

---

## [ISSUE-005] NOTE-10 — Scenario 2 (goods transfer) mechanics unclear
**Status:** OPEN
**Priority:** MEDIUM
**Opened:** 2026-05-24
**Description:**
Dynamic insertion Scenario 2 (transfer delivery goods to free capacity) is
simplified. The exact transfer mechanics from the paper (Table 11) are not
fully described. Current implementation is a heuristic approximation.
**Affected files:** src/insertion_strategy.py
**Action needed:** Low priority until ISSUE-001 resolved. Revisit after TOC
gap is within 50%.

---

## [ISSUE-006] NOTE-04/05 — Undefined parameters w, C_e, IR
**Status:** OPEN
**Priority:** LOW
**Opened:** 2026-05-24
**Description:**
Parameters w, C_e, IR=1.1 appear in Table 15 of the paper but no equation
references them. Not currently implemented. Impact unknown.
**Affected files:** Unknown
**Action needed:** After main issues resolved, search paper more carefully
for these parameter usages.

---

## [ISSUE-007] β_f (depot fixed cost) set to 0
**Status:** OPEN
**Priority:** LOW
**Opened:** 2026-05-24
**Description:**
NOTE-07: β_f appears in Eq.21 (FC) but the paper doesn't give its value.
Set to 0. If paper uses a non-zero β_f, TOC will be systematically lower
in our results.
**Affected files:** src/objectives.py

---

## [ISSUE-008] BUG-CRITICAL: _check_feasibility_with_insertion always returns True
**Status:** OPEN
**Priority:** CRITICAL
**Opened:** 2026-05-25
**Description:**
`_check_feasibility_with_insertion` (insertion_strategy.py) ends with:
  `return eval_r.is_feasible or True  # Soft time windows: always feasible`
This means even when `evaluate_route` correctly detects a hard capacity violation
(is_feasible=False), the function ignores it and returns True. Hard capacity constraints
are never enforced in insertion feasibility checks.
**Impact:** Routes can be assigned dynamic customers that overflow vehicle capacity,
causing infeasible solutions with artificially low detour cost. Downstream evaluate_route
will flag infeasible but the solution is still accepted into the result.
**Affected files:** src/insertion_strategy.py line ~87
**Fix:** Change to `return True` (keep soft TW) but add explicit hard capacity check:
  `if current_load + customer.P_i > vehicle.capacity + 1e-6: return False`
  The existing capacity pre-check in scenario_1 handles this, so the main risk is
  when _check_feasibility_with_insertion is called for TW-only validation.
**Linked:** ISSUE-001

---

## [ISSUE-009] BUG-HIGH: scenario_1_direct_insert ignores delivery load in capacity check
**Status:** OPEN
**Priority:** HIGH
**Opened:** 2026-05-25
**Description:**
In `scenario_1_direct_insert`, the capacity available for a dynamic pickup customer
is computed as:
  `used_load = current_load  # = sum of existing PICKUP loads only`
  `available = route.vehicle.capacity - used_load`
The variable `delivery_load` is computed but never subtracted from available.
**Example:** Route with 80 delivery demand + 0 pickups: available = 100 - 0 = 100.
A dynamic customer with P_i=30 passes the check. But at the start of the route,
the vehicle carries 80 delivery goods + 30 pickup = 110 > capacity.
**Affected files:** src/insertion_strategy.py, scenario_1_direct_insert ~line 130
**Fix:** Change `used_load = current_load` to:
  `used_load = current_load + delivery_load` (or more precisely:
  the max concurrent load = max over all positions of (remaining_delivery + pickups_so_far))
  For a conservative fix: treat initial_available = capacity - delivery_load (worst case).
**Linked:** ISSUE-001, ISSUE-008

---

## [ISSUE-010] BUG-PERF: compute_similarity recomputes max_d on every call via O(N²) dict scan
**Status:** OPEN
**Priority:** MEDIUM
**Opened:** 2026-05-25
**Description:**
`compute_similarity` (nsga2.py) calls `list(instance.dist_matrix.values())` + `max()`
on every invocation to find max_d. dist_matrix has N² entries. For N=50 customers:
  - 2500 dict values scanned per call
  - local_search calls this for N*(N-1) ≈ 2450 pairs per trigger
  - At 33µs/call × 2450 calls = 81ms per local_search trigger
  - ~10 triggers per run = 810ms overhead per instance
**Affected files:** src/nsga2.py, compute_similarity
**Fix:** Pre-compute `max_d = float(instance._dist_arr.max())` once at local_search entry
and pass it as a parameter, or cache on instance as `instance._max_dist`.
**Linked:** performance

---

## [ISSUE-011] FINDING: TOC gap root cause decomposition (Instance 1, seed=42)
**Status:** OPEN
**Priority:** HIGH
**Opened:** 2026-05-25
**Description:**
Full TOC breakdown for current best (gen=150, pop=100):
  TOC=3816  (paper: 1654)
  TC=1045   (paper implied ≈304)  ← main culprit, 3.4x too high
  PC=1311   (paper implied ≈0)    ← second culprit, non-zero TW penalty
  MC=769    NV=7  (paper: MC=659, NV=6)
  IC=0, FC=691 (correct, constant)

TC is 3.4x too high → routes are ~3x longer in total distance.
Root causes (in order of impact):
  1. Routes have too many vehicles with short inefficient paths
     (NV=7-9 vs paper NV=6 → each extra vehicle adds a depot-return leg)
  2. Clustering assigns customers to suboptimal depots (s/t=0.5 NOTE-08)
  3. PC=1311 from TW violations despite l_i sort within routes
PC=1311 → the l_i-sort-within-route approach reduces but does not eliminate penalties.
The paper's PC ≈ 0 implies a fundamentally different route structure.
**Next action:** Investigate if open-route handling (DD→PD) reduces PC significantly,
and whether FC=691 matches paper. If paper uses different FC formula, TC estimate changes.

---

## [ISSUE-012] BUG-CRITICAL: Coordinate scale mismatch — TC = 1045 vs paper 192
**Status:** OPEN
**Priority:** CRITICAL
**Opened:** 2026-05-25
**Description:**
Through backward analysis of paper TOC=1654 for Instance 1:
  TOC = TC + PC + MC + IC + FC
  1654 = TC+PC + 659 (MC,NV=6) + 112 (IC) + 691 (FC)
  → TC + PC = 192

Physical minimum TC at current coord scale (6-route geo-cluster NN) = 1189.
TC=192 is **6.2× below our physical minimum** — unreachable at current scale.

Scale factor needed: 0.162 → 1 coord unit ≈ 160m (not 1km).

Evidence supporting scale=0.16:
- DD→PD at scale 0.16: 49.1×0.16 = 7.9 km ✓ (city logistics)
- Customer area: 149×0.16 = 24 km ✓ (Chongqing metro area)
- Our TC=1045 × 0.16 = 167 ≈ paper TC≈192 ✓ (within 13%)
- Paper coords created fresh (NOT from pr10 directly — pr10 depot at (425,170) vs Instance 1 at (-36,49))

**Affected files:** src/data_loader.py (coord loading) or src/data_model.py (distance computation)
**Fix:** Add a COORD_SCALE_FACTOR = 0.16 multiplier when computing Euclidean distances in
`build_distance_matrix()`, OR when loading x/y from CSV in `load_benchmark_instance()`.
**Must verify:** Does scale=0.16 also fix PC=1311→≈0? (travel times scale → TW compliance improves)
**Reference:** F-007 in findings.md, SRS §2.2 (Euclidean distance), ISSUE-001
**Linked:** ISSUE-001, ISSUE-011
