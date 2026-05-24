#!/usr/bin/env python3
"""
MDPDTWDD CLI — 3DAPANSGA-II Implementation
Paper: Wang et al. (2025), EAAI 139, 109700

Usage:
  python main.py solve --instance <path>
  python main.py benchmark --dir <benchmark_dir> [--runs N] [--log <logfile>]
  python main.py case --data <case_csv>
  python main.py summary --log <logfile>
  python main.py info --instance <path>
"""
import argparse
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_loader import load_benchmark_instance, load_case_study, load_all_benchmark_instances
from src.algorithm import AlgorithmParams, run_3dapansga2
from src.result_logger import log_result, summarize_log, compute_toc_gap


def cmd_solve(args):
    """Solve a single instance."""
    print(f"Loading instance: {args.instance}")
    instance = load_benchmark_instance(args.instance)
    print(instance.summary())

    params = AlgorithmParams(
        m_gen=args.m_gen,
        n_ind=args.n_ind,
        random_seed=args.seed,
    )

    print(f"Running 3DAPANSGA-II (gen={params.m_gen}, pop={params.n_ind})...")
    result = run_3dapansga2(instance, params, verbose=args.verbose)

    print(f"\n{'='*50}")
    print(f"TOC:  ${result.best_toc:,.2f}")
    print(f"NV:   {result.best_nv}")
    print(f"CT:   {result.computation_time:.1f}s")
    if result.notes:
        print("\nNotes:")
        for note in result.notes:
            print(f"  - {note}")

    if args.log:
        log_result(args.log, instance, result, extra={"cmd": "solve"})
        print(f"\nResult logged to: {args.log}")


def cmd_benchmark(args):
    """
    Run on all 30 benchmark instances.
    Reproduces Table 16 of the paper.
    """
    bench_dir = args.dir
    runs = getattr(args, 'runs', 1)
    logfile = getattr(args, 'log', 'logs/benchmark_results.jsonl')

    print(f"Loading benchmark instances from: {bench_dir}")
    instances = load_all_benchmark_instances(bench_dir)
    print(f"Found {len(instances)} instances.\n")

    params = AlgorithmParams(
        m_gen=getattr(args, 'm_gen', 150),
        n_ind=getattr(args, 'n_ind', 100),
        random_seed=getattr(args, 'seed', None),
    )

    # Paper reference values from Table 16 (3DAPANSGA-II column)
    # TOC, NV, CT reference from paper
    paper_reference = {
        1: (1654, 6, 84),  2: (2715, 9, 142), 3: (3362, 14, 208),
        4: (8785, 20, 666), 5: (13177, 21, 481),
        6: (1577, 6, 131),  7: (2094, 8, 365),  8: (2926, 11, 392),
        9: (5399, 18, 273), 10: (5682, 19, 370),
        11: (1313, 5, 119), 12: (1687, 7, 197), 13: (3457, 14, 404),
        14: (3643, 15, 332), 15: (17252, 31, 430),
        16: (1549, 6, 169), 17: (2380, 11, 196), 18: (2973, 12, 253),
        19: (3497, 16, 261), 20: (4485, 18, 886),
        21: (1568, 7, 280), 22: (2270, 10, 389), 23: (3377, 15, 525),
        24: (3403, 15, 371), 25: (6874, 31, 827),
        26: (1252, 4, 129), 27: (2105, 10, 445), 28: (4256, 19, 618),
        29: (3433, 16, 652), 30: (4731, 19, 598),
    }

    print(f"{'#':<5} {'Instance':<15} {'C':>5} {'TOC':>9} {'NV':>4} {'CT(s)':>7} "
          f"{'Ref TOC':>9} {'Gap%':>7}")
    print("-" * 70)

    for i, instance in enumerate(instances, 1):
        best_toc = float('inf')
        best_nv = 0
        best_ct = 0.0

        for run_n in range(1, runs + 1):
            result = run_3dapansga2(instance, params, verbose=args.verbose)
            if result.best_toc < best_toc:
                best_toc = result.best_toc
                best_nv = result.best_nv
                best_ct = result.computation_time
            log_result(logfile, instance, result, run_number=run_n,
                       extra={"benchmark_idx": i})

        # Compare with paper
        ref = paper_reference.get(i)
        if ref:
            gap = compute_toc_gap(best_toc, ref[0])
            ref_str = f"${ref[0]:>7,}"
            gap_str = f"{gap:>+7.2f}%"
        else:
            ref_str = "N/A"
            gap_str = "N/A"

        print(f"{i:<5} {instance.name:<15} {len(instance.all_customers):>5} "
              f"${best_toc:>8,.0f} {best_nv:>4} {best_ct:>7.1f}s "
              f"{ref_str} {gap_str}")

    print(f"\nAll results logged to: {logfile}")
    print("\n" + summarize_log(logfile))


