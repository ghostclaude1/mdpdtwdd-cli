"""Tests for data loader."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.data_loader import load_benchmark_instance, load_case_study
from src.data_model import NodeType

BENCH_DIR = "/home/user/.workspace/vr-research/data/process/benchmark"
CASE_FILE = "/home/user/.workspace/vr-research/data/process/case/case.csv"


def test_load_instance_1():
    inst = load_benchmark_instance(f"{BENCH_DIR}/1 Instance__Sheet1.csv", name="Instance_1")
    print(inst.summary())

    # Instance 1 per Table 14: 1 DD, 1 PD, 48 customers (25 delivery, 18 pickup, 5 dynamic)
    assert len(inst.delivery_depots) == 1, f"Expected 1 DD, got {len(inst.delivery_depots)}"
    assert len(inst.pickup_depots) == 1, f"Expected 1 PD, got {len(inst.pickup_depots)}"
    assert len(inst.all_customers) == 48, f"Expected 48 customers, got {len(inst.all_customers)}"
    assert len(inst.static_delivery_customers) == 25, f"Expected 25 static delivery, got {len(inst.static_delivery_customers)}"
    assert len(inst.static_pickup_customers) == 18, f"Expected 18 static pickup, got {len(inst.static_pickup_customers)}"
    assert len(inst.dynamic_customers) == 5, f"Expected 5 dynamic, got {len(inst.dynamic_customers)}"

    print("✓ Instance 1 loaded correctly")


def test_load_instance_2():
    inst = load_benchmark_instance(f"{BENCH_DIR}/2 Instance__Sheet1.csv", name="Instance_2")
    # Table 14: 1 DD, 1 PD, 72 customers (34 delivery, 28 pickup, 10 dynamic)
    assert len(inst.all_customers) == 72, f"Expected 72, got {len(inst.all_customers)}"
    assert len(inst.dynamic_customers) == 10, f"Expected 10 dynamic, got {len(inst.dynamic_customers)}"
    print("✓ Instance 2 loaded correctly")


def test_distance_matrix():
    inst = load_benchmark_instance(f"{BENCH_DIR}/1 Instance__Sheet1.csv")
    assert len(inst.dist_matrix) > 0
    # Distance between same node should be 0
    node_ids = list(inst.nodes.keys())
    for nid in node_ids[:5]:
        assert inst.dist(nid, nid) == 0 or inst.dist_matrix.get((nid, nid), 0) == 0
    print("✓ Distance matrix built")


def test_load_case_study():
    if not os.path.exists(CASE_FILE):
        print("⚠ Case file not found, skipping")
        return

    inst = load_case_study(CASE_FILE)
    print(inst.summary())
    assert len(inst.all_depots) >= 2, "Need at least one DD and one PD"
    print("✓ Case study loaded")


def test_dynamic_customer_known_time():
    inst = load_benchmark_instance(f"{BENCH_DIR}/1 Instance__Sheet1.csv")
    dynamics = inst.dynamic_customers
    for d in dynamics:
        assert d.known_time > 0, f"Dynamic customer {d.node_id} has known_time=0"
        assert d.P_i > 0, f"Dynamic customer {d.node_id} has no pickup demand"
    print(f"✓ Dynamic customers verified: {[(d.node_id, d.known_time, d.P_i) for d in dynamics]}")


if __name__ == '__main__':
    print("=" * 60)
    print("Running data loader tests...")
    print("=" * 60)
    test_load_instance_1()
    test_load_instance_2()
    test_distance_matrix()
    test_load_case_study()
    test_dynamic_customer_known_time()
    print("\n✅ All tests passed")
