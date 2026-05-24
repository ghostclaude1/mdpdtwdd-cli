"""
Objective functions for MDPDTWDD — performance-optimised version.

Eq.15: min TOC = TC + PC + MC + IC + FC
Eq.17: TC = Σ f_v·p_v·x_ij·d_ij
Eq.18: PC = Σ (ε·max{l_i-A_vi,0} + ω·max{A_vi-r_i,0})
Eq.19: MC = Σ M_v·x_ij^v / T   (1 per route)
Eq.20: IC = Σ_{i∈D} P_i·γ
Eq.21: FC = Σ β_f + δ·Σ_{i∈R} Q_i + χ·Σ_{i∈S∪D} P_i

PERFORMANCE CHANGES vs original:
- evaluate_route: all loops use precomputed numpy arrays via instance._idx,
  _dist_arr, _time_arr, _l_arr, _r_arr, is_delivery, is_pickup_node.
  Eliminates per-iteration dict lookups and method calls in the inner loop.
- evaluate_solution: FC computed once and cached on instance._fc_const.
- dominates: inlined tuple comparison — no function call overhead.
- RouteEvaluation.arrival_times removed from hot path (only filled on demand).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from src.data_model import ProblemInstance, Route, Solution, NodeType


@dataclass
class RouteEvaluation:
    """Detailed evaluation of a single route."""
    route_idx: int
    vehicle_id: int
    arrival_times: dict[int, float] = field(default_factory=dict)
    is_feasible: bool = True
    infeasibility_reason: str = ""

    TC: float = 0.0
    PC: float = 0.0
    MC: float = 0.0
    IC: float = 0.0


def evaluate_route(
    route: Route,
    instance: ProblemInstance,
    is_dynamic: bool = False,
    fill_arrivals: bool = True,
) -> RouteEvaluation:
    """
    Evaluate a single route.

    Hot-path uses precomputed numpy arrays when available (after
    instance.build_distance_matrix()).  Falls back to dict lookup otherwise.

    B_v selection:
      lower = max(depot.l_i,  l_first - t(depot→first))
      upper = min over all nodes of (r_i - cum_travel_i)   [backward pass]
      B_v   = clamp(upper, lower, depot.r_i)
    """
    v = route.vehicle
    nodes_seq = route.nodes
    if not nodes_seq:
        return RouteEvaluation(route_idx=0, vehicle_id=v.vehicle_id)

    result = RouteEvaluation(route_idx=0, vehicle_id=v.vehicle_id)

    # ---- choose fast or fallback path -------------------------------- #
    fast = instance._dist_arr is not None
    if fast:
        idx = instance._idx
        dist_arr = instance._dist_arr
        time_arr = instance._time_arr
        l_arr    = instance._l_arr
        r_arr    = instance._r_arr
        is_del   = instance.is_delivery
        is_pku   = instance.is_pickup_node
        is_dd    = instance.is_dd_arr

        origin_idx = idx[route.origin_depot_id]
        first_idx  = idx[nodes_seq[0]]

        # B_v lower
        l_origin = l_arr[route.origin_depot_id]
        r_origin = r_arr[route.origin_depot_id]
        B_v_lower = max(l_origin, l_arr[nodes_seq[0]] - time_arr[origin_idx, first_idx])

        # B_v upper — backward pass (fast)
        B_v_upper = r_origin
        prev_idx  = origin_idx
        cum_t     = 0.0
        for nid in nodes_seq:
            nidx   = idx[nid]
            cum_t += time_arr[prev_idx, nidx]
            r_n    = r_arr[nid]
            upper_n = r_n - cum_t
            if upper_n < B_v_upper:
                B_v_upper = upper_n
            prev_idx = nidx

        B_v = B_v_lower if B_v_lower > B_v_upper else (
              B_v_upper if B_v_upper < r_origin else r_origin)
        B_v = max(B_v, B_v_lower)   # hard lower bound

        # initial delivery load
        current_load = 0.0
        if is_dd[route.origin_depot_id]:
            for nid in nodes_seq:
                if is_del[nid]:
                    current_load += instance._demand_arr[nid]

        if current_load > v.capacity:
            result.is_feasible = False
            result.infeasibility_reason = f"Initial load {current_load} exceeds capacity {v.capacity}"

        # precomputed scalars
        fcp     = v.fuel_cost_per_dist   # f_v * p_v
        epsilon = instance.epsilon
        omega   = instance.omega
        cap     = v.capacity

        t        = B_v
        prev_nid = route.origin_depot_id
        prev_idx = origin_idx
        TC = 0.0
        PC = 0.0

        if fill_arrivals:
            result.arrival_times[route.origin_depot_id] = B_v

        for nid in nodes_seq:
            nidx    = idx[nid]
            tt      = time_arr[prev_idx, nidx]
            d       = dist_arr[prev_idx, nidx]
            arrival = t + tt
            TC     += fcp * d

            l_n = l_arr[nid]
            r_n = r_arr[nid]
            early = l_n - arrival
            late  = arrival - r_n
            if early > 0.0:
                PC += epsilon * early
            elif late > 0.0:
                PC += omega * late

            # service start: wait if early
            t = arrival if arrival >= l_n else l_n

            # load update
            if is_del[nid]:
                current_load -= instance._demand_arr[nid]
            elif is_pku[nid]:
                current_load += instance._demand_arr[nid]

            if current_load < -1e-6 or current_load > cap + 1e-6:
                result.is_feasible = False
                result.infeasibility_reason = f"Capacity violated at node {nid}: load={current_load}"

            if fill_arrivals:
                result.arrival_times[nid] = arrival

            prev_nid = nid
            prev_idx = nidx

        # end depot leg
        if route.end_depot_id is not None:
            end_idx = idx[route.end_depot_id]
            tt  = time_arr[prev_idx, end_idx]
            d   = dist_arr[prev_idx, end_idx]
            arr = t + tt
            TC += fcp * d
            if fill_arrivals:
                result.arrival_times[route.end_depot_id] = arr
            if arr > r_arr[route.end_depot_id] + 1e-6:
                result.is_feasible = False
                result.infeasibility_reason = f"End depot TW violated: arrival={arr:.2f}"

        result.TC = TC
        result.PC = PC

    else:
        # ---- fallback path (no numpy) -------------------------------- #
        origin = instance.nodes[route.origin_depot_id]
        first_node = instance.nodes[nodes_seq[0]]
        t_to_first = instance.travel_time(route.origin_depot_id, nodes_seq[0])
        B_v_lower = max(origin.l_i, first_node.l_i - t_to_first)

        B_v_upper = origin.r_i
        prev_bv = route.origin_depot_id
        cum_t = 0.0
        for _nid in nodes_seq:
            cum_t += instance.travel_time(prev_bv, _nid)
            B_v_upper = min(B_v_upper, instance.nodes[_nid].r_i - cum_t)
            prev_bv = _nid
        B_v = max(B_v_lower, min(B_v_upper, origin.r_i))

        current_load = 0.0
        if origin.is_delivery_depot():
            for nid in nodes_seq:
                n = instance.nodes[nid]
                if n.is_static_delivery():
                    current_load += n.Q_i
        if current_load > v.capacity:
            result.is_feasible = False

        t = B_v
        prev_id = route.origin_depot_id
        if fill_arrivals:
            result.arrival_times[route.origin_depot_id] = B_v
        TC = PC = 0.0
        fcp = v.fuel_rate * v.fuel_price
        for nid in nodes_seq:
            node = instance.nodes[nid]
            travel_t = instance.travel_time(prev_id, nid)
            d = instance.dist(prev_id, nid)
            arrival = t + travel_t
            TC += fcp * d
            early = node.l_i - arrival
            late  = arrival - node.r_i
            if early > 0.0:
                PC += instance.epsilon * early
            elif late > 0.0:
                PC += instance.omega * late
            t = max(arrival, node.l_i)
            if node.is_static_delivery():
                current_load -= node.Q_i
            elif node.is_static_pickup() or node.is_dynamic():
                current_load += node.P_i
            if fill_arrivals:
                result.arrival_times[nid] = arrival
            prev_id = nid
        if route.end_depot_id is not None:
            end_node = instance.nodes[route.end_depot_id]
            tt = instance.travel_time(prev_id, route.end_depot_id)
            d  = instance.dist(prev_id, route.end_depot_id)
            arr = t + tt
            TC += fcp * d
            if fill_arrivals:
                result.arrival_times[route.end_depot_id] = arr
            if arr > end_node.r_i + 1e-6:
                result.is_feasible = False
        result.TC = TC
        result.PC = PC

    # maintenance (Eq.19): one arc depot→customer = one vehicle
    result.MC = v.annual_maintenance / instance.working_days
    return result


# Cache FC on the instance so evaluate_solution doesn't recompute every call
def _compute_fc_const(instance: ProblemInstance) -> float:
    fc = 0.0
    for _ in instance.all_depots:
        fc += instance.depot_fixed_cost
    for node in instance.nodes.values():
        if node.is_static_delivery():
            fc += instance.delta * node.Q_i
        elif node.is_static_pickup() or node.is_dynamic():
            fc += instance.chi * node.P_i
    return fc


def evaluate_solution(
    solution: Solution,
    instance: ProblemInstance,
) -> Solution:
    """
    Evaluate complete solution in-place.
    FC is a constant for a given instance — computed once and cached.
    """
    # lazy-cache FC constant
    if not hasattr(instance, '_fc_const') or instance._fc_const is None:
        instance._fc_const = _compute_fc_const(instance)

    total_TC = 0.0
    total_PC = 0.0
    total_MC = 0.0
    total_IC = 0.0
    nv = 0

    is_dyn = instance.is_dyn if instance.is_dyn is not None else None
    gamma  = instance.gamma
    demand = instance._demand_arr if instance._demand_arr is not None else None

    for route in solution.routes:
        if not route.nodes:
            continue
        nv += 1
        ev = evaluate_route(route, instance, fill_arrivals=False)
        total_TC += ev.TC
        total_PC += ev.PC
        total_MC += ev.MC

        # Insertion cost (Eq.20)
        if is_dyn is not None:
            for nid in route.nodes:
                if is_dyn[nid]:
                    total_IC += gamma * demand[nid]
        else:
            for nid in route.nodes:
                n = instance.nodes[nid]
                if n.is_dynamic():
                    total_IC += gamma * n.P_i

    solution.TC = total_TC
    solution.PC = total_PC
    solution.MC = total_MC
    solution.IC = total_IC
    solution.FC = instance._fc_const
    solution.NV = nv
    solution.TOC = total_TC + total_PC + total_MC + total_IC + instance._fc_const
    return solution


def dominates(sol_a: Solution, sol_b: Solution) -> bool:
    """
    Pareto dominance check — inlined for speed.
    sol_a dominates sol_b iff a ≤ b on both objectives and < on at least one.
    """
    toc_a, nv_a = sol_a.TOC, sol_a.NV
    toc_b, nv_b = sol_b.TOC, sol_b.NV
    return (toc_a <= toc_b and nv_a <= nv_b) and (toc_a < toc_b or nv_a < nv_b)


def compute_toc_gap(toc_algo: float, toc_cplex: float) -> float:
    if toc_cplex == 0:
        return 0.0
    return (toc_algo - toc_cplex) / toc_cplex * 100.0


def fitness(toc: float, nv: int, toc_max: float, nv_max: float) -> float:
    """Eq.54: fit = 1 / (TOC/TOC_max + NV/NV_max)"""
    d = (toc / toc_max if toc_max > 0 else 0) + (nv / nv_max if nv_max > 0 else 0)
    return 1.0 / d if d > 0 else float('inf')
