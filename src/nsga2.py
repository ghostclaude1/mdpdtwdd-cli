"""
Adaptive NSGA-II (ANSGA-II) for MDPDTWDD.

Implements Section 4.3 of Wang et al. (2025):
- Population initialization (Table 7)
- PMX crossover (Section 4.3.1, Fig. 4)
- Adaptive mutation (Eq.55, Table 8)
- Nondominated + crowding distance sorting (Table 10)
- Local search: destroy-repair (Eq.56, Table 9)
- Pareto front management (Section 4.3.3)

NOTE-03: Parameter "gp=0.90" from Table 15 is unresolved.
         Implemented as tournament selection probability.
NOTE-09: Chromosome length L = number of static customers (R∪S).
         Dynamic customers are handled by insertion strategy (Section 4.4).
"""
from __future__ import annotations
import random
import copy
import math
from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from src.data_model import ProblemInstance, Solution, Route, Vehicle, NodeType
from src.objectives import evaluate_solution, fitness, dominates


@dataclass
class Chromosome:
    """
    A chromosome encodes a permutation of static customer IDs.
    Genes represent the visit order within and across clusters.

    Cluster information: customer_id -> depot_id
    The chromosome is a permutation that will be decoded into routes
    by assigning consecutive customers in the permutation to their clusters.
    """
    genes: list[int]                         # Ordered customer IDs (L genes)
    cluster_map: dict[int, int]              # customer_id -> depot_id
    solution: Optional[Solution] = None      # Decoded solution (computed lazily)
    fitness_val: float = 0.0
    rank: int = 0                            # Nondomination rank
    crowding_dist: float = 0.0

    def copy(self) -> Chromosome:
        import copy as _copy
        c = Chromosome(
            genes=self.genes.copy(),
            cluster_map=self.cluster_map.copy(),
        )
        c.solution = _copy.deepcopy(self.solution)
        c.fitness_val = self.fitness_val
        c.rank = self.rank
        c.crowding_dist = self.crowding_dist
        return c


def decode_chromosome(
    chrom: Chromosome,
    instance: ProblemInstance,
    vehicle_proto: Vehicle,
) -> Solution:
    """
    Decode a chromosome into a Solution.

    Decoding strategy:
    1. Group genes by cluster (depot assignment)
    2. Create one route per cluster group
    3. Route starts from assigned depot, visits customers in gene order
    4. Route ends at appropriate depot:
       - If route contains only delivery customers → closed at DD
       - If route contains only pickup customers → closed at PD
       - If route contains both → open route: start at DD, end at PD (Section 3.1)

    NOTE-09: Chromosome encodes only static customers. Dynamic customers added
    via insertion strategy.
    """
    routes = []
    vehicle_id = 1

    # Group customers by their assigned depot
    depot_groups: dict[int, list[int]] = {}
    for cid in chrom.genes:
        depot_id = chrom.cluster_map.get(cid)
        if depot_id is None:
            continue
        if depot_id not in depot_groups:
            depot_groups[depot_id] = []
        depot_groups[depot_id].append(cid)

    for depot_id, customers in depot_groups.items():
        if not customers:
            continue

        depot_node = instance.nodes[depot_id]

        # ── Capacity-aware route splitting ──────────────────────────────
        # Split customers into sub-routes that respect vehicle capacity.
        # This is the standard VRP route construction needed before NSGA-II.
        sub_routes = _split_into_routes(customers, depot_id, depot_node, instance)

        for sub_nodes, origin_id, end_id in sub_routes:
            if not sub_nodes:
                continue
            vehicle = Vehicle(
                vehicle_id=vehicle_id,
                capacity=instance.vehicle_capacity,
                speed=instance.vehicle_speed,
                fuel_rate=instance.fuel_rate,
                fuel_price=instance.fuel_price,
                annual_maintenance=instance.annual_maintenance,
            )
            vehicle_id += 1
            route = Route(
                vehicle=vehicle,
                origin_depot_id=origin_id,
                nodes=sub_nodes,
                end_depot_id=end_id,
            )
            routes.append(route)

    solution = Solution(routes=routes)
    evaluate_solution(solution, instance)
    return solution


