# SKILL.md — mdpdtwdd-cli

> Agent onboarding guide. Read this in full before touching any code.

---

## 1. What is this project?

Python CLI implementing **3DAPANSGA-II** for the **MDPDTWDD** problem:
> Multi-Depot Pickup and Delivery VRP with Time Windows and Dynamic Demands

**Paper:** Wang, Gou, Luo, Fan, Wang (2025). *Engineering Applications of Artificial Intelligence*, 139, 109700.

**Goal:** Reproduce Table 16 of the paper — match TOC, NV, CT values within acceptable tolerance.

---

## 2. Repository layout

```
mdpdtwdd-cli/
├── main.py                    # CLI entry point
├── SRS.md                     # Full algorithm spec (READ THIS — authoritative source)
├── src/
│   ├── data_model.py          # Node, Vehicle, Route, Solution, ProblemInstance
│   ├── data_loader.py         # CSV parsers (benchmark + case study)
│   ├── objectives.py          # TOC/NV cost functions (Eq.15-21), fitness (Eq.54)
│   ├── clustering.py          # 3D AP clustering (Eq.49-53)
│   ├── nsga2.py               # ANSGA-II: crossover, mutation, NSGA-II sort, local search
│   ├── insertion_strategy.py  # Dynamic demand insertion (Table 11, 3 scenarios)
│   ├── algorithm.py           # Main orchestrator
│   └── result_logger.py       # JSONL result logging
├── data/
│   └── process/benchmark/     # 30 benchmark CSVs (Instance 1–30)
│   └── process/case/          # Chongqing case study CSV
├── mainPaper/                 # Paper PDF + math blocks reference
├── logs/
│   ├── CHANGELOG.md           # ← ALL code changes logged here
│   ├── ISSUES.md              # ← ALL open/closed issues logged here
│   ├── EXPERIMENTS.md         # ← ALL test runs logged here
│   ├── benchmark_results.jsonl
│   └── *.jsonl
└── tests/
    └── test_data_loader.py
```

---

## 3. Quick start (after clone)

```bash
cd mdpdtwdd-cli

# Check instance info
python main.py info --instance "data/process/benchmark/1 Instance__Sheet1.csv"

# Solve single instance
python main.py solve --instance "data/process/benchmark/1 Instance__Sheet1.csv" --m-gen 150 --n-ind 100 --seed 42 --verbose

# Run all 30 benchmarks
python main.py benchmark --dir "data/process/benchmark" --runs 1 --log logs/benchmark_results.jsonl

# Summarize results
python main.py summary --log logs/benchmark_results.jsonl
```

---

## 4. Algorithm overview

### Stage 1 — 3D AP Clustering (src/clustering.py)
- Affinity Propagation with spatial-temporal distance (STD, Eq.49)
- Depots forced as exemplars
- Output: customer → depot assignment

### Stage 2 — ANSGA-II (src/nsga2.py)
- Chromosome: permutation of static customer IDs
- Crossover: PMX (Fig.4)
- Mutation: swap with decaying probability (Eq.55)
- Fitness: `1 / (TOC/TOC_max + NV/NV_max)` (Eq.54)
- NSGA-II fast nondominated sort + crowding distance
- Local search: triggered every R_Lg=15 no-improvement gens

### Dynamic insertion (src/insertion_strategy.py)
- 3 scenarios: direct insert / goods transfer / new vehicle
- Applied after Stage 2 for each dynamic customer

---

## 5. Paper target values (Table 16)

| Instance | DDs | PDs | Customers | TOC($) | NV | CT(s) |
|----------|-----|-----|-----------|--------|----|-------|
| 1        | 1   | 1   | 48        | 1,654  | 6  | 84    |
| 5        | 1   | 1   | 150       | 13,177 | 21 | 481   |
| 11       | 2   | 1   | 48        | 1,313  | 5  | 119   |
| 15       | 2   | 1   | 150       | 17,252 | 31 | 430   |
| 30       | 3   | 1   | 150       | 4,731  | 19 | 598   |
| **Avg**  | -   | -   | -         | **4,096** | **14** | **373** |

