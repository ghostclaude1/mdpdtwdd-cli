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
