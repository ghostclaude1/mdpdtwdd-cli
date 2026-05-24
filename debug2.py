import sys
sys.path.insert(0, '.')
from src.data_loader import load_benchmark_instance
from src.data_model import Vehicle, Route
from src.objectives import evaluate_route, evaluate_solution
from src.nsga2 import decode_chromosome, Chromosome
from src.clustering import APClustering3D
import random
random.seed(42)

inst = load_benchmark_instance(
    '/home/user/.workspace/vr-research/data/process/benchmark/1 Instance__Sheet1.csv')
clustering = APClustering3D(inst)
assignment = clustering.fit()
static_ids = [n.node_id for n in inst.static_customers]
cluster_map = {cid: assignment.get(cid, inst.all_depots[0].node_id) for cid in static_ids}
genes = static_ids.copy()
random.shuffle(genes)
chrom = Chromosome(genes=genes, cluster_map=cluster_map)
v = Vehicle(1, 100, 30, 0.07, 7, 40000)
sol = decode_chromosome(chrom, inst, v)
evaluate_solution(sol, inst)

print("=== AFTER FIX — Route-by-route breakdown ===")
from src.objectives import evaluate_route
for i, route in enumerate(sol.routes):
    ev = evaluate_route(route, inst)
    print(f"\nRoute {i+1} (origin={route.origin_depot_id}, {len(route.nodes)} nodes, TC=${ev.TC:.1f}, PC=${ev.PC:.1f}):")
    prev = route.origin_depot_id
    t = ev.arrival_times.get(route.origin_depot_id, 0)
    print(f"  Depart depot at t={t:.1f}")
    for nid in route.nodes:
        node = inst.nodes[nid]
        arr = ev.arrival_times.get(nid, -1)
        early = max(node.l_i - arr, 0)
        late = max(arr - node.r_i, 0)
        flag = "✓" if early == 0 and late == 0 else ("EARLY" if early > 0 else "LATE")
        print(f"  Node {nid:3d} ({node.node_type.value}): arrive={arr:6.1f}, TW=[{node.l_i:4.0f},{node.r_i:4.0f}], early={early:5.1f}, late={late:5.1f} {flag}")

print()
print(f"Total: TOC=${sol.TOC:.2f} TC=${sol.TC:.2f} PC=${sol.PC:.2f} MC=${sol.MC:.2f} FC=${sol.FC:.2f} NV={sol.NV}")

# Check what % of customers have violations
all_violations = []
for route in sol.routes:
    ev = evaluate_route(route, inst)
    for nid in route.nodes:
        node = inst.nodes[nid]
        arr = ev.arrival_times.get(nid, -1)
        early = max(node.l_i - arr, 0)
        late = max(arr - node.r_i, 0)
        if early > 0 or late > 0:
            all_violations.append((nid, early, late))

print(f"\nViolations: {len(all_violations)}/{sum(len(r.nodes) for r in sol.routes)} customers")
for nid, e, l in all_violations[:10]:
    print(f"  Node {nid}: early={e:.1f}, late={l:.1f}")
