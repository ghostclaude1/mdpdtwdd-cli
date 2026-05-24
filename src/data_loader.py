"""
Data loaders for MDPDTWDD benchmark and case study instances.

NOTE-01: Dynamic customers in CSV are identified by PCs column value == 4.
         Known_time column gives the arrival time of the dynamic demand.
         This is inferred from data inspection, not explicitly stated in paper.

NOTE-02: Raw .vrp files (Cordeau MDVRPTW format) are NOT used directly for
         the 30 benchmark instances. The CSV files in data/process/benchmark/
         are the actual processed instances used in the paper.
"""
import csv
import os
import math
from pathlib import Path
from typing import Optional

from src.data_model import (
    Node, NodeType, ProblemInstance
)


def _detect_node_type(row: dict) -> NodeType:
    """
    Determine node type from CSV row.

    Logic inferred from data patterns (NOTE-01):
    - DCs=1000: Delivery Depot (DD)
    - PCs=1000: Pickup Depot (PD)
    - DCs=1, delivery demand > 0: Static delivery customer (R)
    - PCs=1, pickup demand > 0, Known time == 0: Static pickup customer (S)
    - PCs=4, pickup demand > 0, Known time > 0: Dynamic pickup customer (D)
    """
    try:
        dcs = float(row.get('DCs', 0))
        pcs = float(row.get('PCs', 0))
        known_time = float(row.get('Known time', 0))
        delivery_demand = float(row.get('Delivery demands', 0))
        pickup_demand_str = row.get('Picku up demands', row.get('Pickup demands', '0'))
        pickup_demand = float(pickup_demand_str)
    except (ValueError, TypeError):
        return NodeType.STATIC_DELIVERY  # fallback

    if dcs >= 100:  # DCs=1000 for depot
        return NodeType.DELIVERY_DEPOT
    if pcs >= 100:  # PCs=1000 for depot
        return NodeType.PICKUP_DEPOT
    if pcs == 4 and known_time > 0:
        return NodeType.DYNAMIC_PICKUP  # NOTE-01: inferred
    if delivery_demand > 0 and pickup_demand == 0:
        return NodeType.STATIC_DELIVERY
    if pickup_demand > 0 and delivery_demand == 0:
        return NodeType.STATIC_PICKUP
    # Edge case: both zero (shouldn't happen for customers)
    return NodeType.STATIC_DELIVERY


