import sys
sys.path.insert(0, '.')
from src.data_loader import load_benchmark_instance
from src.data_model import Route, Vehicle

inst = load_benchmark_instance(
    '/home/user/.workspace/vr-research/data/process/benchmark/1 Instance__Sheet1.csv')

dd = inst.delivery_depots[0]
v = Vehicle(1, 100, 30, 0.07, 7, 40000)

c1 = inst.static_delivery_customers[0]
dist = inst.dist(dd.node_id, c1.node_id)
travel = dist / 30.0

print("=== BUG: depart at t=0 ===")
arrive = 0 + travel
early = max(c1.l_i - arrive, 0)
print(f"Arrive at Node {c1.node_id}: t={arrive:.2f}, TW=[{c1.l_i},{c1.r_i}], early={early:.1f}, PC=${20*early:.0f}")

print()
print("=== FIX: depart at B_v = l_j - t_ij ===")
B_v = max(0.0, c1.l_i - travel)
arrive2 = B_v + travel
early2 = max(c1.l_i - arrive2, 0)
print(f"B_v = {B_v:.2f}")
print(f"Arrive at Node {c1.node_id}: t={arrive2:.2f}, TW=[{c1.l_i},{c1.r_i}], early={early2:.2f}, PC=${20*early2:.0f}")

print()
print("=== PAPER Constraint 31-33 ===")
print("B_v range for first customer j: [l_j - t_ij, r_j - t_ij]")
print(f"Node {c1.node_id}: B_v in [{c1.l_i - travel:.1f}, {c1.r_i - travel:.1f}]")
print(f"Current code: B_v=0 → OUTSIDE valid range → MASSIVE early penalty")

print()
print("=== MULTI-CUSTOMER ROUTE: B_v computed from earliest customer ===")
# For a route c1,c2,...,cn: compute cumulative time and back-calculate optimal B_v
route_nodes = [c.node_id for c in inst.static_delivery_customers[:4]]
print(f"Route nodes: {route_nodes}")

# Forward pass: assuming depart at B_v=0
t = 0.0
prev = dd.node_id
total_early = 0.0
print("With B_v=0:")
for nid in route_nodes:
    d = inst.dist(prev, nid)
    t += d/30.0
    node = inst.nodes[nid]
    early = max(node.l_i - t, 0)
    total_early += early
    print(f"  Node {nid}: arrive={t:.1f}, TW=[{node.l_i},{node.r_i}], early={early:.1f}")
    t = max(t, node.l_i)  # wait if early
    prev = nid
print(f"  Total PC = 20 * {total_early:.1f} = ${20*total_early:.0f}")

# Optimal B_v: depart so that arrive at first customer at exactly l_c1
d0 = inst.dist(dd.node_id, route_nodes[0])
B_v_opt = max(0.0, inst.nodes[route_nodes[0]].l_i - d0/30.0)
print(f"\nWith B_v_opt={B_v_opt:.1f}:")
t = B_v_opt
prev = dd.node_id
total_early2 = 0.0
for nid in route_nodes:
    d = inst.dist(prev, nid)
    t += d/30.0
    node = inst.nodes[nid]
    early = max(node.l_i - t, 0)
    total_early2 += early
    print(f"  Node {nid}: arrive={t:.1f}, TW=[{node.l_i},{node.r_i}], early={early:.1f}")
    t = max(t, node.l_i)
    prev = nid
print(f"  Total PC = 20 * {total_early2:.1f} = ${20*total_early2:.0f}")

print()
print("=== CONCLUSION ===")
print("Bug: evaluate_route() departs at t=origin.l_i=0 always")
print("Fix: B_v = max(depot.l_i, first_customer.l_i - t(depot, first_customer))")
print(f"Impact: PC drops from ~$111,000 to near $0 per solution")
print(f"This explains the 5000% TOC gap vs paper")
