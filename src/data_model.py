"""
Data model for MDPDTWDD (Multi-Depot Pickup & Delivery VRP with Time Windows & Dynamic Demands)
Paper: Wang et al. (2025), EAAI 139, 109700

Notation follows Table 4 of the paper exactly.

PERFORMANCE NOTES:
- dist_matrix / time_matrix replaced by dense numpy arrays (_dist_arr, _time_arr)
  indexed by compact 0-based index (_idx[node_id]).  O(1) array lookup vs dict hash.
- All @property lists cached as plain attributes after build_distance_matrix().
- Node-type membership encoded as precomputed frozensets for O(1) lookup.
- Per-node scalar arrays (_l_arr, _r_arr, _demand_arr, _epsilon_arr, _omega_arr)
  enable vectorised evaluate_route without per-node attribute access.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import math
import numpy as np


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
    [l_i, r_i] = time window; Q_i = delivery qty; P_i = pickup qty.
    """
    node_id: int
    x: float
    y: float
    node_type: NodeType

    Q_i: float = 0.0
    P_i: float = 0.0
    l_i: float = 0.0
    r_i: float = 1000.0
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
    """Homogeneous vehicle (Table 15)."""
    vehicle_id: int
    capacity: float
    speed: float
    fuel_rate: float
    fuel_price: float
    annual_maintenance: float

    def __post_init__(self):
        # Cache hot derived scalars
        self.fuel_cost_per_dist: float = self.fuel_rate * self.fuel_price
        self.maint_per_route: float = self.annual_maintenance / 364.0  # default T


@dataclass
class Route:
    """
    Single vehicle route: depot → [customers] → depot.
    Open route: origin_depot_id ≠ end_depot_id.
    """
    vehicle: Vehicle
    origin_depot_id: int
    nodes: list[int] = field(default_factory=list)
    end_depot_id: Optional[int] = None

    def is_open(self) -> bool:
        return self.end_depot_id is not None and self.end_depot_id != self.origin_depot_id


@dataclass
class Solution:
    """Complete MDPDTWDD solution with computed objective values."""
    routes: list[Route] = field(default_factory=list)

    TOC: float = float('inf')
    NV: int = 0
    TC: float = 0.0
    PC: float = 0.0
    MC: float = 0.0
    IC: float = 0.0
    FC: float = 0.0

    def is_feasible(self) -> bool:
        return self.TOC < float('inf')


