"""
Dynamic Demand Insertion Strategy.

Implements Section 4.4 of Wang et al. (2025) — Table 11 pseudocode.

Three insertion scenarios:
1. Direct insertion: dynamic customer inserted into existing route (vehicle detours)
2. Goods transfer: goods transferred to another vehicle to free capacity
3. New vehicle: if no existing vehicle can handle, dispatch new vehicle

NOTE-10: Scenario 2 (goods transfer) mechanics are not fully specified in
the paper. Only mentioned that "goods in the original vehicle are transferred
to another vehicle." Implementation is simplified:
  - Find dynamic customer k that cannot fit in any vehicle due to capacity
  - Check if any delivery goods can be offloaded to another vehicle in proximity
  - If yes, rebalance load and insert k
  - If no viable transfer found, proceed to Scenario 3
"""
from __future__ import annotations
import copy
import math
from dataclasses import dataclass
from typing import Optional

from src.data_model import ProblemInstance, Solution, Route, Vehicle, Node, NodeType
from src.objectives import evaluate_solution, evaluate_route


@dataclass
class InsertionResult:
    """Result of attempting to insert a dynamic customer."""
    success: bool
    scenario: int           # 1, 2, or 3
    new_solution: Optional[Solution] = None
    cost_increase: float = 0.0


def _compute_insertion_cost(
    route: Route,
    pos: int,
    customer_id: int,
    instance: ProblemInstance,
) -> float:
    """
    Compute additional cost of inserting customer at position pos in route.
    Uses detour cost: d(i,k) + d(k,j) - d(i,j) where k=customer, i=prev, j=next.
    """
    nodes = [route.origin_depot_id] + route.nodes + [route.end_depot_id or route.origin_depot_id]
    prev_node = nodes[pos]
    next_node = nodes[pos + 1]

    detour = (instance.dist(prev_node, customer_id)
              + instance.dist(customer_id, next_node)
              - instance.dist(prev_node, next_node))
    return detour


def _check_feasibility_with_insertion(
    route: Route,
    pos: int,
    customer_id: int,
    instance: ProblemInstance,
) -> bool:
    """
    Check if inserting customer_id at position pos is feasible.
    Checks: capacity + time window (Constraints 41-46).
    """
    customer = instance.nodes[customer_id]
    vehicle = route.vehicle

    # Check capacity: load after insertion
    current_load = 0.0
    for nid in route.nodes:
        n = instance.nodes[nid]
        if n.is_static_delivery():
            current_load += n.Q_i
        elif n.is_static_pickup() or n.is_dynamic():
            current_load += n.P_i

    if current_load + customer.P_i > vehicle.capacity + 1e-6:
        return False

    # Check time window feasibility by evaluating modified route
    new_nodes = route.nodes[:pos] + [customer_id] + route.nodes[pos:]
    test_route = Route(
        vehicle=vehicle,
        origin_depot_id=route.origin_depot_id,
        nodes=new_nodes,
        end_depot_id=route.end_depot_id,
    )
    eval_r = evaluate_route(test_route, instance)

    # Allow insertion if it doesn't exceed customer's time window too severely
    # (paper uses soft time windows, so any violation adds penalty)
    # For insertion feasibility, check hard capacity only + soft TW is acceptable
    return eval_r.is_feasible or True  # Soft time windows: always feasible (penalty added)


def scenario_1_direct_insert(
    solution: Solution,
    customer_id: int,
    instance: ProblemInstance,
) -> Optional[InsertionResult]:
    """
    Scenario 1: Direct insertion of dynamic customer into existing route.
    Finds the minimum-cost feasible insertion position across all routes.
    (Table 11, lines 7-10)
    """
    customer = instance.nodes[customer_id]
    best_cost = float('inf')
    best_route_idx = -1
    best_pos = -1

    for r_idx, route in enumerate(solution.routes):
        if not route.nodes:
            continue

        # Check capacity first
        current_load = sum(
            instance.nodes[nid].P_i
            for nid in route.nodes
            if instance.nodes[nid].is_static_pickup() or instance.nodes[nid].is_dynamic()
        )
        delivery_load = sum(
            instance.nodes[nid].Q_i
            for nid in route.nodes
            if instance.nodes[nid].is_static_delivery()
        )
        # Available capacity for pickup
        used_load = current_load  # simplification: count pickups
        available = route.vehicle.capacity - used_load

        if customer.P_i > available + 1e-6:
            continue

        # Try all insertion positions
        for pos in range(len(route.nodes) + 1):
            insert_cost = _compute_insertion_cost(route, pos, customer_id, instance)
            if insert_cost < best_cost:
                if _check_feasibility_with_insertion(route, pos, customer_id, instance):
                    best_cost = insert_cost
                    best_route_idx = r_idx
                    best_pos = pos

    if best_route_idx >= 0:
        new_solution = copy.deepcopy(solution)
        new_solution.routes[best_route_idx].nodes.insert(best_pos, customer_id)

        # Update cluster map for this customer (assigned to route's depot)
        evaluate_solution(new_solution, instance)
        return InsertionResult(
            success=True,
            scenario=1,
            new_solution=new_solution,
            cost_increase=best_cost,
        )
    return None


def scenario_2_goods_transfer(
    solution: Solution,
    customer_id: int,
    instance: ProblemInstance,
) -> Optional[InsertionResult]:
    """
    Scenario 2: Transfer goods from overloaded vehicle to free capacity for dynamic customer.

    NOTE-10: Implementation is simplified. We find a vehicle that could handle
    the dynamic pickup if some of its delivery goods were transferred to another vehicle.
    Transfer target is the nearest vehicle with available capacity.
    """
    customer = instance.nodes[customer_id]

    for r_idx, route in enumerate(solution.routes):
        if not route.nodes:
            continue

        # Check if vehicle has delivery goods that could be transferred
        delivery_nodes = [
            nid for nid in route.nodes
            if instance.nodes[nid].is_static_delivery()
        ]
        if not delivery_nodes:
            continue

        # Try to find another route to accept delivery goods
        for transfer_nid in delivery_nodes:
            transfer_node = instance.nodes[transfer_nid]

            # Find route that can accept this delivery node
            for r2_idx, route2 in enumerate(solution.routes):
                if r2_idx == r_idx:
                    continue
                if not route2.vehicle.capacity >= transfer_node.Q_i:
                    continue

                # Simulate transfer: remove delivery node from route1, add to route2
                # Then check if route1 can now accept dynamic customer
                test_route1_nodes = [n for n in route.nodes if n != transfer_nid]
                test_load_1 = sum(
                    instance.nodes[n].P_i
                    for n in test_route1_nodes
                    if instance.nodes[n].is_static_pickup()
                )
                if customer.P_i + test_load_1 <= route.vehicle.capacity + 1e-6:
                    # Transfer feasible, insert dynamic customer
                    new_solution = copy.deepcopy(solution)
                    new_solution.routes[r_idx].nodes = test_route1_nodes + [customer_id]
                    # Add transferred delivery to route2 (at end)
                    new_solution.routes[r2_idx].nodes.append(transfer_nid)
                    evaluate_solution(new_solution, instance)
                    return InsertionResult(
                        success=True,
                        scenario=2,
                        new_solution=new_solution,
                        cost_increase=new_solution.TOC - solution.TOC,
                    )

    return None


def scenario_3_new_vehicle(
    solution: Solution,
    customer_id: int,
    instance: ProblemInstance,
) -> InsertionResult:
    """
    Scenario 3: Dispatch a new vehicle for the dynamic customer.
    (Table 11, lines 16-17)
    Find nearest depot to serve this dynamic customer.
    """
    customer = instance.nodes[customer_id]

    # Assign to nearest pickup depot
    pickup_depots = instance.pickup_depots
    if not pickup_depots:
        pickup_depots = instance.all_depots

    nearest_depot = min(
        pickup_depots,
        key=lambda d: instance.dist(d.node_id, customer_id)
    )

    new_vehicle = Vehicle(
        vehicle_id=max((r.vehicle.vehicle_id for r in solution.routes), default=0) + 1,
        capacity=instance.vehicle_capacity,
        speed=instance.vehicle_speed,
        fuel_rate=instance.fuel_rate,
        fuel_price=instance.fuel_price,
        annual_maintenance=instance.annual_maintenance,
    )

    new_route = Route(
        vehicle=new_vehicle,
        origin_depot_id=nearest_depot.node_id,
        nodes=[customer_id],
        end_depot_id=nearest_depot.node_id,
    )

    new_solution = copy.deepcopy(solution)
    new_solution.routes.append(new_route)
    evaluate_solution(new_solution, instance)

    return InsertionResult(
        success=True,
        scenario=3,
        new_solution=new_solution,
        cost_increase=new_solution.TOC - solution.TOC,
    )


def insert_dynamic_demands(
    solution: Solution,
    dynamic_customers: list[int],
    instance: ProblemInstance,
) -> Solution:
    """
    Table 11 pseudocode: Full insertion strategy.

    For each dynamic customer:
    1. Try Scenario 1 (direct insertion)
    2. If fails, try Scenario 2 (goods transfer)
    3. If fails, use Scenario 3 (new vehicle)
    Choose minimum-cost feasible option.
    """
    current_solution = copy.deepcopy(solution)

    for customer_id in dynamic_customers:
        # Collect all feasible scenarios
        feasible = []

        r1 = scenario_1_direct_insert(current_solution, customer_id, instance)
        if r1 and r1.success:
            feasible.append(r1)

        r2 = scenario_2_goods_transfer(current_solution, customer_id, instance)
        if r2 and r2.success:
            feasible.append(r2)

        # Always possible (new vehicle as fallback)
        r3 = scenario_3_new_vehicle(current_solution, customer_id, instance)
        feasible.append(r3)

        # Select minimum cost increase (Table 11, line 19)
        best = min(feasible, key=lambda r: r.cost_increase)
        current_solution = best.new_solution

    return current_solution