def cmd_case(args):
    """Run on the Chongqing case study."""
    print(f"Loading case study: {args.data}")
    instance = load_case_study(args.data)
    print(instance.summary())

    params = AlgorithmParams(
        m_gen=getattr(args, 'm_gen', 150),
        n_ind=getattr(args, 'n_ind', 100),
        random_seed=getattr(args, 'seed', None),
    )

    print("Running 3DAPANSGA-II on case study...")
    result = run_3dapansga2(instance, params, verbose=True)

    print(f"\n{'='*50}")
    print(f"TOC:  ${result.best_toc:,.2f}")
    print(f"NV:   {result.best_nv}")
    print(f"CT:   {result.computation_time:.1f}s")

    logfile = getattr(args, 'log', 'logs/case_results.jsonl')
    log_result(logfile, instance, result, extra={"cmd": "case"})
    print(f"\nResult logged to: {logfile}")


def cmd_info(args):
    """Show instance details without running."""
    instance = load_benchmark_instance(args.instance)
    print(instance.summary())

    print("Sample nodes:")
    for node in list(instance.nodes.values())[:10]:
        print(f"  {node}")


def cmd_summary(args):
    """Print summary of logged results."""
    if not os.path.exists(args.log):
        print(f"Log file not found: {args.log}")
        sys.exit(1)
    print(summarize_log(args.log))


def main():
    parser = argparse.ArgumentParser(
        description="MDPDTWDD CLI — 3DAPANSGA-II (Wang et al. 2025)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest='command')

    # solve
    p_solve = subparsers.add_parser('solve', help='Solve a single instance')
    p_solve.add_argument('--instance', required=True, help='Path to instance CSV')
    p_solve.add_argument('--m-gen', type=int, default=150)
    p_solve.add_argument('--n-ind', type=int, default=100)
    p_solve.add_argument('--seed', type=int, default=None)
    p_solve.add_argument('--log', default='logs/results.jsonl')
    p_solve.add_argument('--verbose', action='store_true')

    # benchmark
    p_bench = subparsers.add_parser('benchmark', help='Run all 30 benchmark instances')
    p_bench.add_argument('--dir', required=True, help='Directory containing benchmark CSVs')
    p_bench.add_argument('--runs', type=int, default=1, help='Runs per instance (paper: 10)')
    p_bench.add_argument('--m-gen', type=int, default=150)
    p_bench.add_argument('--n-ind', type=int, default=100)
    p_bench.add_argument('--seed', type=int, default=None)
    p_bench.add_argument('--log', default='logs/benchmark_results.jsonl')
    p_bench.add_argument('--verbose', action='store_true')

    # case
    p_case = subparsers.add_parser('case', help='Run Chongqing case study')
    p_case.add_argument('--data', required=True, help='Path to case study CSV')
    p_case.add_argument('--m-gen', type=int, default=150)
    p_case.add_argument('--n-ind', type=int, default=100)
    p_case.add_argument('--seed', type=int, default=None)
    p_case.add_argument('--log', default='logs/case_results.jsonl')
    p_case.add_argument('--verbose', action='store_true')

    # info
    p_info = subparsers.add_parser('info', help='Show instance info')
    p_info.add_argument('--instance', required=True)

    # summary
    p_summary = subparsers.add_parser('summary', help='Summarize logged results')
    p_summary.add_argument('--log', required=True)

    args = parser.parse_args()

    if args.command == 'solve':
        cmd_solve(args)
    elif args.command == 'benchmark':
        cmd_benchmark(args)
    elif args.command == 'case':
        cmd_case(args)
    elif args.command == 'info':
        cmd_info(args)
    elif args.command == 'summary':
        cmd_summary(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