@dataclass
class ProblemInstance:
    """
    Complete MDPDTWDD problem instance.

    After build_distance_matrix() is called, fast lookups are available:
      inst.dist_fast(i, j)        — O(1) numpy array lookup
      inst.travel_time_fast(i, j) — O(1) numpy array lookup
      inst.is_delivery[node_id]   — O(1) bool
      inst.is_pickup_node[node_id]— O(1) bool
      inst.is_dyn[node_id]        — O(1) bool
    """
    name: str
    nodes: dict[int, Node] = field(default_factory=dict)

    working_days: int = 364
    vehicle_capacity: float = 100.0
    vehicle_speed: float = 30.0
    fuel_rate: float = 0.07
    fuel_price: float = 7.0
    annual_maintenance: float = 40000.0
    epsilon: float = 20.0
    omega: float = 30.0
    delta: float = 1.0
    chi: float = 1.0
    gamma: float = 1.0
    depot_fixed_cost: float = 0.0

    # Legacy dict matrices (kept for compatibility, not used in hot paths)
    dist_matrix: dict[tuple[int, int], float] = field(default_factory=dict)
    time_matrix: dict[tuple[int, int], float] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    # Fast-access structures (populated by build_distance_matrix)         #
    # ------------------------------------------------------------------ #
    # numpy N×N distance / time arrays, row/col = _idx[node_id]
    _dist_arr: Optional[np.ndarray] = field(default=None, repr=False)
    _time_arr: Optional[np.ndarray] = field(default=None, repr=False)
    _idx: dict[int, int] = field(default_factory=dict, repr=False)
    _ids: list[int] = field(default_factory=list, repr=False)   # index → node_id
    _inv_speed: float = field(default=0.0, repr=False)

    # Per-node scalar arrays indexed by node_id (max_id+1 length, 0 for missing)
    _l_arr: Optional[np.ndarray] = field(default=None, repr=False)
    _r_arr: Optional[np.ndarray] = field(default=None, repr=False)
    _demand_arr: Optional[np.ndarray] = field(default=None, repr=False)  # Q or P

    # Type membership — O(1) set lookup replaces repeated Enum comparisons
    _delivery_depot_ids: frozenset = field(default_factory=frozenset, repr=False)
    _pickup_depot_ids: frozenset = field(default_factory=frozenset, repr=False)
    _static_delivery_ids: frozenset = field(default_factory=frozenset, repr=False)
    _static_pickup_ids: frozenset = field(default_factory=frozenset, repr=False)
    _dynamic_ids: frozenset = field(default_factory=frozenset, repr=False)

    # Cached list properties (populated once)
    _delivery_depots_cache: Optional[list] = field(default=None, repr=False)
    _pickup_depots_cache: Optional[list] = field(default=None, repr=False)
    _all_depots_cache: Optional[list] = field(default=None, repr=False)
    _static_customers_cache: Optional[list] = field(default=None, repr=False)
    _dynamic_customers_cache: Optional[list] = field(default=None, repr=False)
    _all_customers_cache: Optional[list] = field(default=None, repr=False)
    _static_delivery_cache: Optional[list] = field(default=None, repr=False)
    _static_pickup_cache: Optional[list] = field(default=None, repr=False)

    # ------------------------------------------------------------------
    # Boolean lookup arrays (size = max_node_id+1)
    is_delivery: Optional[np.ndarray] = field(default=None, repr=False)   # bool[id]
    is_pickup_node: Optional[np.ndarray] = field(default=None, repr=False)
    is_dyn: Optional[np.ndarray] = field(default=None, repr=False)
    is_depot_arr: Optional[np.ndarray] = field(default=None, repr=False)
    is_dd_arr: Optional[np.ndarray] = field(default=None, repr=False)
    is_pd_arr: Optional[np.ndarray] = field(default=None, repr=False)

    # ------------------------------------------------------------------
    # @property shims — delegate to cached values after build
    @property
    def delivery_depots(self) -> list[Node]:
        if self._delivery_depots_cache is None:
            self._delivery_depots_cache = [n for n in self.nodes.values() if n.is_delivery_depot()]
        return self._delivery_depots_cache

    @property
    def pickup_depots(self) -> list[Node]:
        if self._pickup_depots_cache is None:
            self._pickup_depots_cache = [n for n in self.nodes.values() if n.is_pickup_depot()]
        return self._pickup_depots_cache

    @property
    def all_depots(self) -> list[Node]:
        if self._all_depots_cache is None:
            self._all_depots_cache = [n for n in self.nodes.values() if n.is_depot()]
        return self._all_depots_cache

    @property
    def static_delivery_customers(self) -> list[Node]:
        if self._static_delivery_cache is None:
            self._static_delivery_cache = [n for n in self.nodes.values() if n.is_static_delivery()]
        return self._static_delivery_cache

    @property
    def static_pickup_customers(self) -> list[Node]:
        if self._static_pickup_cache is None:
            self._static_pickup_cache = [n for n in self.nodes.values() if n.is_static_pickup()]
        return self._static_pickup_cache

    @property
    def dynamic_customers(self) -> list[Node]:
        if self._dynamic_customers_cache is None:
            self._dynamic_customers_cache = [n for n in self.nodes.values() if n.is_dynamic()]
        return self._dynamic_customers_cache

    @property
    def all_customers(self) -> list[Node]:
        if self._all_customers_cache is None:
            self._all_customers_cache = [n for n in self.nodes.values() if not n.is_depot()]
        return self._all_customers_cache

    @property
    def static_customers(self) -> list[Node]:
        if self._static_customers_cache is None:
            self._static_customers_cache = [
                n for n in self.nodes.values()
                if n.node_type in (NodeType.STATIC_DELIVERY, NodeType.STATIC_PICKUP)
            ]
        return self._static_customers_cache

    # ------------------------------------------------------------------
    # Distance / time — hot path: O(1) array lookup
    def dist_fast(self, i: int, j: int) -> float:
        """O(1) distance lookup via numpy array."""
        return self._dist_arr[self._idx[i], self._idx[j]]

    def travel_time_fast(self, i: int, j: int) -> float:
        """O(1) travel time lookup via numpy array."""
        return self._time_arr[self._idx[i], self._idx[j]]

    # Backward-compatible aliases (used everywhere in existing code)
    def dist(self, i: int, j: int) -> float:
        if self._dist_arr is not None:
            return self._dist_arr[self._idx[i], self._idx[j]]
        return self.dist_matrix.get((i, j), self._compute_euclidean(i, j))

    def travel_time(self, i: int, j: int) -> float:
        if self._time_arr is not None:
            return self._time_arr[self._idx[i], self._idx[j]]
        return self.dist(i, j) / self.vehicle_speed

    def _compute_euclidean(self, i: int, j: int) -> float:
        ni, nj = self.nodes[i], self.nodes[j]
        return math.sqrt((ni.x - nj.x) ** 2 + (ni.y - nj.y) ** 2)

    def build_distance_matrix(self):
        """
        Precompute all pairwise distances into a dense numpy N×N array.
        Also builds all cached lookup structures.
        O(N²) once; all subsequent calls are O(1).
        """
        all_ids = sorted(self.nodes.keys())
        n = len(all_ids)
        self._ids = all_ids
        self._idx = {nid: i for i, nid in enumerate(all_ids)}
        self._inv_speed = 1.0 / self.vehicle_speed

        # Build coordinate arrays for vectorised distance computation
        xs = np.array([self.nodes[nid].x for nid in all_ids], dtype=np.float64)
        ys = np.array([self.nodes[nid].y for nid in all_ids], dtype=np.float64)

        # Broadcasting: (N,1) - (1,N) → (N,N)
        dx = xs[:, None] - xs[None, :]
        dy = ys[:, None] - ys[None, :]
        self._dist_arr = np.sqrt(dx * dx + dy * dy)
        self._time_arr = self._dist_arr * self._inv_speed

        # Also populate legacy dicts (used by clustering code)
        for i, nid_i in enumerate(all_ids):
            for j, nid_j in enumerate(all_ids):
                if i != j:
                    d = float(self._dist_arr[i, j])
                    self.dist_matrix[(nid_i, nid_j)] = d
                    self.time_matrix[(nid_i, nid_j)] = d * self._inv_speed

        # ---- Type membership sets ------------------------------------ #
        self._delivery_depot_ids = frozenset(
            n.node_id for n in self.nodes.values() if n.is_delivery_depot()
        )
        self._pickup_depot_ids = frozenset(
            n.node_id for n in self.nodes.values() if n.is_pickup_depot()
        )
        self._static_delivery_ids = frozenset(
            n.node_id for n in self.nodes.values() if n.is_static_delivery()
        )
        self._static_pickup_ids = frozenset(
            n.node_id for n in self.nodes.values() if n.is_static_pickup()
        )
        self._dynamic_ids = frozenset(
            n.node_id for n in self.nodes.values() if n.is_dynamic()
        )

        # ---- Boolean lookup arrays ----------------------------------- #
        max_id = max(all_ids)
        sz = max_id + 1
        self.is_delivery  = np.zeros(sz, dtype=bool)
        self.is_pickup_node = np.zeros(sz, dtype=bool)
        self.is_dyn       = np.zeros(sz, dtype=bool)
        self.is_depot_arr = np.zeros(sz, dtype=bool)
        self.is_dd_arr    = np.zeros(sz, dtype=bool)
        self.is_pd_arr    = np.zeros(sz, dtype=bool)
        for nid in self._static_delivery_ids:
            self.is_delivery[nid] = True
        for nid in self._static_pickup_ids:
            self.is_pickup_node[nid] = True
        for nid in self._dynamic_ids:
            self.is_dyn[nid] = True
            self.is_pickup_node[nid] = True
        for nid in self._delivery_depot_ids:
            self.is_depot_arr[nid] = True
            self.is_dd_arr[nid] = True
        for nid in self._pickup_depot_ids:
            self.is_depot_arr[nid] = True
            self.is_pd_arr[nid] = True

        # ---- Per-node scalar arrays (indexed by node_id) ------------- #
        self._l_arr = np.zeros(sz, dtype=np.float64)
        self._r_arr = np.zeros(sz, dtype=np.float64)
        self._demand_arr = np.zeros(sz, dtype=np.float64)
        for nid, node in self.nodes.items():
            self._l_arr[nid] = node.l_i
            self._r_arr[nid] = node.r_i
            # demand: Q_i for delivery, P_i for pickup/dynamic
            if node.is_static_delivery():
                self._demand_arr[nid] = node.Q_i
            else:
                self._demand_arr[nid] = node.P_i

        # ---- Warm up cached list properties ------------------------- #
        _ = self.delivery_depots
        _ = self.pickup_depots
        _ = self.all_depots
        _ = self.static_customers
        _ = self.dynamic_customers
        _ = self.all_customers
        _ = self.static_delivery_customers
        _ = self.static_pickup_customers

    def summary(self) -> str:
        return (
            f"Instance: {self.name}\n"
            f"  Delivery depots (DD): {len(self.delivery_depots)}\n"
            f"  Pickup depots (PD):   {len(self.pickup_depots)}\n"
            f"  Static delivery (R):  {len(self.static_delivery_customers)}\n"
            f"  Static pickup (S):    {len(self.static_pickup_customers)}\n"
            f"  Dynamic pickup (D):   {len(self.dynamic_customers)}\n"
            f"  Total customers:      {len(self.all_customers)}\n"
        )
