# Findings — mdpdtwdd-cli TOC Gap Investigation

## F-001 TOC Decomposition (2026-05-25, seed=42, gen=150, pop=100)
- TOC=3816 (before dynamic insertion) → 4260 (after, NV jumps 7→9)
- TC=1045, PC=1311, MC=769 (NV=7), IC=0, FC=691
- **TC paper implied ≈ 304** (= 1654 − 659 MC − 691 FC − 0 IC − 0 PC)
- TC ratio = 1045/304 = **3.44×** → routes tổng dài gấp 3.44× paper
- PC=1311 chiếm 31% TOC → significant contributor

## F-002 Dynamic Insertion Impact (2026-05-25)
- Pre-insertion: NV=7, TOC=3816
- Post-insertion: NV=9, TOC=4260 (delta=+444, NV+2)
- 5 dynamic customers → 2 new vehicles dispatched (scenario 3)
- 3 inserted into existing routes (scenario 1)
- Per-customer average cost: 444/5 = +88.8

## F-003 Route Structure (Instance 1)
- Clustering: Depot 1 (DD) gets 17 customers, Depot 2 (PD) gets 26 customers
- Total static customers: 43 (25 delivery + 18 pickup)
- Single DD + Single PD → open route possible when mixed delivery+pickup
- Current NV=7 before insertion → paper NV=6 (static only implied ≈4-5)

## F-004 Module Audit Results (2026-05-25)
- Bugs fixed: ISSUE-008 (or True), ISSUE-009 (delivery load), ISSUE-010 (max_d cache)
- All bugs in insertion_strategy.py and nsga2.py
- No TOC change after fix → bugs were correctness/perf, not root cause of gap
- Root cause still open: TC 3.4× high + PC 1311 non-zero

## F-005 Open Route Logic (from code inspection)
- `_get_route_endpoints`: mixed route → open (DD origin, PD end) ✓ in code
- BUT: cluster assignment assigns ALL customers (delivery+pickup) to ONE depot
- DD cluster: delivery customers → closed DD→DD route
- PD cluster: pickup customers → closed PD→PD route
- Mixed route only happens when BOTH delivery AND pickup customers end up in same cluster
- With 2 depots (1 DD, 1 PD): clustering tends to split by type → no mixed routes!
- **HYPOTHESIS H1 confirmed: open routes likely not being created at all**

## F-006 H1 FALSIFIED: All routes are already OPEN (2026-05-25)
- Verified: best solution has 7/7 routes as OPEN (DD→PD), 0 closed
- H1 eliminated as bug candidate
- Mixed customer types exist in both clusters (DD: 11R+6S+1D, PD: 14R+12S+4D)

## F-007 CRITICAL — Coordinate Scale Bug Discovered (2026-05-25)
**This is the root cause of TC=1045 vs paper TC≈192**

Evidence chain:
1. Paper TOC=1654, NV=6, MC=659, FC=691, IC=112 → TC+PC = **192**
2. TC = f_v × p_v × total_dist = 0.49 × dist → paper dist = **392 units**
3. Our PHYSICAL MINIMUM (6-route geo-cluster NN) = **2426 units** → TC=1189
4. Paper TC=192 is **6.2× below our physical minimum** — IMPOSSIBLE with current coords
5. Scale needed: 0.162 → 1 coord unit = **163m** not 1km

Root cause: paper created benchmark coords from scratch (NOT from pr10 directly).
pr10 depot at (425,170), Instance 1 depot at (-36,49) — completely different.
Paper likely uses coords in units of **~0.16km (160m)** not 1km.

Alternative explanation: FC=691 is CORRECT but paper may NOT include δ×ΣQ+χ×ΣP in FC.
If paper FC ≈ 0 (only β_f which is very small), then TC+PC = 1654-659-0-112 = 883.
Then TC_min_needed = 883-PC ≈ 400-500.
But our physical min TC = 1189 (6.2× > 192) or at best 394 units×0.49 = 193 if scale=0.16.

**ACTUAL SCALE HYPOTHESIS:**
- If each coord unit = 0.16km: our TC=1045 → scaled = 1045×0.16 = 167 ≈ 192 ✓ (close!)
- Need to verify: case study uses actual km (confirmed), benchmarks use a different scale
- Scale factor ≈ 0.18 (= 192/1045)

**NEXT ACTION**: Verify by checking if coords×0.16 make physical sense:
- DD→PD distance = 49.1 units × 0.16 = 7.9 km ✓ (reasonable city distance)
- Customer span = 149 units × 0.16 = 24 km ✓ (reasonable city area)
- Travel time DD→customer: 49.1×0.16/30 h = 16 minutes ✓
