"""
3D Affinity Propagation (AP) Clustering Algorithm.

Implements the 3D AP clustering from Section 4.2 of Wang et al. (2025).

Key equations:
- Eq.49: STD_ij = s * d_ij + t * min{|l_i-l_j|, |l_i-r_j|, |r_i-l_j|, |r_i-r_j|} * α_v
- Eq.50: R_{m+1}(i,j) = S(i,j) - max_{j'≠j}{A_m(i,j') + S(i,j')}
- Eq.51: A_{m+1}(i,j) = min{0, R_m(j,j) + Σ_{j'∉{i,j}} max{0, R_m(j',j)}} for i≠j
         A_{m+1}(j,j) = Σ_{j'≠j} max{0, R_m(j',j)} for i=j
- Eq.52: R_{m+1} = λ' * R_m + (1-λ') * R_{m+1}  (damping)
- Eq.53: A_{m+1} = λ' * A_m + (1-λ') * A_{m+1}  (damping)

Table 6 pseudocode:
  Initialize clustering centers with depots
  Calculate STD between all nodes
  Generate similarity matrix
  While m <= M:
      Calculate R_m, A_m
      Assign customers to clusters
      Update clusters
      If no change: break

NOTE-08: Spatial coefficient s and temporal coefficient t are NOT given in
the paper. Default s=t=0.5 used here. This is a known limitation.
The paper mentions these are "coefficients" but never specifies values.
Related work (WangEtAl2021 companion paper) uses normalized versions.
"""
from __future__ import annotations
import numpy as np
from typing import Optional
from src.data_model import ProblemInstance, Node, NodeType


