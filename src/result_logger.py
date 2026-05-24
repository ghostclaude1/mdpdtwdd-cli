"""
Result logging for experimental reproduction.

Logs results in JSONL format for easy analysis and comparison with paper tables.
Each run is logged with: instance, algorithm params, results, timestamp.
"""
from __future__ import annotations
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.algorithm import RunResult
from src.data_model import ProblemInstance


def log_result(
    logfile: str,
    instance: ProblemInstance,
    run_result: RunResult,
    run_number: int = 1,
    algorithm: str = "3DAPANSGA-II",
    extra: Optional[dict] = None,
) -> None:
    """
    Append a run result to the JSONL log file.

    Log format (mirrors paper Table 16 columns):
    {
      "timestamp": "ISO8601",
      "instance": "Instance_1",
      "algorithm": "3DAPANSGA-II",
      "run": 1,
      "TOC": 1654.0,
      "NV": 6,
      "CT_s": 84.3,
      "n_customers": 48,
      "n_DD": 1,
      "n_PD": 1,
      "n_static_delivery": 25,
      "n_static_pickup": 18,
      "n_dynamic": 5,
      "notes": [],
      "extra": {}
    }
    """
    Path(logfile).parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp": datetime.now().isoformat(),
        "instance": instance.name,
        "algorithm": algorithm,
        "run": run_number,
        "TOC": round(run_result.best_toc, 2),
        "NV": run_result.best_nv,
        "CT_s": round(run_result.computation_time, 1),
        "n_customers": len(instance.all_customers),
        "n_DD": len(instance.delivery_depots),
        "n_PD": len(instance.pickup_depots),
        "n_static_delivery": len(instance.static_delivery_customers),
        "n_static_pickup": len(instance.static_pickup_customers),
        "n_dynamic": len(instance.dynamic_customers),
        "notes": run_result.notes,
        "extra": extra or {},
    }

    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def compute_toc_gap(toc_algo: float, toc_reference: float) -> float:
    """TOC gap = (algo - reference) / reference * 100 (%)"""
    if toc_reference == 0:
        return 0.0
    return (toc_algo - toc_reference) / toc_reference * 100.0


def summarize_log(logfile: str) -> str:
    """
    Read the log file and produce a summary table matching paper format.
    """
    if not os.path.exists(logfile):
        return "Log file not found."

    records = []
    with open(logfile, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not records:
        return "No records found."

    # Group by instance
    by_instance = {}
    for r in records:
        key = r['instance']
        if key not in by_instance:
            by_instance[key] = []
        by_instance[key].append(r)

    lines = ["=" * 80]
    lines.append("RESULT SUMMARY")
    lines.append("=" * 80)
    lines.append(f"{'Instance':<15} {'DD':>4} {'PD':>4} {'C':>5} {'Best TOC':>10} {'NV':>4} {'CT(s)':>8} {'Runs':>5}")
    lines.append("-" * 80)

    for instance_name, runs in sorted(by_instance.items()):
        best_run = min(runs, key=lambda r: r['TOC'])
        lines.append(
            f"{instance_name:<15} "
            f"{best_run['n_DD']:>4} "
            f"{best_run['n_PD']:>4} "
            f"{best_run['n_customers']:>5} "
            f"{best_run['TOC']:>10.1f} "
            f"{best_run['NV']:>4} "
            f"{best_run['CT_s']:>8.1f} "
            f"{len(runs):>5}"
        )

    lines.append("=" * 80)
    return "\n".join(lines)
