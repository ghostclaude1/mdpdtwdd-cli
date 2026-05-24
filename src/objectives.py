"""
Objective functions and constraint checker for MDPDTWDD.

Equations follow paper notation exactly:
- Eq.15: min TOC = TC + PC + MC + IC + FC
- Eq.16: min NV = Σ_v Σ_i∈F Σ_j∈C x_ij^v
- Eq.17: TC = Σ_v Σ_i Σ_j (f_v * p_v * x_ij^v * d_ij)
- Eq.18: PC = Σ_v Σ_i∈C (ε*max{l_i-A_vi,0} + ω*max{A_vi-r_i,0})
- Eq.19: MC = Σ_v Σ_i∈F Σ_j∈C (M_v * x_ij^v / T)
- Eq.20: IC = Σ_i∈D Σ_f∈F Σ_v (y_if^v * P_i * γ)
- Eq.21: FC = Σ_f β_f + δ*Σ_i∈R Σ_f Σ_v (y_if^v * Q_i) + χ*Σ_i∈S∪D Σ_f Σ_v (y_if^v * P_i)
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from src.data_model import ProblemInstance, Route, Solution, NodeType


@dataclass
class RouteEvaluation:
    """Detailed evaluation of a single route."""
    route_idx: int
    vehicle_id: int
    arrival_times: dict[int, float]   # node_id -> arrival time A_vi
    is_feasible: bool = True
    infeasibility_reason: str = ""

    # Cost components for this route
    TC: float = 0.0
    PC: float = 0.0
    MC: float = 0.0
    IC: float = 0.0


def evaluate_route(
    route: Route,
    instance: ProblemInstance,
    is_dynamic: bool = False,
) -> RouteEvaluation:
    """
    Evaluate a single route: compute arrival times and costs.

    Travel time: t_ij = d_ij / α_v (Eq. text)
    Arrival time: A_vi = departure from previous node + travel time
    Vehicle departs from origin depot at time B_v (earliest = depot's l_f).

    NOTE: Paper uses B_v = time vehicle leaves depot. Waiting at customer is
    allowed (vehicle arrives early and waits until l_i). This is standard VRP
    with soft time windows (penalty for early + late, not hard constraint).
    Constraints 34-35 suggest soft time windows (penalty-based).
    """
    v = route.vehicle
    result = RouteEvaluation(
        route_idx=0,
        vehicle_id=v.vehicle_id,
        arrival_times={},
    )

    if not route.nodes:
        return result

    # Start from origin depot
    origin = instance.nodes[route.origin_depot_id]

    # Compute optimal departure time B_v (Constraints 31-33):
    #   B_v = max(depot.l_i, l_first_customer - t(depot→first_customer))
    # Departing at t=0 always causes massive early penalty because customers
    # have l_i in range [80, 600+] while travel times are only 0.5–5 units.
    first_nid = route.nodes[0]
    first_node = instance.nodes[first_nid]
    t_to_first = instance.travel_time(route.origin_depot_id, first_nid)
    B_v = max(origin.l_i, first_node.l_i - t_to_first)

    current_time = B_v
    result.arrival_times[route.origin_depot_id] = B_v

    prev_id = route.origin_depot_id
    current_load = 0.0

    # Track delivery load at start (loaded at depot)
    # For delivery depot: load delivery goods for R customers on this route
    # For pickup depot: start with empty vehicle (picks up goods from S customers)
    if origin.is_delivery_depot():
        for nid in route.nodes:
            n = instance.nodes[nid]
            if n.is_static_delivery():
                current_load += n.Q_i
    # else: pickup route starts empty, accumulates pickup goods

    # Check initial capacity
    if current_load > v.capacity:
        result.is_feasible = False
        result.infeasibility_reason = f"Initial load {current_load} exceeds capacity {v.capacity}"

    # Traverse route
    for nid in route.nodes:
        node = instance.nodes[nid]
        travel_t = instance.travel_time(prev_id, nid)
        arrival = current_time + travel_t
        result.arrival_times[nid] = arrival

        # Travel cost component for this leg
        dist = instance.dist(prev_id, nid)
        result.TC += v.fuel_rate * v.fuel_price * dist  # Eq.17

        # Penalty cost (Eq.18): soft time window — penalize both early AND late arrival.
        # A_vi = service start = max(actual_arrival, l_i) (vehicle waits if arrives early).
        # early_violation = max(l_i - A_vi, 0): A_vi = max(arr,l_i) >= l_i → always 0 via wait.
        # BUT paper explicitly writes epsilon*max(l_i - A_vi, 0), so A_vi = raw arrival time.
        # Keep both penalties as stated in Eq.18.
        early_violation = max(node.l_i - arrival, 0.0)
        late_violation = max(arrival - node.r_i, 0.0)
        result.PC += instance.epsilon * early_violation + instance.omega * late_violation

        # Service: if arrive early, wait until window opens
        service_start = max(arrival, node.l_i)
        current_time = service_start  # No service time given in paper (assumed instantaneous)

        # Update load
        if node.is_static_delivery():
            current_load -= node.Q_i
        elif node.is_static_pickup() or node.is_dynamic():
            current_load += node.P_i

        # Capacity check
        if current_load < -1e-6 or current_load > v.capacity + 1e-6:
            result.is_feasible = False
            result.infeasibility_reason = f"Capacity violated at node {nid}: load={current_load}"

        prev_id = nid

    # Return to end depot (if specified)
    if route.end_depot_id is not None:
        end_depot = instance.nodes[route.end_depot_id]
        travel_t = instance.travel_time(prev_id, route.end_depot_id)
        arrival = current_time + travel_t
        result.arrival_times[route.end_depot_id] = arrival

        dist = instance.dist(prev_id, route.end_depot_id)
        result.TC += v.fuel_rate * v.fuel_price * dist

        # Check depot time window (Constraint 36)
        if arrival > end_depot.r_i + 1e-6:
            result.is_feasible = False
            result.infeasibility_reason = (
                f"Depot {route.end_depot_id} time window violated: "
                f"arrival={arrival:.2f} > r_f={end_depot.r_i}"
            )

    # Maintenance cost (Eq.19): M_v / T per vehicle-route
    # NOTE-06: MC = M_v * x_ij^v / T where i∈F, j∈C.
    # This counts one depot->first_customer arc = one vehicle used.
    result.MC = v.annual_maintenance / instance.working_days

    return result


def evaluate_solution(
    solution: Solution,
    instance: ProblemInstance,
) -> Solution:
    """
    Evaluate a complete solution: compute all objective values.
    Updates solution in place and returns it.
    """
    total_TC = 0.0
    total_PC = 0.0
    total_MC = 0.0
    total_IC = 0.0
    total_FC = 0.0
    nv = 0

    # Fixed cost (Eq.21): FC = Σ_f β_f + δ·Σ_{i∈R} Q_i + χ·Σ_{i∈S∪D} P_i
    # This is a CONSTANT for a given instance — independent of routes.
    # NOTE-07: β_f not given in paper, using 0.0
    for depot in instance.all_depots:
        total_FC += instance.depot_fixed_cost
    for node in instance.nodes.values():
        if node.is_static_delivery():
            total_FC += instance.delta * node.Q_i
        elif node.is_static_pickup():
            total_FC += instance.chi * node.P_i
        elif node.is_dynamic():
            total_FC += instance.chi * node.P_i   # dynamic pickup also uses χ for FC

    # Evaluate each route
    for i, route in enumerate(solution.routes):
        if not route.nodes:
            continue

        nv += 1  # Each active route uses one vehicle

        eval_r = evaluate_route(route, instance)
        total_TC += eval_r.TC
        total_PC += eval_r.PC
        total_MC += eval_r.MC

        # Insertion cost for dynamic customers on this route (Eq.20): IC = Σ P_i * γ
        for nid in route.nodes:
            node = instance.nodes[nid]
            if node.is_dynamic():
                total_IC += instance.gamma * node.P_i

    solution.TC = total_TC
    solution.PC = total_PC
    solution.MC = total_MC
    solution.IC = total_IC
    solution.FC = total_FC
    solution.NV = nv
    solution.TOC = total_TC + total_PC + total_MC + total_IC + total_FC

    return solution


def compute_toc_gap(toc_algo: float, toc_cplex: float) -> float:
    """
    Compute TOC gap percentage as used in paper Tables 12/13.
    TOC gap = (toc_algo - toc_cplex) / toc_cplex * 100
    """
    if toc_cplex == 0:
        return 0.0
    return (toc_algo - toc_cplex) / toc_cplex * 100.0


def fitness(toc: float, nv: int, toc_max: float, nv_max: float) -> float:
    """
    Fitness function (Eq.54):
    fit = 1 / (TOC/TOC_max + NV/NV_max)

    Higher fitness = better solution (selected for crossover/mutation).
    """
    denominator = (toc / toc_max if toc_max > 0 else 0) + (nv / nv_max if nv_max > 0 else 0)
    if denominator == 0:
        return float('inf')
    return 1.0 / denominator


def dominates(sol_a: Solution, sol_b: Solution) -> bool:
    """
    Returns True if sol_a dominates sol_b in Pareto sense.
    sol_a dominates sol_b if:
    - sol_a is at least as good as sol_b on all objectives
    - sol_a is strictly better on at least one objective
    """
    not_worse = (sol_a.TOC <= sol_b.TOC) and (sol_a.NV <= sol_b.NV)
    strictly_better = (sol_a.TOC < sol_b.TOC) or (sol_a.NV < sol_b.NV)
    return not_worse and strictly_better
