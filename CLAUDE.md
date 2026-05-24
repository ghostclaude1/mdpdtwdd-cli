# CLAUDE.md — Agent Instructions for mdpdtwdd-cli

> This file is read automatically by Claude Code when opening this project.
> Read it before doing anything else.

---

## What this project is

Python CLI implementing **3DAPANSGA-II** for MDPDTWDD (Multi-Depot Pickup & Delivery VRP with Time Windows & Dynamic Demands).

**Paper:** Wang et al. (2025), EAAI 139, 109700.
**Goal:** Reproduce Table 16 benchmark results.

---

## Before writing any code — read these files

```
1. skills/mdpdtwdd-cli/SKILL.md       ← full project overview + current status
2. SRS.md                              ← authoritative algorithm specification
3. logs/ISSUES.md                      ← all open bugs (read before starting)
4. logs/EXPERIMENTS.md (last 2 entries) ← recent test context
```

Path from workspace root: all under `mdpdtwdd-cli/`

---

## 🔴 Mandatory — Log everything

| What happened | Where to log |
|--------------|--------------|
| Any code change | `logs/CHANGELOG.md` |
| Any test/run | `logs/EXPERIMENTS.md` |
| New bug found | `logs/ISSUES.md` (new entry) |
| Bug fixed | `logs/ISSUES.md` (update status to CLOSED) |

**Logs are append-only. Never delete or overwrite entries.**

---

## Quick test command (use after every change)

```bash
python main.py solve \
  --instance "data/process/benchmark/1 Instance__Sheet1.csv" \
  --seed 42 \
  --verbose
```

**Baseline:** TOC=71,417 (+4,220% vs paper 1,654), CT=0.2s (paper: 84s)
If CT < 10s after your change, the main loop is still broken.

---

## Current priority issues

1. **ISSUE-002** (HIGH) — CT only 0.2s, NSGA-II not running properly
2. **ISSUE-001** (CRITICAL) — TOC 40x too high
3. **ISSUE-003** (HIGH) — STD coefficients s/t unknown

See `logs/ISSUES.md` for full details.

---

## Commit format

```bash
git add -A
git commit -m "fix(nsga2): <short description of what was fixed>"
```

Types: `fix`, `feat`, `refactor`, `test`, `docs`
Always update logs BEFORE committing.
