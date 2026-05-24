"""
3DAPANSGA-II: Main algorithm orchestrator.

Implements the full two-stage hybrid algorithm from Section 4.1 (Fig. 2):
Stage 1: 3D AP Clustering → assign customers to depots
Stage 2: ANSGA-II → find Pareto optimal solutions
         (genetic ops + local search + Pareto management)
+ Dynamic insertion strategy for dynamic demands

Parameters from Table 15:
  M_gen = 150, N_IND = 100, cp = 0.90, mp = 0.05
  R_c = min(5, C_n), R_Lg = 15
"""
from __future__ import annotations
import time
import random
import copy
from dataclasses import dataclass, field
from typing import Optional

from src.data_model import ProblemInstance, Solution, Vehicle, NodeType
from src.clustering import APClustering3D, cluster_by_depot_type
from src.nsga2 import (
    Chromosome, decode_chromosome, initialize_population,
    pmx_crossover, mutate, adaptive_mutation_rate,
    fast_nondominated_sort, crowding_distance_assignment,
    tournament_selection, local_search,
)
from src.insertion_strategy import insert_dynamic_demands
from src.objectives import evaluate_solution, dominates


@dataclass
class AlgorithmParams:
    """Parameters for 3DAPANSGA-II (Table 15)."""
    m_gen: int = 150            # Max generations
    n_ind: int = 100            # Population size
    cp: float = 0.90            # Crossover probability
    mp: float = 0.05            # Initial mutation probability
    gp: float = 0.90            # Tournament selection probability (NOTE-03: inferred)
    r_c_max: int = 5            # Max removed customers in local search
    r_lg: int = 15              # Local search trigger (no improvement streak)
    vehicle_capacity: float = 100.0
    vehicle_speed: float = 30.0
    fuel_rate: float = 0.07
    fuel_price: float = 7.0
    annual_maintenance: float = 40000.0
    working_days: int = 364
    epsilon: float = 20.0
    omega: float = 30.0
    delta: float = 1.0
    chi: float = 1.0
    gamma: float = 1.0
    ap_damping: float = 0.9
    ap_max_iter: int = 200
    s_coeff: float = 0.5        # Spatial coefficient in STD (NOTE-08)
    t_coeff: float = 0.5        # Temporal coefficient in STD (NOTE-08)
    random_seed: Optional[int] = None