def _split_into_routes(
    customers: list[int],
    depot_id: int,
    depot_node,
    instance: ProblemInstance,
) -> list[tuple[list[int], int, int]]:
    """
    Split a list of customers into capacity-feasible sub-routes.
    Each sub-route: (customer_list, origin_depot_id, end_depot_id)

    Strategy: greedy sequential packing respecting vehicle capacity.
    Within each sub-route, sort customers by time-window left bound (l_i)
    to minimize penalty costs from out-of-order arrivals.
    For mixed routes (delivery+pickup), open route: DD → PD.
    """
    capacity = instance.vehicle_capacity
    result = []
    current_route = []
    current_load = 0.0

    # Determine open/closed based on depot type
    pds = instance.pickup_depots
    dds = instance.delivery_depots

    for cid in customers:
        node = instance.nodes[cid]
        demand = node.Q_i if node.is_static_delivery() else node.P_i

        if current_load + demand > capacity + 1e-6:
            # Start new route
            if current_route:
                origin_id, end_id = _get_route_endpoints(
                    current_route, depot_id, depot_node, instance, dds, pds
                )
                result.append((current_route, origin_id, end_id))
            current_route = [cid]
            current_load = demand
        else:
            current_route.append(cid)
            current_load += demand

    if current_route:
        origin_id, end_id = _get_route_endpoints(
            current_route, depot_id, depot_node, instance, dds, pds
        )
        result.append((current_route, origin_id, end_id))

    return result if result else [([cid for cid in customers], depot_id, depot_id)]


def _get_route_endpoints(
    route_nodes: list[int],
    depot_id: int,
    depot_node,
    instance: ProblemInstance,
    dds: list,
    pds: list,
) -> tuple[int, int]:
    """Determine origin and end depot for a route based on content."""
    has_delivery = any(instance.nodes[n].is_static_delivery() for n in route_nodes)
    has_pickup = any(
        instance.nodes[n].is_static_pickup() or instance.nodes[n].is_dynamic()
        for n in route_nodes
    )

    if has_delivery and has_pickup:
        # Open route: DD → PD (Section 3.1)
        if depot_node.is_delivery_depot():
            origin = depot_id
            end = min(pds, key=lambda pd: instance.dist(depot_id, pd.node_id)).node_id if pds else depot_id
        else:
            origin = min(dds, key=lambda dd: instance.dist(depot_id, dd.node_id)).node_id if dds else depot_id
            end = depot_id
    else:
        origin = depot_id
        end = depot_id

    return origin, end


def initialize_population(
    n_ind: int,
    cluster_map: dict[int, int],
    static_customers: list[int],
    instance: ProblemInstance,
    vehicle_proto: Vehicle,
) -> list[Chromosome]:
    """
    Table 7 pseudocode: Initialize population.
    Randomize each chromosome based on clustering results.
    """
    population = []
    for _ in range(n_ind):
        genes = static_customers.copy()
        random.shuffle(genes)
        chrom = Chromosome(genes=genes, cluster_map=cluster_map)
        chrom.solution = decode_chromosome(chrom, instance, vehicle_proto)
        population.append(chrom)
    return population


def pmx_crossover(parent1: Chromosome, parent2: Chromosome) -> tuple[Chromosome, Chromosome]:
    """
    Partial Mapped Crossover (PMX) as described in Section 4.3.1 and Fig. 4.

    Steps:
    1. Select random crossover segment [L_p1, L_p2]
    2. Swap segment between parents
    3. Fix duplicates using mapping relationship
    4. Update chromosomes to produce offspring
    """
    L = len(parent1.genes)
    if L < 2:
        return parent1.copy(), parent2.copy()

    # Step 1: Select random crossover points
    L_p1 = random.randint(0, L - 2)
    L_p2 = random.randint(L_p1 + 1, L - 1)

    o1_genes = parent1.genes.copy()
    o2_genes = parent2.genes.copy()

    # Extract segments
    seg1 = parent1.genes[L_p1:L_p2 + 1]
    seg2 = parent2.genes[L_p1:L_p2 + 1]

    # Step 2: Swap segments
    o1_genes[L_p1:L_p2 + 1] = seg2
    o2_genes[L_p1:L_p2 + 1] = seg1

    # Step 3: Build mapping
    mapping_1_to_2 = dict(zip(seg1, seg2))
    mapping_2_to_1 = dict(zip(seg2, seg1))

    # Step 4: Fix duplicates outside segment
    def fix_genes(genes: list[int], segment: list[int], mapping: dict) -> list[int]:
        """Resolve duplicate genes using the mapping relation (transitive)."""
        seg_set = set(segment)
        result = genes.copy()
        for idx in range(len(result)):
            if idx >= len(genes):
                break
            # Check if outside segment
            is_in_segment = False
            # Compute actual segment range for this offspring
            # We already swapped: segment positions L_p1..L_p2 have new segment
            # Fix positions OUTSIDE the segment
            if not (L_p1 <= idx <= L_p2):
                val = result[idx]
                # Follow mapping chain to resolve duplicate
                visited = set()
                while val in seg_set and val not in visited:
                    visited.add(val)
                    val = mapping.get(val, val)
                result[idx] = val
        return result

    # FIX: o1 has seg2 inserted → duplicates are values in seg2 → resolve via mapping_2_to_1
    # FIX: o2 has seg1 inserted → duplicates are values in seg1 → resolve via mapping_1_to_2
    o1_genes = fix_genes(o1_genes, seg2, mapping_2_to_1)
    o2_genes = fix_genes(o2_genes, seg1, mapping_1_to_2)

    off1 = Chromosome(genes=o1_genes, cluster_map=parent1.cluster_map)
    off2 = Chromosome(genes=o2_genes, cluster_map=parent2.cluster_map)
    return off1, off2


