# Software Requirements Specification (SRS)
## MDPDTWDD CLI — 3DAPANSGA-II Python Implementation

**Paper:** Wang, Gou, Luo, Fan, Wang (2025). "The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands." *Engineering Applications of Artificial Intelligence*, 139, 109700.

**Purpose of this SRS:** Enable any agent or developer to implement or reproduce the exact algorithm as implemented here, with full traceability to the paper.

---

## 1. System Overview

A Python CLI tool that implements the 3DAPANSGA-II algorithm for the MDPDTWDD problem. The system:
- Loads benchmark instances from CSV format
- Runs the two-stage hybrid optimization algorithm
- Handles dynamic demand insertion
- Logs all experimental results
- Reports TOC, NV, and CT for comparison with paper tables

---

## 2. Problem Formulation

### 2.1 Problem: MDPDTWDD
Multi-Depot Pickup and Delivery VRP with Time Windows and Dynamic Demands.

**Sets:**
- `W` = Delivery Depots (DDs)
- `O` = Pickup Depots (PDs)
- `F = W ∪ O` = All depots
- `R` = Static delivery customers
- `S` = Static pickup customers
- `D` = Dynamic pickup customers
- `C = R ∪ S ∪ D` = All customers

**Objectives (bi-objective):**
- min TOC = TC + PC + MC + IC + FC (Eq.15)
- min NV = Σ_v Σ_{i∈F} Σ_{j∈C} x_ij^v (Eq.16)

### 2.2 Cost Components
- TC (Eq.17): `Σ f_v * p_v * x_ij^v * d_ij` = fuel cost per unit distance
- PC (Eq.18): `Σ ε*max{l_i-A_vi,0} + ω*max{A_vi-r_i,0}` = soft time window penalty
- MC (Eq.19): `Σ M_v * x_ij^v / T` for i∈F, j∈C = per-vehicle daily maintenance
- IC (Eq.20): `Σ y_if^v * P_i * γ` for dynamic customers = insertion handling cost
- FC (Eq.21): `Σ β_f + δ*ΣQ_i + χ*ΣP_i` = fixed depot + per-unit delivery/pickup cost

### 2.3 Parameters (Table 15)
| Parameter | Value | Notes |
|-----------|-------|-------|
| M_gen | 150 | Max generations |
| N_IND | 100 | Population size |
| cp | 0.90 | Crossover probability |
| mp | 0.05 | Initial mutation probability (decays per Eq.55) |
| R_c | min(5, C_n) | Removed customers in local search |
| R_Lg | 15 | Local search no-improvement trigger |
| ∂_v | 100 | Vehicle capacity |
| α_v | 30 | Vehicle speed |
| f_v | 0.07 | Fuel consumption rate |
| p_v | 7 | Fuel price |
| M_v | 40,000 | Annual maintenance cost |
| T | 364 | Working days/year |
| ε | 20 | Early arrival penalty coefficient |
| ω | 30 | Late arrival penalty coefficient |
| δ | 1 | Delivery cost coefficient |
| χ | 1 | Pickup cost coefficient |
| γ | 1 | Dynamic insertion cost coefficient |
| β_f | 0 | Depot fixed cost (**NOTE-07**: not in paper) |
| gp | 0.90 | **NOTE-03**: used as tournament selection prob |
| s | 0.5 | **NOTE-08**: spatial coeff in STD, inferred |
| t | 0.5 | **NOTE-08**: temporal coeff in STD, inferred |
| w, C_e, IR | — | **NOTE-04, 05**: in Table 15 but no equation found |

---

## 3. Algorithm Specification

### 3.1 Stage 1: 3D AP Clustering (Section 4.2)

```
Input: all nodes (customers + depots), λ', M
Output: cluster assignment (customer → depot)

1. Initialize: depots as forced exemplars
2. Compute similarity S using STD (Eq.49):
   STD_ij = s*d_ij + t*min{|l_i-l_j|, |l_i-r_j|, |r_i-l_j|, |r_i-r_j|} * α_v
3. Init R=0, A=0
4. For m=1..M:
   R_{m+1}(i,j) = S(i,j) - max_{j'≠j}{A_m(i,j')+S(i,j')}   [Eq.50]
   A_{m+1}(i,j) = min{0, R_m(j,j)+Σ_{j'∉{i,j}} max{0,R_m(j',j)}}  [Eq.51, i≠j]
   A_{m+1}(j,j) = Σ_{j'≠j} max{0,R_m(j',j)}                        [Eq.51, i=j]
   R_{m+1} = λ'*R_m + (1-λ')*R_{m+1}  [Eq.52]
   A_{m+1} = λ'*A_m + (1-λ')*A_{m+1}  [Eq.53]
   Assign each customer to highest-similarity depot
   If no change: break
5. Return assignment
```

### 3.2 Stage 2: ANSGA-II (Section 4.3)

**Chromosome encoding** (NOTE-09):
- Genes = permutation of static customer IDs (|R|+|S| genes)
- Dynamic customers handled separately by insertion strategy
- Cluster map: gene → depot (from Stage 1)

**Decoding:** Group genes by cluster, form routes per depot group.
- Mixed route (delivery+pickup on same vehicle): open route, start at DD → end at PD
- Single-type route: closed route

**Fitness (Eq.54):** `fit = 1/(TOC/TOC_max + NV/NV_max)`

**Crossover:** PMX (Partial Mapped Crossover, Fig.4):
1. Select [L_p1, L_p2]
2. Swap segments
3. Fix duplicates via mapping chain

**Mutation (Eq.55, Table 8):**
- With prob mp: swap genes at positions L_p1, L_p2
- mp decays: `mp = mp_init * (1 - gen/M_gen)`