---

## 6. Current status (2026-05-24)

⚠️ **Algorithm NOT reproducing paper results.**

| Instance | Paper TOC | Actual TOC | Gap       | CT paper | CT actual |
|----------|-----------|------------|-----------|----------|-----------|
| 1        | 1,654     | 71,417     | **+4,220%** | 84s    | 0.2s      |
| 5        | 13,177    | 387,556    | **+2,841%** | 481s   | 2.3s      |
| 11       | 1,313     | 17,630     | **+1,243%** | 119s   | 0.2s      |
| 15       | 17,252    | 2,825,530  | **+16,277%**| 430s   | 2.9s      |

**Root cause hypothesis (priority order):**
1. NSGA-II loop likely not running full M_gen=150 iterations or converging too fast
2. s/t=0.5 STD coefficients (NOTE-08) may be wrong — affects clustering quality
3. Route decoding may be incorrect — open vs closed routes not handled properly
4. Objective function coefficients (Eq.17-21) may have errors

See `logs/ISSUES.md` for full issue tracker.

---

## 7. Known algorithm parameters

From SRS.md (Table 15):

| Param    | Value  | Notes                                    |
|----------|--------|------------------------------------------|
| M_gen    | 150    | Max generations                          |
| N_IND    | 100    | Population size                          |
| cp       | 0.90   | Crossover probability                    |
| mp       | 0.05   | Initial mutation prob (decays per Eq.55) |
| R_c      | min(5, C_n) | Removed customers in local search   |
| R_Lg     | 15     | Local search no-improvement trigger      |
| ∂_v      | 100    | Vehicle capacity                         |
| α_v      | 30     | Vehicle speed                            |
| f_v      | 0.07   | Fuel consumption rate                    |
| p_v      | 7      | Fuel price                               |
| M_v      | 40,000 | Annual maintenance cost                  |
| T        | 364    | Working days/year                        |
| ε        | 20     | Early arrival penalty                    |
| ω        | 30     | Late arrival penalty                     |
| s, t     | 0.5    | ⚠️ STD spatial/temporal coeffs (inferred)|

---

## 8. Rules for all agents

> These are mandatory. Read before writing a single line.

1. **Read SRS.md first.** It's the authoritative spec. Cross-check every implementation decision against it.
2. **Log every change** in `logs/CHANGELOG.md` immediately after making it.
3. **Log every test run** in `logs/EXPERIMENTS.md` — include command, results, TOC/NV/CT.
4. **Log every new issue** in `logs/ISSUES.md` — include ID, description, status.
5. **Never delete or overwrite log files.** Append only.
6. **One change at a time.** Fix one thing, test, log, then move to next.
7. **Track TOC gap** — Instance 1 is the fastest to test. Always report gap vs paper.
8. **Check CT** — if CT < 10s for instance 1, the main loop is likely under-running.
9. **Comment every non-obvious implementation** with `# SRS §X.Y` or `# Eq.NN` references.
10. **Do not modify `data/` files.** They are read-only benchmark data.

---

## 9. File change workflow

```
1. Read current state of the file
2. Make targeted change (one logical fix at a time)
3. Run: python main.py solve --instance "data/process/benchmark/1 Instance__Sheet1.csv" --seed 42
4. Append result to logs/EXPERIMENTS.md
5. Append change description to logs/CHANGELOG.md
6. If new bug found → append to logs/ISSUES.md
7. Commit: git add -A && git commit -m "fix: <short description>"
```

---

## 10. Reading the paper

The paper PDF is at `mainPaper/25-The multi-depot pickup and delivery vehicle routing problem with time.pdf`.
The English markdown translation is at `mainPaper/ENG The multi-depot... .md`.
Math blocks are extracted at `mainPaper/paper_math_blocks.md`.

Key sections:
- Section 4.2 → Clustering (Eq.49-53)
- Section 4.3 → ANSGA-II (Eq.54-56, Tables 8-10, Fig.4)
- Section 4.4 → Dynamic insertion (Table 11)
- Table 15 → All algorithm parameters
- Table 16 → Target benchmark results
