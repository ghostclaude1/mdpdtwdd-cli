# Paper Math Blocks

Chỉ chứa công thức LaTeX trích từ paper. Không có giải thích văn bản.

---

<!-- tag: Eq15 -->
$$\min TOC = TC + PC + MC + IC + FC$$

<!-- tag: Eq16 -->
$$\min NV = \sum_{v \in V} \sum_{i \in F} \sum_{j \in C} x^v_{ij}$$

<!-- tag: Eq17 -->
$$TC = \sum_{v \in V} \sum_{i \in C \cup F} \sum_{j \in C \cup F} f_v \cdot p_v \cdot x^v_{ij} \cdot d_{ij}$$

<!-- tag: Eq18 -->
$$PC = \sum_{v \in V} \sum_{i \in C} \left( \epsilon \cdot \max\{l_i - A^v_i, 0\} + \omega \cdot \max\{A^v_i - r_i, 0\} \right)$$

<!-- tag: Eq19 -->
$$MC = \sum_{v \in V} \sum_{i \in C \cup F} \sum_{j \in C \cup F} \frac{M_v \cdot x^v_{ij}}{T}$$

<!-- tag: Eq20 -->
$$IC = \sum_{v \in V} \sum_{f \in F} \sum_{i \in D} y^v_{if} \cdot P_i \cdot \gamma$$

<!-- tag: Eq21 -->
$$FC = \sum_{f \in F} \beta_f + \delta \cdot \sum_{i \in R} Q_i + \chi \cdot \sum_{i \in S \cup D} P_i$$

---

<!-- tag: Constraint22 -->
$$\sum_{v \in V} \sum_{j \in C \cup F} x^v_{ij} = 1, \quad \forall i \in R \cup S$$

<!-- tag: Constraint23 -->
$$\sum_{i \in F} x^v_{ij} = \sum_{i \in F} x^v_{ji}, \quad \forall j \in C, \forall v \in V$$

<!-- tag: Constraint24 -->
$$\sum_{j \in C \cup W} L^v_j = \sum_{i \in R} Q_i, \quad \forall v \in V$$

<!-- tag: Constraint25 -->
$$L^v_i \leq \partial_v, \quad \forall i \in C \cup F, \forall v \in V$$

<!-- tag: Constraint26 -->
$$L^v_j = L^v_i + Q_j, \quad \forall i,j \in R, \forall v \in V$$

<!-- tag: Constraint27 -->
$$L^v_j = L^v_i + P_j, \quad \forall i \in R, j \in S, \forall v \in V$$

<!-- tag: Constraint28 -->
$$L^v_j = L^v_i - Q_i + P_j, \quad \forall i \in R, j \in S, \forall v \in V$$

<!-- tag: Constraint29 -->
$$\sum_{f \in O} y^v_{if} = 1, \quad \forall i \in C, \forall v \in V$$

<!-- tag: Constraint30 -->
$$\sum_{f \in W} y^v_f = 1, \quad \forall v \in V$$

<!-- tag: Constraint31 -->
$$A^v_f = 0, \quad \forall f \in O, \forall v \in V$$

<!-- tag: Constraint32 -->
$$A^v_j = A^v_i + s_i + t_{ij}, \quad \forall i,j \in C \cup F, \forall v \in V$$

<!-- tag: Constraint33 -->
$$l_i \leq A^v_i, \quad \forall i \in C, \forall v \in V$$

<!-- tag: Constraint34 -->
$$A^v_i \leq r_i, \quad \forall i \in C, \forall v \in V$$

<!-- tag: Constraint35 -->
$$A^v_f \leq T, \quad \forall f \in W, \forall v \in V$$

<!-- tag: Constraint36 -->
$$A^v_i + s_i + t_{if} \leq T, \quad \forall i \in C, f \in W, \forall v \in V$$

<!-- tag: Constraint37 -->
$$A^v_i \geq 0, \quad \forall i \in C \cup F, \forall v \in V$$

<!-- tag: Constraint38 -->
$$u_i - u_j + n \cdot x^v_{ij} \leq n - 1, \quad \forall i,j \in C, \forall v \in V$$

---

<!-- tag: Constraint39 -->
$$\sum_{v \in V} \sum_{i \in C \cup F} \sum_{j \in C \cup F} x^v_{ikj} = 1, \quad \forall k \in D$$

<!-- tag: Constraint40 -->
$$\sum_{i \in C \cup F} x^v_{ikj} = \sum_{i \in C \cup F} x^v_{jki}, \quad \forall j \in C, k \in D, \forall v \in V$$

<!-- tag: Constraint41 -->
$$x^v_{ikj} \leq x^v_{ij}, \quad \forall i,j \in C \cup F, k \in D, \forall v \in V$$

<!-- tag: Constraint42 -->
$$L^{v'}_k = L^v_i + P_k, \quad \forall i \in C \cup F, k \in D, \forall v \in V$$

<!-- tag: Constraint43 -->
$$L^{v'}_k \leq \partial_v, \quad \forall k \in D, \forall v \in V$$

<!-- tag: Constraint44 -->
$$A^{v'}_k = A^v_i + s_i + t_{ik}, \quad \forall i \in C \cup F, k \in D, \forall v \in V$$

<!-- tag: Constraint45 -->
$$l_k \leq A^{v'}_k, \quad \forall k \in D$$

<!-- tag: Constraint46 -->
$$A^{v'}_k \leq r_k, \quad \forall k \in D$$

<!-- tag: Constraint47 -->
$$A^{v'}_j = A^{v'}_k + s_k + t_{kj}, \quad \forall j \in C \cup F, k \in D, \forall v \in V$$

<!-- tag: Constraint48 -->
$$u_i - u_k + u_k - u_j + n \cdot x^v_{ikj} \leq n - 1, \quad \forall i,j \in C, k \in D, \forall v \in V$$

---

<!-- tag: Eq49 -->
$$STD_{ij} = s \cdot d_{ij} + t \cdot \min\{|l_i - l_j|, |l_i - r_j|, |r_i - l_j|, |r_i - r_j|\} \cdot \alpha_v$$

<!-- tag: Eq50 -->
$$R(i,k) = S(i,k) - \max_{k' \neq k}\{A(i,k') + S(i,k')\}$$

<!-- tag: Eq51 -->
$$A(i,k) = \min\left\{0, R(k,k) + \sum_{i' \neq i,k} \max\{0, R(i',k)\}\right\}$$

<!-- tag: Eq52 -->
$$R_{new}(i,k) = \lambda \cdot R_{old}(i,k) + (1 - \lambda) \cdot R_{new}(i,k)$$

<!-- tag: Eq53 -->
$$A_{new}(i,k) = \lambda \cdot A_{old}(i,k) + (1 - \lambda) \cdot A_{new}(i,k)$$

<!-- tag: Eq54 -->
$$fit = \frac{1}{TOC/TOC_{max} + NV/NV_{max}}$$

<!-- tag: Eq55 -->
$$m_p = m_p \cdot \left(1 - \frac{gen}{M_{gen}}\right)$$

<!-- tag: Eq56 -->
$$s_{ij} = \frac{1}{x^v_{ij} + d_{ij}/\max\{d_{ij}\}}$$