**Nondominated sort + crowding distance (Table 10):**
- NSGA-II fast-sort
- Rank + crowding distance for selection
- Merge P+F → select top N_IND

**Local Search (Table 9, Eq.56):**
- Trigger: gbest no improvement for R_Lg generations
- Similarity: `s_ij = 1/(x_ij + d_ij/max{d_ij})`
- Destroy: remove R_c most similar customers to seed
- Repair: greedy re-insertion in best position

### 3.3 Dynamic Insertion Strategy (Section 4.4, Table 11)

For each dynamic customer k (in order of known_time):
1. **Scenario 1 (direct insert):** Find min-cost insertion position across all routes.
   Feasibility: capacity + time window check.
2. **Scenario 2 (goods transfer):** Transfer delivery goods to another vehicle to free capacity.
   *NOTE-10: Simplified implementation — see findings.md*
3. **Scenario 3 (new vehicle):** Dispatch new vehicle from nearest pickup depot.
4. Select minimum-cost feasible scenario.

---

## 4. Data Format

### 4.1 Benchmark CSV Format
```
Columns: Nodes, X, Y, Delivery demands, Picku up demands (typo in source),
         Time windows left D, Time windows right D,
         Time windows left P, Time windows right P,
         Known time, DCs, PCs

Node type detection (NOTE-01: inferred from data patterns):
- DCs=1000 → Delivery Depot (DD)
- PCs=1000 → Pickup Depot (PD)
- DCs=1, Delivery demand>0 → Static delivery customer (R)
- PCs=1, Pickup demand>0, Known time=0 → Static pickup customer (S)
- PCs=4, Pickup demand>0, Known time>0 → Dynamic pickup customer (D)
```

### 4.2 Case Study CSV Format
```
Columns: No., Longitude, Latitude, Delivery demand, Pickup demand,
         Left/Right time for delivering, Left/Right time for pickup,
         Responsible DD, Responsible PD

Node type detection by label prefix (DD*, PD*) or demand values.
```

---

## 5. Result Logging

JSONL format in `logs/`:
```json
{
  "timestamp": "2026-05-24T...",
  "instance": "Instance_1",
  "algorithm": "3DAPANSGA-II",
  "run": 1,
  "TOC": 1654.0,
  "NV": 6,
  "CT_s": 84.3,
  "n_customers": 48,
  "n_DD": 1,
  "n_PD": 1,
  ...
}
```

---

## 6. File Structure

```
mdpdtwdd-cli/
├── main.py                  # CLI entry point
├── SRS.md                   # This file
├── src/
│   ├── __init__.py
│   ├── data_model.py        # Data structures (Node, Vehicle, Route, Solution, ProblemInstance)
│   ├── data_loader.py       # CSV parsers for benchmark and case study
│   ├── objectives.py        # TOC/NV objectives (Eq.15-21), fitness (Eq.54), dominance
│   ├── clustering.py        # 3D AP clustering (Eq.49-53, Table 6)
│   ├── nsga2.py             # ANSGA-II: crossover, mutation, sorting, local search
│   ├── insertion_strategy.py # Dynamic insertion (Table 11)
│   ├── algorithm.py         # Main orchestrator (Fig.2)
│   └── result_logger.py     # JSONL result logging
├── tests/
│   └── test_data_loader.py  # Data loading tests
└── logs/                    # Output logs
```

---

## 7. Known Limitations / NOTES

| ID | Issue | Impact | Action |
|----|-------|--------|--------|
| NOTE-01 | Dynamic customer encoding (PCs=4) inferred | Medium | Verified against data patterns |
| NOTE-02 | Raw .vrp not used for benchmarks | Low | Use CSV benchmarks |
| NOTE-03 | "gp=0.90" undefined | Low | Tournament selection prob |
| NOTE-04 | "w, C_e" undefined | Unknown | Not implemented |
| NOTE-05 | "IR=1.1" undefined | Unknown | Not implemented |
| NOTE-06 | MC counts depot→customer only | Low | Consistent with NV |
| NOTE-07 | β_f (depot fixed cost) not given | Medium | Set to 0.0 |
| NOTE-08 | s, t coefficients in STD not given | High | Default 0.5, 0.5 |
| NOTE-09 | Chromosome length L unclear | Medium | L=n1+n2 (static customers) |
| NOTE-10 | Scenario 2 mechanics unclear | Medium | Simplified implementation |

**⚠ HIGH IMPACT NOTE:** Notes 7, 8, and 9 most likely affect result quality.
The β_f=0 and s/t=0.5 assumptions directly impact TOC values.
If results diverge significantly from paper, these should be revisited first.

---

## 8. Expected Results (Paper Table 16, 3DAPANSGA-II column)

| Instance | DDs | PDs | Customers | TOC($) | NV | CT(s) |
|----------|-----|-----|-----------|--------|----|----|
| 1 | 1 | 1 | 48 | 1654 | 6 | 84 |
| 5 | 1 | 1 | 150 | 13177 | 21 | 481 |
| 11 | 2 | 1 | 48 | 1313 | 5 | 119 |
| 15 | 2 | 1 | 150 | 17252 | 31 | 430 |
| 30 | 3 | 1 | 150 | 4731 | 19 | 598 |
| **Avg** | - | - | - | **4096** | **14** | **373** |

---

## 9. CLI Commands

```bash
# Show instance info
python main.py info --instance <path.csv>

# Solve single instance
python main.py solve --instance <path.csv> [--m-gen 150] [--n-ind 100] [--seed N] [--verbose]

# Run all 30 benchmark instances (reproduces Table 16)
python main.py benchmark --dir <benchmark_dir> [--runs 10] [--log logs/results.jsonl]

# Run case study
python main.py case --data <case.csv>

# Summarize results
python main.py summary --log <logfile>
```