def mutate(chromosome: Chromosome, mp: float) -> Chromosome:
    """
    Table 8 pseudocode: Mutation by gene swap.
    For each chromosome: with probability mp, swap two random positions.

    NOTE: mp updated adaptively per Eq.55.
    """
    chrom = chromosome.copy()
    L = len(chrom.genes)
    if L < 2:
        return chrom

    c_mp = random.random()
    if c_mp < mp:
        L_p1 = random.randint(0, L - 1)
        L_p2 = random.randint(0, L - 1)
        while L_p2 == L_p1:
            L_p2 = random.randint(0, L - 1)
        # Swap genes at positions L_p1 and L_p2
        chrom.genes[L_p1], chrom.genes[L_p2] = chrom.genes[L_p2], chrom.genes[L_p1]
    return chrom


def adaptive_mutation_rate(mp_init: float, gen: int, m_gen: int) -> float:
    """
    Eq.55: mp = mp * (1 - gen/M_gen)
    Mutation probability decays over generations.
    """
    return mp_init * (1 - gen / m_gen)


def fast_nondominated_sort(population: list[Chromosome]) -> list[list[int]]:
    """
    Fast nondominated sort (NSGA-II Algorithm 1).
    Returns list of fronts, each front is list of indices into population.
    """
    n = len(population)
    domination_count = [0] * n       # Number of solutions that dominate i
    dominated_by = [[] for _ in range(n)]  # Solutions dominated by i
    fronts = [[]]

    for i in range(n):
        for j in range(i + 1, n):
            sol_i = population[i].solution
            sol_j = population[j].solution
            if sol_i is None or sol_j is None:
                continue
            if dominates(sol_i, sol_j):
                dominated_by[i].append(j)
                domination_count[j] += 1
            elif dominates(sol_j, sol_i):
                dominated_by[j].append(i)
                domination_count[i] += 1

    for i in range(n):
        if domination_count[i] == 0:
            population[i].rank = 0
            fronts[0].append(i)

    front_idx = 0
    while fronts[front_idx]:
        next_front = []
        for i in fronts[front_idx]:
            for j in dominated_by[i]:
                domination_count[j] -= 1
                if domination_count[j] == 0:
                    population[j].rank = front_idx + 1
                    next_front.append(j)
        front_idx += 1
        fronts.append(next_front)

    return fronts[:-1]  # Remove last empty front


def crowding_distance_assignment(
    front: list[int],
    population: list[Chromosome],
) -> None:
    """
    Assign crowding distances to individuals in a front.
    Uses TOC and NV as the two objectives.
    """
    n = len(front)
    if n <= 2:
        for i in front:
            population[i].crowding_dist = float('inf')
        return

    for i in front:
        population[i].crowding_dist = 0.0

    objectives = ['TOC', 'NV']
    for obj in objectives:
        # Sort by objective
        sorted_front = sorted(
            front,
            key=lambda i: getattr(population[i].solution, obj, float('inf'))
        )

        population[sorted_front[0]].crowding_dist = float('inf')
        population[sorted_front[-1]].crowding_dist = float('inf')

        obj_min = getattr(population[sorted_front[0]].solution, obj, 0)
        obj_max = getattr(population[sorted_front[-1]].solution, obj, 0)
        obj_range = obj_max - obj_min if obj_max != obj_min else 1.0

        for k in range(1, n - 1):
            prev_val = getattr(population[sorted_front[k - 1]].solution, obj, 0)
            next_val = getattr(population[sorted_front[k + 1]].solution, obj, 0)
            population[sorted_front[k]].crowding_dist += (next_val - prev_val) / obj_range