def load_benchmark_instance(filepath: str, name: Optional[str] = None) -> ProblemInstance:
    """
    Load a benchmark instance from CSV format.

    CSV format (data/process/benchmark/):
    Nodes, X, Y, Delivery demands, Picku up demands,
    Time windows left D, Time windows right D,
    Time windows left P, Time windows right P,
    Known time, DCs, PCs

    Note: Column 'Picku up demands' has typo in source data.
    """
    if name is None:
        name = Path(filepath).stem

    instance = ProblemInstance(name=name)
    depot_counter = {'DD': 0, 'PD': 0}

    with open(filepath, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip empty rows
            if not row.get('Nodes', '').strip():
                continue

            try:
                node_id = int(float(row['Nodes']))
            except (ValueError, TypeError):
                continue

            try:
                x = float(row['X'])
                y = float(row['Y'])
            except (ValueError, TypeError):
                continue

            ntype = _detect_node_type(row)

            # Parse demands
            try:
                delivery_demand = float(row.get('Delivery demands', 0) or 0)
            except ValueError:
                delivery_demand = 0.0

            pickup_str = row.get('Picku up demands', row.get('Pickup demands', '0'))
            try:
                pickup_demand = float(pickup_str or 0)
            except ValueError:
                pickup_demand = 0.0

            # Parse time windows
            # Delivery customers use "Time windows left D / right D"
            # Pickup customers use "Time windows left P / right P"
            try:
                tw_left_d = float(row.get('Time windows left D', 0) or 0)
                tw_right_d = float(row.get('Time windows right D', 1000) or 1000)
                tw_left_p = float(row.get('Time windows left P', 0) or 0)
                tw_right_p = float(row.get('Time windows right P', 1000) or 1000)
            except (ValueError, TypeError):
                tw_left_d = tw_right_d = tw_left_p = tw_right_p = 0.0

            # Assign correct time window based on node type
            if ntype in (NodeType.DELIVERY_DEPOT, NodeType.STATIC_DELIVERY):
                l_i = tw_left_d
                r_i = tw_right_d
            elif ntype in (NodeType.PICKUP_DEPOT, NodeType.STATIC_PICKUP, NodeType.DYNAMIC_PICKUP):
                l_i = tw_left_p
                r_i = tw_right_p
            else:
                l_i, r_i = 0.0, 1000.0

            try:
                known_time = float(row.get('Known time', 0) or 0)
            except (ValueError, TypeError):
                known_time = 0.0

            node = Node(
                node_id=node_id,
                x=x,
                y=y,
                node_type=ntype,
                Q_i=delivery_demand,
                P_i=pickup_demand,
                l_i=l_i,
                r_i=r_i,
                known_time=known_time,
            )

            instance.nodes[node_id] = node

    instance.build_distance_matrix()
    return instance


def load_case_study(filepath: str, name: str = "chongqing_case") -> ProblemInstance:
    """
    Load the real-world case study (Chongqing city).

    CSV format (data/process/case/case.csv):
    No., Longitude, Latitude, Delivery demand, Pickup demand,
    Left time for delivering, Right time for delivering,
    Left time for pickup, Right time for pickup,
    Responsible DD, Responsible PD

    NOTE: Case study uses longitude/latitude (real coordinates).
    Distance computed as Euclidean on lat/lon (consistent with paper approach).
    For precise geographic distance, haversine should be used, but paper uses
    Euclidean on coordinate space (standard in VRP literature for case studies
    with small geographic area). Using Euclidean for consistency with paper.
    """
    instance = ProblemInstance(name=name)

    with open(filepath, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        node_id = 1

        for row in reader:
            label = row.get('No.', '').strip()
            if not label:
                continue

            try:
                lon = float(row['Longtitude'])
                lat = float(row['Latitude'])
            except (ValueError, KeyError):
                # Try alternate spelling
                try:
                    lon = float(row.get('Longitude', 0))
                    lat = float(row.get('Latitude', 0))
                except (ValueError, TypeError):
                    continue

            # Determine node type from label prefix
            if label.startswith('DD'):
                ntype = NodeType.DELIVERY_DEPOT
            elif label.startswith('PD'):
                ntype = NodeType.PICKUP_DEPOT
            else:
                # Determine from demand values
                try:
                    dd = float(row.get('Delivery demand', 0) or 0)
                    pd_demand = float(row.get('Pickup demand', 0) or 0)
                except (ValueError, TypeError):
                    dd = pd_demand = 0.0

                known = float(row.get('Known time', 0) or 0) if 'Known time' in row else 0.0

                if known > 0:
                    ntype = NodeType.DYNAMIC_PICKUP
                elif dd > 0:
                    ntype = NodeType.STATIC_DELIVERY
                elif pd_demand > 0:
                    ntype = NodeType.STATIC_PICKUP
                else:
                    ntype = NodeType.STATIC_DELIVERY

            try:
                delivery_demand = float(row.get('Delivery demand', 0) or 0)
                pickup_demand = float(row.get('Pickup demand', 0) or 0)
            except (ValueError, TypeError):
                delivery_demand = pickup_demand = 0.0

            try:
                l_d = float(row.get('Left time for delivering', 0) or 0)
                r_d = float(row.get('Right time for delivering', 1000) or 1000)
                l_p = float(row.get('Left time for pickup', 0) or 0)
                r_p = float(row.get('Right time for pickup', 1000) or 1000)
            except (ValueError, TypeError):
                l_d = l_p = 0.0
                r_d = r_p = 1000.0

            if ntype in (NodeType.DELIVERY_DEPOT, NodeType.STATIC_DELIVERY):
                l_i, r_i = l_d, r_d
            else:
                l_i, r_i = l_p, r_p

            node = Node(
                node_id=node_id,
                x=lon,
                y=lat,
                node_type=ntype,
                Q_i=delivery_demand,
                P_i=pickup_demand,
                l_i=l_i,
                r_i=r_i,
                known_time=0.0,
            )
            instance.nodes[node_id] = node
            node_id += 1

    instance.build_distance_matrix()
    return instance


def load_all_benchmark_instances(benchmark_dir: str) -> list[ProblemInstance]:
    """Load all 30 benchmark instances in sorted order."""
    import re
    instances = []
    bench_path = Path(benchmark_dir)

    # Find all CSV files
    csv_files = sorted(
        bench_path.glob("*.csv"),
        key=lambda p: int(re.search(r'(\d+)', p.name).group(1)) if re.search(r'(\d+)', p.name) else 0
    )

    for i, f in enumerate(csv_files, 1):
        inst = load_benchmark_instance(str(f), name=f"Instance_{i}")
        instances.append(inst)

    return instances