class APClustering3D:
    """
    3D Affinity Propagation clustering for MDPDTWDD.

    The 3D refers to: geographic location (x,y) + time window → space-time distance.
    Depots serve as initial clustering centers (exemplars).
    """

    def __init__(
        self,
        instance: ProblemInstance,
        damping: float = 0.9,           # λ': damping coefficient (typical AP: 0.5-0.99)
        max_iter: int = 200,             # M: max iterations
        spatial_coeff: float = 0.5,      # s: NOTE-08 inferred
        temporal_coeff: float = 0.5,     # t: NOTE-08 inferred
    ):
        self.instance = instance
        self.damping = damping
        self.max_iter = max_iter
        self.spatial_coeff = spatial_coeff      # s in Eq.49
        self.temporal_coeff = temporal_coeff    # t in Eq.49

        # All nodes to cluster: customers + depots
        # Depots serve as exemplar candidates
        self.all_nodes = list(instance.nodes.values())
        self.node_ids = [n.node_id for n in self.all_nodes]
        self.n = len(self.node_ids)
        self.id_to_idx = {nid: i for i, nid in enumerate(self.node_ids)}

        # Matrices (n x n)
        self.S = None       # Similarity matrix
        self.R = None       # Responsibility matrix
        self.A = None       # Availability matrix

    def _space_time_distance(self, ni: Node, nj: Node) -> float:
        """
        Eq.49: STD_ij = s * d_ij + t * min{|l_i-l_j|, |l_i-r_j|, |r_i-l_j|, |r_i-r_j|} * α_v

        The minimum of the four differences represents the minimum time-window overlap distance.
        """
        d_ij = self.instance.dist(ni.node_id, nj.node_id)

        tw_dist = min(
            abs(ni.l_i - nj.l_i),
            abs(ni.l_i - nj.r_i),
            abs(ni.r_i - nj.l_j) if hasattr(nj, 'l_j') else abs(ni.r_i - nj.l_i),
            abs(ni.r_i - nj.r_i),
        )
        # Correct: using node attributes
        tw_dist = min(
            abs(ni.l_i - nj.l_i),
            abs(ni.l_i - nj.r_i),
            abs(ni.r_i - nj.l_i),
            abs(ni.r_i - nj.r_i),
        )

        return (self.spatial_coeff * d_ij
                + self.temporal_coeff * tw_dist * self.instance.vehicle_speed)

    def _build_similarity_matrix(self) -> np.ndarray:
        """
        Build similarity matrix S.
        S(i,j) = -STD_ij  (negative of space-time distance, as AP maximizes similarity)

        Diagonal S(i,i) is the preference for node i to be an exemplar.
        For depot nodes: set high preference (force them as exemplars).
        For customers: set to median of similarities (standard AP default).
        """
        S = np.zeros((self.n, self.n))

        for i, nid_i in enumerate(self.node_ids):
            ni = self.instance.nodes[nid_i]
            for j, nid_j in enumerate(self.node_ids):
                if i == j:
                    continue
                nj = self.instance.nodes[nid_j]
                std = self._space_time_distance(ni, nj)
                S[i, j] = -std  # Similarity = negative distance

        # Set diagonal (self-similarity / preference)
        # Depots: force as exemplars with very high preference
        depot_ids = {n.node_id for n in self.instance.all_depots}

        # For customer nodes: use median of off-diagonal similarities
        all_off_diag = S[~np.eye(self.n, dtype=bool)]
        median_pref = np.median(all_off_diag) if len(all_off_diag) > 0 else 0.0

        for i, nid in enumerate(self.node_ids):
            if nid in depot_ids:
                # Force depot as exemplar: very high preference
                S[i, i] = np.max(S) * 10 if np.max(S) != 0 else 1e6
            else:
                S[i, i] = median_pref  # Standard AP preference

        return S

    def fit(self) -> dict[int, int]:
        """
        Run 3D AP clustering (Table 6 pseudocode).

        Returns:
            cluster_assignment: dict mapping customer_id -> depot_id (exemplar)
        """
        self.S = self._build_similarity_matrix()
        self.R = np.zeros((self.n, self.n))
        self.A = np.zeros((self.n, self.n))

        prev_exemplars = None

        for m in range(1, self.max_iter + 1):
            # Step 1: Update responsibility matrix R (Eq.50)
            R_new = self._update_responsibility()

            # Step 2: Update availability matrix A (Eq.51)
            A_new = self._update_availability(R_new)

            # Step 3: Apply damping (Eqs.52, 53)
            self.R = self.damping * self.R + (1 - self.damping) * R_new
            self.A = self.damping * self.A + (1 - self.damping) * A_new

            # Step 4: Assign customers to clusters
            exemplars = self._get_exemplars()

            # Step 5: Check convergence (Table 6, line 12)
            if prev_exemplars is not None and exemplars == prev_exemplars:
                break
            prev_exemplars = exemplars

        return self._assign_clusters(exemplars)

    def _update_responsibility(self) -> np.ndarray:
        """
        Eq.50: R_{m+1}(i,j) = S(i,j) - max_{j'≠j}{A_m(i,j') + S(i,j')}
        """
        R_new = np.zeros((self.n, self.n))

        AS = self.A + self.S  # Shape: (n, n)

        for i in range(self.n):
            for j in range(self.n):
                # max over j' ≠ j
                vals = AS[i, :].copy()
                vals[j] = -np.inf
                R_new[i, j] = self.S[i, j] - np.max(vals)

        return R_new

    def _update_availability(self, R_new: np.ndarray) -> np.ndarray:
        """
        Eq.51:
        A_{m+1}(i,j) = min{0, R(j,j) + Σ_{j'∉{i,j}} max{0, R(j',j)}}  for i≠j
        A_{m+1}(j,j) = Σ_{j'≠j} max{0, R(j',j)}                         for i=j
        """
        A_new = np.zeros((self.n, self.n))

        for j in range(self.n):
            # Self-availability: sum of positive responsibilities from all i'≠j
            pos_r = np.maximum(0, R_new[:, j])
            pos_r[j] = 0  # exclude self
            A_new[j, j] = np.sum(pos_r)  # Eq.51 second case

            for i in range(self.n):
                if i == j:
                    continue
                # Eq.51 first case
                pos_r_excl = np.maximum(0, R_new[:, j].copy())
                pos_r_excl[i] = 0  # exclude i
                pos_r_excl[j] = 0  # j not in {i,j} means exclude j too
                # Actually re-reading Eq.51: j' ∉ {i,j}, so exclude both i and j
                A_new[i, j] = min(0, R_new[j, j] + np.sum(pos_r_excl))

        return A_new

    def _get_exemplars(self) -> set[int]:
        """
        Exemplars are nodes where R(i,i) + A(i,i) is maximized.
        In practice: node i is an exemplar if argmax_j{R(i,j)+A(i,j)} == i.
        """
        criterion = self.R + self.A
        exemplars = set()
        for i in range(self.n):
            if np.argmax(criterion[i, :]) == i:
                exemplars.add(i)

        # Always force depots as exemplars
        depot_ids = {n.node_id for n in self.instance.all_depots}
        for i, nid in enumerate(self.node_ids):
            if nid in depot_ids:
                exemplars.add(i)

        return frozenset(exemplars)

    def _assign_clusters(self, exemplar_indices: frozenset) -> dict[int, int]:
        """
        Assign each customer to the nearest exemplar (depot).
        Returns: customer_id -> depot_id
        """
        # Convert exemplar indices back to node IDs
        exemplar_node_ids = {self.node_ids[idx] for idx in exemplar_indices}

        # Only depot exemplars are valid cluster centers
        depot_ids = {n.node_id for n in self.instance.all_depots}
        valid_exemplars = exemplar_node_ids & depot_ids

        if not valid_exemplars:
            # Fallback: use all depots as exemplars
            valid_exemplars = depot_ids

        valid_exemplar_indices = [self.id_to_idx[nid] for nid in valid_exemplars]

        assignment = {}
        for i, nid in enumerate(self.node_ids):
            if self.instance.nodes[nid].is_depot():
                continue  # Skip depots, only assign customers

            # Assign to exemplar with highest similarity
            best_exemplar_idx = max(
                valid_exemplar_indices,
                key=lambda j: self.S[i, j]
            )
            best_depot_id = self.node_ids[best_exemplar_idx]
            assignment[nid] = best_depot_id

        return assignment


def cluster_by_depot_type(
    assignment: dict[int, int],
    instance: ProblemInstance,
) -> dict[int, list[int]]:
    """
    Group customer IDs by their assigned depot.
    Returns: depot_id -> [customer_id, ...]
    """
    clusters: dict[int, list[int]] = {}
    for depot in instance.all_depots:
        clusters[depot.node_id] = []

    for customer_id, depot_id in assignment.items():
        if depot_id not in clusters:
            clusters[depot_id] = []
        clusters[depot_id].append(customer_id)

    return clusters