def tournament_selection(
    population: list[Chromosome],
    tournament_size: int = 2,
) -> Chromosome:
    """
    Tournament selection based on rank and crowding distance.
    Lower rank preferred; for equal rank, higher crowding distance preferred.
    """
    candidates = random.sample(range(len(population)), min(tournament_size, len(population)))
    best = candidates[0]
    for c in candidates[1:]:
        if (population[c].rank < population[best].rank or
                (population[c].rank == population[best].rank and
                 population[c].crowding_dist > population[best].crowding_dist)):
            best = c
    return population[best]


def compute_similarity(i: int, j: int, route_i: set[int], instance: ProblemInstance) -> float:
    """
    Eq.56: s_ij = 1 / (x_ij^v + d_ij/max{d_ij})
    where x_ij^v = 1 if i,j are on same route, else 0.

    x_ij: 1 if i and j are both in route_i (same route before removal), else 0
    d_ij: distance between i and j
    max{d_ij}: maximum distance in instance (normalization)
    """
    x_ij = 1.0 if (i in route_i and j in route_i) else 0.0
    d_ij = instance.dist(i, j)

    # max distance across all pairs
    all_dists = list(instance.dist_matrix.values())
    max_d = max(all_dists) if all_dists else 1.0

    denominator = x_ij + (d_ij / max_d if max_d > 0 else 0)
    if denominator == 0:
        return float('inf')
    return 1.0 / denominator


def local_search(
    chromosome: Chromosome,
    instance: ProblemInstance,
    vehicle_proto: Vehicle,
    r_c: int,
) -> Chromosome:
    """
    Table 9 pseudocode: Destroy-repair local search.

    1. Select random customer as seed
    2. Compute similarity to other customers (Eq.56)
    3. Remove R_c most similar customers
    4. Reinsert them in best positions
    5. Accept if improved
    """
    if len(chromosome.genes) <= 1:
        return chromosome

    chrom = chromosome.copy()
    if chrom.solution is None:
        chrom.solution = decode_chromosome(chrom, instance, vehicle_proto)

    # Build route membership map for similarity computation
    route_membership: dict[int, set[int]] = {}
    for route in chrom.solution.routes:
        route_set = set(route.nodes)
        for nid in route.nodes:
            route_membership[nid] = route_set

    # Step 1: Select random seed customer
    seed_idx = random.randint(0, len(chrom.genes) - 1)
    seed_id = chrom.genes[seed_idx]
    seed_route = route_membership.get(seed_id, set())

    # Step 2: Compute similarities
    sims = {}
    for cid in chrom.genes:
        if cid != seed_id:
            sims[cid] = compute_similarity(seed_id, cid, seed_route, instance)

    # Step 3: Select R_c most similar customers (higher similarity = more similar)
    r_c_actual = min(r_c, len(chrom.genes) - 1)
    remove_ids = set(
        sorted(sims.keys(), key=lambda x: sims[x], reverse=True)[:r_c_actual]
    )
    remove_ids.add(seed_id)

    # Step 4: Remove from chromosome
    remaining = [g for g in chrom.genes if g not in remove_ids]
    removed = list(remove_ids)

    # Reinsert removed customers in best positions (greedy)
    random.shuffle(removed)
    new_genes = remaining.copy()
    for cid in removed:
        # Find best insertion position
        best_pos = 0
        best_toc = float('inf')
        for pos in range(len(new_genes) + 1):
            trial_genes = new_genes[:pos] + [cid] + new_genes[pos:]
            trial_chrom = Chromosome(genes=trial_genes, cluster_map=chrom.cluster_map)
            trial_sol = decode_chromosome(trial_chrom, instance, vehicle_proto)
            if trial_sol.TOC < best_toc:
                best_toc = trial_sol.TOC
                best_pos = pos
        new_genes.insert(best_pos, cid)

    new_chrom = Chromosome(genes=new_genes, cluster_map=chrom.cluster_map)
    new_chrom.solution = decode_chromosome(new_chrom, instance, vehicle_proto)

    # Step 5: Accept if improved (by fitness)
    toc_old = chrom.solution.TOC if chrom.solution else float('inf')
    nv_old = chrom.solution.NV if chrom.solution else 0
    toc_new = new_chrom.solution.TOC if new_chrom.solution else float('inf')
    nv_new = new_chrom.solution.NV if new_chrom.solution else 0

    if toc_new < toc_old or nv_new < nv_old:
        return new_chrom
    return chrom