@dataclass
class RunResult:
    """Results from one algorithm run."""
    best_toc: float
    best_nv: int
    computation_time: float
    pareto_front: list[Solution] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def run_3dapansga2(
    instance: ProblemInstance,
    params: AlgorithmParams,
    verbose: bool = False,
) -> RunResult:
    """
    Main 3DAPANSGA-II algorithm (Fig. 2 flow chart).

    Returns the best solution found (minimum TOC from Pareto front).
    """
    start_time = time.time()
    notes = []

    if params.random_seed is not None:
        random.seed(params.random_seed)

    # Apply parameters to instance
    instance.vehicle_capacity = params.vehicle_capacity
    instance.vehicle_speed = params.vehicle_speed
    instance.fuel_rate = params.fuel_rate
    instance.fuel_price = params.fuel_price
    instance.annual_maintenance = params.annual_maintenance
    instance.working_days = params.working_days
    instance.epsilon = params.epsilon
    instance.omega = params.omega
    instance.delta = params.delta
    instance.chi = params.chi
    instance.gamma = params.gamma

    # ── Stage 1: 3D AP Clustering ──────────────────────────────────────────
    if verbose:
        print("  [Stage 1] Running 3D AP Clustering...")

    clustering = APClustering3D(
        instance=instance,
        damping=params.ap_damping,
        max_iter=params.ap_max_iter,
        spatial_coeff=params.s_coeff,
        temporal_coeff=params.t_coeff,
    )
    cluster_assignment = clustering.fit()  # customer_id -> depot_id

    # Only assign static customers in initial routing
    static_ids = [
        n.node_id for n in instance.static_customers
    ]
    dynamic_ids = [
        n.node_id for n in instance.dynamic_customers
    ]

    # Build cluster map for static customers only
    static_cluster_map = {
        cid: cluster_assignment.get(cid, instance.all_depots[0].node_id)
        for cid in static_ids
    }

    if verbose:
        clusters = cluster_by_depot_type(static_cluster_map, instance)
        for depot_id, customers in clusters.items():
            print(f"    Depot {depot_id}: {len(customers)} customers")

    # ── Stage 2: ANSGA-II ──────────────────────────────────────────────────
    vehicle_proto = Vehicle(
        vehicle_id=1,
        capacity=params.vehicle_capacity,
        speed=params.vehicle_speed,
        fuel_rate=params.fuel_rate,
        fuel_price=params.fuel_price,
        annual_maintenance=params.annual_maintenance,
    )

    r_c = min(params.r_c_max, len(static_ids))

    if verbose:
        print(f"  [Stage 2] ANSGA-II: {params.n_ind} individuals × {params.m_gen} generations")

    # Initialize parent population P (Table 7)
    population = initialize_population(
        n_ind=params.n_ind,
        cluster_map=static_cluster_map,
        static_customers=static_ids,
        instance=instance,
        vehicle_proto=vehicle_proto,
    )

    # Evaluate initial population
    for chrom in population:
        if chrom.solution is None:
            chrom.solution = decode_chromosome(chrom, instance, vehicle_proto)

    gbest: Optional[Chromosome] = None
    gbest_no_change = 0
    mp_current = params.mp
    pareto_archive: list[Chromosome] = []

    for gen in range(1, params.m_gen + 1):
        mp_current = adaptive_mutation_rate(params.mp, gen, params.m_gen)

        # Compute fitness for selection
        toc_vals = [c.solution.TOC for c in population if c.solution]
        nv_vals = [c.solution.NV for c in population if c.solution]
        toc_max = max(toc_vals) if toc_vals else 1.0
        nv_max = max(nv_vals) if nv_vals else 1.0

        # Nondominated sort for ranking
        fronts = fast_nondominated_sort(population)
        for front in fronts:
            crowding_distance_assignment(front, population)

        # Generate offspring population F
        offspring = []
        while len(offspring) < params.n_ind:
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            # Crossover
            if random.random() < params.cp:
                o1, o2 = pmx_crossover(p1, p2)
            else:
                o1, o2 = p1.copy(), p2.copy()

            # Mutation
            o1 = mutate(o1, mp_current)
            o2 = mutate(o2, mp_current)

            # Decode and evaluate
            o1.solution = decode_chromosome(o1, instance, vehicle_proto)
            o2.solution = decode_chromosome(o2, instance, vehicle_proto)
            offspring.extend([o1, o2])

        offspring = offspring[:params.n_ind]

        # Merge P and F → N (2*N_IND individuals)
        combined = population + offspring

        # Nondominated sort on combined
        combined_fronts = fast_nondominated_sort(combined)
        for front in combined_fronts:
            crowding_distance_assignment(front, combined)

        # Select top N_IND for new population (Table 10)
        new_population = []
        for front in combined_fronts:
            if len(new_population) + len(front) <= params.n_ind:
                new_population.extend([combined[i] for i in front])
            else:
                # Fill remaining slots by crowding distance (Table 10, lines 15-17)
                remaining = params.n_ind - len(new_population)
                sorted_front = sorted(
                    front,
                    key=lambda i: combined[i].crowding_dist,
                    reverse=True,
                )
                new_population.extend([combined[i] for i in sorted_front[:remaining]])
                break

        population = new_population

        # Update gbest (minimum TOC in current population)
        current_best = min(
            population,
            key=lambda c: c.solution.TOC if c.solution else float('inf')
        )

        if current_best.solution is not None:
            if gbest is None or gbest.solution is None:
                gbest = current_best.copy()
                gbest_no_change = 0
            elif current_best.solution.TOC < gbest.solution.TOC:
                gbest = current_best.copy()
                gbest_no_change = 0
            else:
                gbest_no_change += 1
        else:
            gbest_no_change += 1

        # Local search trigger (Table 9, line 1: if gbest hasn't changed in R_Lg iterations)
        if gbest_no_change >= params.r_lg and gbest is not None:
            improved = local_search(gbest, instance, vehicle_proto, r_c)
            if (improved.solution and gbest.solution and
                    improved.solution.TOC < gbest.solution.TOC):
                gbest = improved
                gbest_no_change = 0
                # Replace worst in population with gbest
                worst_idx = max(
                    range(len(population)),
                    key=lambda i: population[i].solution.TOC if population[i].solution else 0
                )
                population[worst_idx] = gbest.copy()

        # Update Pareto archive
        pareto_archive = _update_pareto_archive(pareto_archive + [gbest] if gbest else pareto_archive)

        if verbose and gen % 25 == 0:
            best_toc = gbest.solution.TOC if gbest and gbest.solution else float('inf')
            best_nv = gbest.solution.NV if gbest and gbest.solution else 0
            print(f"    Gen {gen:4d}: TOC={best_toc:.1f}, NV={best_nv}")

    # ── Apply Dynamic Insertion Strategy ──────────────────────────────────
    if dynamic_ids and gbest and gbest.solution:
        if verbose:
            print(f"  [Stage 3] Inserting {len(dynamic_ids)} dynamic demands...")
        # Sort by known_time (process in order of arrival)
        dynamic_sorted = sorted(
            dynamic_ids,
            key=lambda k: instance.nodes[k].known_time
        )
        final_solution = insert_dynamic_demands(
            gbest.solution,
            dynamic_sorted,
            instance,
        )
    else:
        final_solution = gbest.solution if gbest else Solution()

    elapsed = time.time() - start_time

    best_toc = final_solution.TOC if final_solution else float('inf')
    best_nv = final_solution.NV if final_solution else 0

    # Collect pareto solutions
    pareto_solutions = [c.solution for c in pareto_archive if c.solution]

    return RunResult(
        best_toc=best_toc,
        best_nv=best_nv,
        computation_time=elapsed,
        pareto_front=pareto_solutions,
        notes=notes,
    )


def _update_pareto_archive(archive: list[Chromosome]) -> list[Chromosome]:
    """Maintain non-dominated archive."""
    result = []
    for chrom in archive:
        if chrom.solution is None:
            continue
        dominated = False
        for other in archive:
            if other is chrom or other.solution is None:
                continue
            if dominates(other.solution, chrom.solution):
                dominated = True
                break
        if not dominated:
            result.append(chrom)

    # Remove duplicates by TOC
    seen = set()
    unique = []
    for c in result:
        key = (round(c.solution.TOC, 2), c.solution.NV)
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique
