"""
Data model for MDPDTWDD (Multi-Depot Pickup & Delivery VRP with Time Windows & Dynamic Demands)
Paper: Wang et al. (2025), EAAI 139, 109700

Notation follows Table 4 of the paper exactly.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import math


class NodeType(Enum):
    """Customer/depot type classification."""
    DELIVERY_DEPOT = "DD"       # Delivery depot (W set)
    PICKUP_DEPOT = "PD"         # Pickup depot (O set)
    STATIC_DELIVERY = "R"       # Static delivery customer (R set)
    STATIC_PICKUP = "S"         # Static pickup customer (S set)
    DYNAMIC_PICKUP = "D"        # Dynamic pickup customer (D set)


@dataclass
class Node:
    """
    Represents a customer or depot in the MDPDTWDD network.

    Attributes follow Table 4 notation.
    [l_i, r_i] = time window of node i
    Q_i = delivery quantity
    P_i = pickup quantity
    """
    node_id: int
    x: float                    # x coordinate (or longitude for case study)
    y: float                    # y coordinate (or latitude for case study)
    node_type: NodeType

    # Demand quantities
    Q_i: float = 0.0            # Delivery quantity (only for R set)
    P_i: float = 0.0            # Pickup quantity (only for S, D sets)

    # Time windows [l_i, r_i]
    l_i: float = 0.0            # Early time window bound
    r_i: float = 1000.0         # Late time window bound

    # Dynamic demand arrival time (only for D set)
    # NOTE-01: Inferred from CSV 'Known time' column.
    # Known time = time at which dynamic demand becomes known to dispatcher.
    known_time: float = 0.0

    def is_depot(self) -> bool:
        return self.node_type in (NodeType.DELIVERY_DEPOT, NodeType.PICKUP_DEPOT)

    def is_delivery_depot(self) -> bool:
        return self.node_type == NodeType.DELIVERY_DEPOT

    def is_pickup_depot(self) -> bool:
        return self.node_type == NodeType.PICKUP_DEPOT

    def is_static_delivery(self) -> bool:
        return self.node_type == NodeType.STATIC_DELIVERY

    def is_static_pickup(self) -> bool:
        return self.node_type == NodeType.STATIC_PICKUP

    def is_dynamic(self) -> bool:
        return self.node_type == NodeType.DYNAMIC_PICKUP

    def __repr__(self) -> str:
        return f"Node({self.node_id}, {self.node_type.value}, Q={self.Q_i}, P={self.P_i}, TW=[{self.l_i},{self.r_i}])"


@dataclass
class Vehicle:
    """
    Represents a homogeneous vehicle.
    Paper: "Homogeneous vehicles are used" (Section 3.1).

    All vehicles share the same parameters from Table 15.
    """
    vehicle_id: int
    capacity: float             # ∂_v: vehicle capacity (= 100 per Table 15)
    speed: float                # α_v: travel speed (= 30 per Table 15)
    fuel_rate: float            # f_v: fuel consumption rate (= 0.07 per Table 15)
    fuel_price: float           # p_v: fuel price (= 7 per Table 15)
    annual_maintenance: float   # M_v: annual maintenance cost (= 40000 per Table 15)


@dataclass
class Route:
    """
    A single vehicle route: sequence of nodes from depot to depot.

    Open route: starts at DD, ends at PD (vehicle does both delivery and pickup)
    Closed route: starts and ends at same depot
    """
    vehicle: Vehicle
    origin_depot_id: int        # Starting depot (DD or PD)
    nodes: list[int] = field(default_factory=list)   # Ordered list of customer IDs visited
    end_depot_id: Optional[int] = None               # Ending depot (may differ from origin)

    def is_open(self) -> bool:
        """Open route: origin ≠ destination."""
        return self.end_depot_id is not None and self.end_depot_id != self.origin_depot_id


@dataclass
class Solution:
    """
    A complete solution to the MDPDTWDD.
    Contains a set of routes and the computed objective values.
    """
    routes: list[Route] = field(default_factory=list)

    # Objective values (computed by evaluate())
    TOC: float = float('inf')   # Total operating cost (Eq.15)
    NV: int = 0                  # Number of vehicles (Eq.16)
    TC: float = 0.0              # Travel cost (Eq.17)
    PC: float = 0.0              # Penalty cost (Eq.18)
    MC: float = 0.0              # Maintenance cost (Eq.19)
    IC: float = 0.0              # Insertion cost (Eq.20)
    FC: float = 0.0              # Fixed cost (Eq.21)

    def is_feasible(self) -> bool:
        return self.TOC < float('inf')


@dataclass
class ProblemInstance:
    """
    Complete problem instance for MDPDTWDD.

    Sets (following Table 4 notation):
    - W: delivery depots
    - O: pickup depots
    - F = W ∪ O: all depots
    - R: static delivery customers
    - S: static pickup customers
    - D: dynamic pickup customers
    - C = R ∪ S ∪ D: all customers
    """
    name: str
    nodes: dict[int, Node] = field(default_factory=dict)   # All nodes (customers + depots)

    # Problem parameters (from Table 15)
    working_days: int = 364         # T: number of working days per year
    vehicle_capacity: float = 100.0  # ∂_v
    vehicle_speed: float = 30.0      # α_v (km/h or consistent unit)
    fuel_rate: float = 0.07          # f_v (L/km)
    fuel_price: float = 7.0          # p_v ($/L)
    annual_maintenance: float = 40000.0  # M_v ($/year)
    epsilon: float = 20.0            # ε: early penalty coefficient ($/unit time)
    omega: float = 30.0              # ω: late penalty coefficient ($/unit time)
    delta: float = 1.0               # δ: cost coefficient per delivery unit
    chi: float = 1.0                 # χ: cost coefficient per pickup unit
    gamma: float = 1.0               # γ: insertion coefficient per dynamic pickup unit
    depot_fixed_cost: float = 0.0    # β_f: fixed cost per depot per day
                                     # NOTE-07: not given in Table 15, using 0.0

    # Distance and time matrices (computed after loading)
    dist_matrix: dict[tuple[int, int], float] = field(default_factory=dict)
    time_matrix: dict[tuple[int, int], float] = field(default_factory=dict)

    @property
    def delivery_depots(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_delivery_depot()]

    @property
    def pickup_depots(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_pickup_depot()]

    @property
    def all_depots(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_depot()]

    @property
    def static_delivery_customers(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_static_delivery()]

    @property
    def static_pickup_customers(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_static_pickup()]

    @property
    def dynamic_customers(self) -> list[Node]:
        return [n for n in self.nodes.values() if n.is_dynamic()]

    @property
    def all_customers(self) -> list[Node]:
        return [n for n in self.nodes.values() if not n.is_depot()]

    @property
    def static_customers(self) -> list[Node]:
        return [n for n in self.nodes.values()
                if n.node_type in (NodeType.STATIC_DELIVERY, NodeType.STATIC_PICKUP)]

    def dist(self, i: int, j: int) -> float:
        """Euclidean distance between nodes i and j."""
        return self.dist_matrix.get((i, j), self._compute_euclidean(i, j))

    def travel_time(self, i: int, j: int) -> float:
        """Travel time from i to j = distance / speed."""
        return self.dist(i, j) / self.vehicle_speed

    def _compute_euclidean(self, i: int, j: int) -> float:
        ni, nj = self.nodes[i], self.nodes[j]
        return math.sqrt((ni.x - nj.x) ** 2 + (ni.y - nj.y) ** 2)

    def build_distance_matrix(self):
        """Pre-compute all pairwise distances."""
        all_ids = list(self.nodes.keys())
        for i in all_ids:
            for j in all_ids:
                if i != j:
                    self.dist_matrix[(i, j)] = self._compute_euclidean(i, j)
                    self.time_matrix[(i, j)] = self.dist_matrix[(i, j)] / self.vehicle_speed

    def summary(self) -> str:
        """Human-readable summary of instance."""
        return (
            f"Instance: {self.name}\n"
            f"  Delivery depots (DD): {len(self.delivery_depots)}\n"
            f"  Pickup depots (PD):   {len(self.pickup_depots)}\n"
            f"  Static delivery (R):  {len(self.static_delivery_customers)}\n"
            f"  Static pickup (S):    {len(self.static_pickup_customers)}\n"
            f"  Dynamic pickup (D):   {len(self.dynamic_customers)}\n"
            f"  Total customers:      {len(self.all_customers)}\n"
        )
