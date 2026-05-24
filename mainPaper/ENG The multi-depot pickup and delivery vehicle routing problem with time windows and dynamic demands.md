# The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands

**Authors:** Yong Wang, Mengyuan Gou, Siyu Luo, Jianxin Fan, Haizhong Wang  
**Journal:** Engineering Applications of Artificial Intelligence 139 (2025) 109700

>[!SUMMARY]+ Table of Contents
>- [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands|The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#ABSTRACT|ABSTRACT]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#1. Introduction|1. Introduction]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#2. Literature review|2. Literature review]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#2.1. VRPTWDD|2.1. VRPTWDD]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#2.2. PDVRPTWDD|2.2. PDVRPTWDD]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#2.3. MDPDVRPTW|2.3. MDPDVRPTW]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#2.4. MDVRPTW-RS|2.4. MDVRPTW-RS]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#3. Problem statement and model formulation|3. Problem statement and model formulation]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#3.1. Problem statement|3.1. Problem statement]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#3.2. Theorem proof|3.2. Theorem proof]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#3.3. Assumptions and definitions|3.3. Assumptions and definitions]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#3.4. Mathematical model|3.4. Mathematical model]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4. Solution methodology|4. Solution methodology]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.1. Two-stage hybrid algorithm|4.1. Two-stage hybrid algorithm]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.2. 3D AP clustering algorithm|4.2. 3D AP clustering algorithm]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.3. Elite iteration|4.3. Elite iteration]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.3.1. Genetic operation|4.3.1. Genetic operation]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.3.2. Local search operator|4.3.2. Local search operator]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.3.3. Pareto optimal solution|4.3.3. Pareto optimal solution]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#4.4. The insertion strategy for dynamic demands|4.4. The insertion strategy for dynamic demands]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5. Implementation and analysis|5. Implementation and analysis]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.1. Algorithm performance test|5.1. Algorithm performance test]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.1.1. Small-scale instances|5.1.1. Small-scale instances]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.1.2. Medium-large scale instances|5.1.2. Medium-large scale instances]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.2. Data description|5.2. Data description]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.3. Optimization results|5.3. Optimization results]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.3.1. Customer clustering result analysis|5.3.1. Customer clustering result analysis]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.3.2. Stability analysis for parameter selection|5.3.2. Stability analysis for parameter selection]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.3.3. MDPDTWDD optimization results|5.3.3. MDPDTWDD optimization results]]
>        - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.4. Analysis and discussion|5.4. Analysis and discussion]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.4.1. Comparison of different types for time windows|5.4.1. Comparison of different types for time windows]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.4.2. Comparison of different vehicle capacities|5.4.2. Comparison of different vehicle capacities]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.4.3. Comparison of different cases for resource sharing|5.4.3. Comparison of different cases for resource sharing]]
>            - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.4.4. Result comparison of insertion strategies adopted in different scenarios|5.4.4. Result comparison of insertion strategies adopted in different scenarios]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#5.5. Management insights|5.5. Management insights]]
>    - [[ENG The multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands#6. Conclusions|6. Conclusions]]

## ABSTRACT

The rapid development of the urban logistics recycling industry, combined with the complexity of the pickup and delivery networks, has created a surge in dynamic customer demands and exacerbated the difficulty of logistics resource sharing. Accordingly, this work focuses on a multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands, which incorporates resource sharing. A bi-objective mathematical model is formulated to minimize the total operating cost and number of vehicles. A three-dimensional affinity propagation clustering and an adaptive nondominated sorting genetic algorithm-II are combined to find Pareto optimal solutions. A dynamic demand insertion strategy is proposed to determine the vehicle service sequences for dynamic situations. Combined with an elite iteration mechanism to prevent the proposed algorithm from falling into search stagnation and improve the convergence performance. The superiority of the proposed algorithm is verified by comparing with CPLEX solver (i.e., ILOG CPLEX Optimization Studio 12.10), multi-objective ant colony optimization, multi-objective particle swarm optimization, multi-objective evolutionary algorithm, multi-objective genetic algorithm, and decomposition-based multi-objective evolutionary algorithm with tabu search. Besides, the proposed model and algorithm are tested by a real-world case study in Chongqing city, China, and the further analysis indicates that significant improvement can be achieved. Furthermore, by incorporating the recognition and prediction techniques of artificial intelligence on dynamic demand data, the proposed approach can realize the self-optimization of multi-depot vehicle routes and the precise allocation of logistics resources in dynamic environments. This study is conducive to the construction of a digitally-intelligent urban logistics system.

## 1. Introduction

With a globalized economy and money digitalization, not only has logistics market has been growing by leaps and bounds, but the customer demands have also become diverse and dynamic (Bergmann et al., 2020; Niu et al., 2021). For example, China’s parcel volume from e-commerce reached 132.1 billion items in 2023, which accounted for more than half of around the world. Meanwhile, the emphasis on environmental pollution, the promise of carbon peak and carbon neutrality, the enforcement of policies on green recycling and garbage sorting, etc., have enhanced residents’ awareness of recycling (Konstantakopoulos et al., 2022; Gutiérrez-Sánchez and Rocha-Medina, 2022). Therefore, how to optimize the operation of logistics networks to reduce the operating cost and mitigate the environmental impacts of logistics activities has become a meaningful and worthwhile question. However, limited resources, fierce competition, rising fuel prices, traffic congestion, and environmental protection regulations have significantly affected the efficiency of logistics network operations (Cleophas et al., 2019; Kim et al., 2023). These aspects require enterprises to build sustainable and win-win green logistics systems (An et al., 2019; Asghari and Al-e-hashem, 2020; Deng et al., 2023). Furthermore, collaboration and resource sharing are valued and widely adopted to improve logistics management operations and ease operational pressures, particularly in the fields of supply chain management, transportation, and renewable resource manufacturing (Hosseinnezhad et al., 2023; Kim et al., 2023).

How to design efficient schedules and integrate pickup and delivery activities through collaboration and resource sharing has become a key issue in practice. This study proposes and investigates a multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands (MDPDTWDD). In the collaborative logistics network of the MDPDTWDD, multiple depots (e.g., delivery and pickup depots) simultaneously provide service for a large number of customers (e.g., pickup customers, delivery customers, and pickup customers with dynamic demands) (He et al., 2019; Guo et al., 2021). Dynamic pickup demand information is frequently sent to depots after the service arrangements have been made (Soeffker et al., 2021; Ulmer et al., 2021). Accordingly, some adjustments and strategies are needed to meet these dynamic pickup demands (Demirbilek, 2021; Du et al., 2023; Wan et al., 2023). The integration of pickups and deliveries facilitates efficient operation of logistics networks and can be achieved by allowing vehicles to perform pickup and delivery services on the same route (Wong et al., 2018; Pan et al., 2020).

Although the aforementioned studies focused on solving problems related to the MDPDTWDD, they have several limitations: (1) Due to the complexity of dynamic demands and the diversity of multi-depot vehicle routing problems, the problem of incorporating the multi-depot pickup and delivery vehicle routing problem and dynamic vehicle routing problem has not been given sufficient attention. (2) Gaps exist in the study of collaboration and resource sharing in the MDPDTWDD. Furthermore, the insertion strategy for dynamic demands has not been sufficiently accounted for in the multi-depot network with dynamic demands. (3) Valid model formulations for the integration of pickup and delivery services and the insertion of dynamic demands among multiple logistics facilities to solve the MDPDTWDD are still lacking. (4) The existing intelligent algorithms for solving the multi-depot vehicle routing problem with time windows (MDVRPTW) and pickup and delivery vehicle routing problem with time windows (PDVRPTW) have limited applicability in solving the MDPDTWDD with collaboration and resource sharing.

This study formulates the MDPDTWDD, in which collaboration and resource sharing are incorporated to balance the resource allocation. A bi-objective mathematical model considering the resource integration is established to optimize the total operating cost (TOC) and number of vehicles. Then, a two-stage hybrid algorithm composed of the three dimensional (3D) affinity propagation (AP) clustering algorithm and the adaptive nondominated sorting genetic algorithm-II (ANSGA-II) (3DAPANSGA-II) is designed to find the Pareto optimal solutions. The 3D AP clustering algorithm is employed to reassign customers to depots on the basis of space-time distances. The elite iteration with local search is designed in the ANSGA-II to ensure optimality. Besides, an insertion strategy is proposed to find the optimal service arrangements with slight changes for satisfying dynamic pickup demands. The numerical results of a real-world case study in Chongqing city, China show that significant improvements can be achieved by adopting the proposed approach, and prove that multiple depots can improve service efficiency by participating in collaboration and resource sharing as much as possible.

Compared with previous studies, several innovative contributions in theory and application are presented as follows. (1) An extended problem of multi-depot pickup and delivery vehicle routing problem with time windows and dynamic demands is presented and studied, which advances the fields of study in MDVRPTW and PDVRPTW. (2) Collaboration and resource sharing are leveraged to promote the integration of pickup and delivery services by constructing open-closed pickup and delivery vehicle routes, thereby achieving rational resource configuration and improve transportation efficiency. Furthermore, an insertion strategy is proposed to find appropriate service routes for dynamic demands without a significant increase in logistics operating costs. (3) A bi-objective mathematical model considering dynamic demands and open-closed pickup and delivery routes is established to minimize the logistics operating costs and number of vehicles in the MDPDTWDD. (4) A two-stage hybrid algorithm with the three dimensional affinity propagation clustering and the adaptive nondominated sorting genetic algorithm-II is developed to solve the bi-objective optimization model, and then find the Pareto optimal solutions and determine the open-closed vehicle routes for the MDPDTWDD.

The remainder of the contents are organized as follows. Section 2 summarizes related literature. Section 3 states the problem of the MDPDTWDD, and proposes a bi-objective mathematical model to minimize the TOC and number of vehicles for solving the MDPDTWDD. Section 4 designs a two-stage hybrid algorithm composed of 3D AP clustering algorithm and ANSGA-II. Section 5 verifies the effectiveness of the proposed model and algorithm by the instances of the different scales and a case study. Section 6 summarizes the conclusions and future research directions.

## 2. Literature review

With the expansion of the logistics market and the change of customer demand characteristics, scholars have shown strong interest in the vehicle routing problem with time windows and dynamic demands (VRPTWDD) (Pan et al., 2020; Niu et al., 2021). In existing literature, scholars have conducted studies on the pickup and delivery vehicle routing problem with time windows and dynamic demands (PDVRPTWDD), multi-depot pickup and delivery vehicle routing problem with time windows (MDPDVRPTW), and multi-depot vehicle routing problem with time windows and resource sharing (MDVRPTW-RS), and they have made promising contributions (Györgyi and Kis, 2019; Li et al., 2018; Kocatürk et al., 2021).

### 2.1. VRPTWDD

As an important extension of the vehicle routing problem, the VRPTWDD needs to optimize vehicle routes in response to dynamic demands (Calvet et al., 2019; Soeffker et al., 2021). When the dynamic demand arrives, the preplanned service arrangement for static demands has to be adjusted to adapt to the demand change in the logistics network (Karami et al., 2020; Júnior et al., 2021). In order to reduce the impact of dynamic demands on the preplanned service arrangement, various strategies were proposed to handle the dynamic demands (Achamrah et al., 2022; Sarbijan and Behnamian, 2023). Abdirad et al. (2020) studied the VRPTWDD, where new requests arrived at depots, while vehicles were executing the preplanned service arrangement for existing demands. Ouertani et al. (2020) solved a VRPTWDD in terms of minimizing the travel risk and the transportation cost, where demands revealed time and the service time windows were considered.

In addition, Soeffker et al. (2021) designed the sequential decision and prescriptive analytics to deal with the dynamic demands. Archetti et al. (2021) proposed a re-optimization strategy to solve the VRPTWDD, which replans the service arrangement when the dynamic demand arrives. Li et al. (2023c) embedded an elastic strategy in the genetic algorithm to find the optimal vehicle routes in the VRPTWDD, considering the increase of distribution nodes. Combined with the artificial intelligence (AI), the postponed service strategy was adopted to solve the VRPTWDD problem, where the part of dynamic demands can be delayed (Ulmer et al., 2018, 2019; Li et al., 2023a). Besides, the effectiveness of the insertion strategy was verified in solving the VRPTWDD, in which customers with dynamic demands were inserted into the obtained service routes for customers with static demands (Júnior et al., 2021; Wang et al., 2024a).

### 2.2. PDVRPTWDD

The problem of pickup and delivery goods under dynamic environment is common and relevant. Accordingly, several scholars have studied the PDVRPTWDD (Zhu and Sheu, 2018; Zhang et al., 2020; Demirbilek, 2021). In the PDVRPTWDD, the decision makers need to coordinate the different types of logistics services (i.e., pickup and delivery services) and deal with the dynamic demands in time (Györgyi and Kis, 2019; Demirbilek, 2021). Due to the complexity of logistics activities and the high response time requirement of dynamic pickup demands, it is essential to design a reasonable and targeted strategy for dynamic demands combined with pickup and delivery services (Zhang et al., 2020; Du et al., 2023). An anticipatory customer assignment policy and a multi-stage failure-specific processing strategy were designed to guide vehicles in serving dynamic demands (Karami et al., 2020; Zhang et al., 2020). Du et al. (2023) proposed an order dispatching strategy to coordinate the dynamic pickup and delivery demands, which contained priority ranking of order services and adjustment of the current vehicle routes. Jeong and Moon (2024) put forward a reassignment strategy to deal with the dynamism in the PDVRPTWDD. Regardless of which strategy is adopted to handle the dynamic demands in the PDVRPTWDD, the related constraints (e.g., vehicle capacity and time window) need to be properly considered (Demirbilek, 2021; Cai et al., 2022; Simoni and Winkenbach, 2023).

### 2.3. MDPDVRPTW

The MDVRPTW is another significant hot topic (Wang et al., 2020a, b, 2024b). Specifically, the MDVRPTW has been widely studied and indicates that multiple depots (i.e., delivery, pickup, delivery and pickup depots) can provide logistics services (i.e., delivery and pickup goods) for large-scale customers (Zhen et al., 2020; Sadati and Çatay, 2021). Several scholars have demonstrated their achievements on the extension problem composed of the MDVRPTW and PDVRPTW, that is, the MDPDVRPTW. Kocatürk et al. (2021) investigated the MDPDVRPTW, with consideration of heterogeneous fleets. Praxedes et al. (2024) studied the MDPDVRPTW, where the pickup and delivery demands can be met simultaneously on the same route.

Heuristic algorithms were often used to solve the related MDPDVRPTW, such as non-dominated sorting genetic algorithm-II (NSGA-II), multi-objective particle swarm optimization (MOPSO), and multi-objective evolution algorithm (MOEA) (Mamaghani and Davari, 2020; Peng et al., 2019; Wang et al., 2020b; Zou et al., 2021; Wang et al., 2024c). Peng et al. (2019) developed an adaptive MOPSO to minimize the total profit and total travel distance. Mamaghani and Davari (2020) focused on reducing the TOC and penalty cost for time window violations in the PDVRPTW and designed an extended NSGA-II to solve the model. Elite iteration composed of nondominated sorting and crowding-distance sorting is a critical design in the NSGA-II (Srivastava et al., 2021; Wang et al., 2021c). Zou et al. (2021) and Wang et al. (2021a) used the MOEA to find the optimum vehicle routes in the related MDPDVRPTW. A hybrid heuristic algorithm merging the advantages of different algorithms was also commonly proposed to find the Pareto optimal solutions in the MDPDVRPTW (Shi et al., 2022; Kchaou-Boujelben et al., 2023).

### 2.4. MDVRPTW-RS

In a multi-depot logistics network optimization, resource sharing was an important measurement to improve operating efficiency and reduce operating costs (Yang et al., 2020; Zhang et al., 2022; Wang et al., 2024b). Customer resource sharing was considered to arrange vehicle service routes for decreasing operating costs (Gansterer and Hartl, 2018; Fernández et al., 2018). Soeanu et al. (2020) solved a multi-depot vehicle routing problem from a novel perspective, where the transportation risk was mitigated by sharing logistics planning techniques among stakeholders. Zhang et al. (2022) presented a novel problem of MDVRPTW-RS and considered the heterogeneous depots and various products in collaborative logistics networks.

In addition to the cost-saving efficiency of resource sharing for logistics network optimization, the construction of service routes can also benefit from it (Şahin and Yaman, 2022; Zhang et al., 2022; Wang et al., 2024c). Li et al. (2018) optimized the transportation distance and fuel consumption of MDVRPTW-RS, where a vehicle was permitted to start from a depot and finally end at any appropriate depot. Wang et al. (2018) constructed the open-closed service routes to realize the resource sharing among depots. Focus on the MDVRPTW-RS, Wang et al. (2021b) utilized cooperation and resource sharing to split loads and realize vehicles be used jointly among different time periods during a working day. In addition, the resource sharing promoted the construction of vehicles’ service and trucks’ centralized transportation routes in a two-echelon MDVRPTW-RS problem (Liu and Liao, 2021; Li et al., 2023b).

In the related MDVRPTW-RS, clustering algorithms, such as AP clustering algorithm, k-means clustering algorithm, and fuzzy clustering algorithm were widely used to reassign customers in the multi-depot logistics network (Yang et al., 2022; Xu et al., 2023). Specifically, customer clustering can decrease the computational complexity in solving the vehicle routing problem and its extensions (Fan et al., 2021; Liu and Liao, 2021). The geographic location (i.e., longitude and latitude) was commonly used to calculate the similarity matrix in AP clustering algorithm, ignoring the characteristics of time windows in the MDVRPTW-RS (He et al., 2019; Wu et al., 2021).

Table 1 summarizes some relevant literature and their features in the above four subsections.

## 3. Problem statement and model formulation

### 3.1. Problem statement

The real-world urban logistics network contains various types of depots, such as the pickup depots (PDs) and delivery depots (DDs), and each depot carries out the corresponding services according to customer demand characteristics (Meng et al., 2024; Zhou et al., 2024). In this study, a multi-depot network composed of delivery depots, pickup depots, and three types of customers (i.e., static delivery, static pickup, dynamic pickup demands) is considered to investigate the optimization method of the MDPDTWDD. The information of dynamic pickup demands is sent to depots after vehicle service schedules have been designed. Homogeneous vehicles are used for pickup and delivery services between delivery and pickup depots. On the one hand, the open-closed mixed vehicle routes are constructed to integrate vehicle’s pickup and delivery activities. On the other hand, some adjustments are determined on current vehicle schedules on the basis of the insertion strategy to satisfy dynamic demands. Three period optimization states of the MDPDTWDD (i.e., initial, optimization results without performing insertion strategy, optimization results with performing insertion strategy) are shown in Fig. 1(a) and (b), and 1(c), respectively. The objective of this problem is to minimize the total operating cost and number of vehicles in the multi-depot network.

Figure 1: Example of the MDPDTWDD optimization process.

In Fig. 1(a), each depot operates independently. The vehicle service routes are closed because vehicles in the non-collaborative logistics network depart from pickup or delivery depots to only perform pickup or delivery activities, and must return to their origin, which not only limits the efficient use of vehicles but also hinders the integration of pickup and delivery services (Mamaghani and Davari, 2020; Kocatürk et al., 2021). Unreasonable vehicle schedules, such as long-distance service (e.g., V7 travels from PD2 to C4 in Fig. 1(a)) and violations of customer time windows (e.g., C12 and C25 in Fig. 1(a)) are difficult to avoid. New routes and vehicles are directly arranged to serve the dynamic demands.

In Fig. 1(b), each depot operates collaboratively, and vehicles can perform open or closed service routes. Specifically, when the delivery and pickup demands are served by the same vehicle, this vehicle is allowed and required to leave from the delivery depot and stop at a corresponding appropriate pickup depot. For example, vehicle 1 starts from DD1, serves customers C1, C2, C3, C4, C5, C6, C7, C8, and finally stops at PD2. Similarly, in Fig. 1(b), dynamic demands are served by new vehicles on new service routes. In Fig. 1(c), an insertion strategy is introduced on the basis of the collaboration strategy to handle dynamic demands. New vehicles are arranged only if the working vehicles cannot be adjusted to serve dynamic demands.

Some indexes, such as the total travel time of all vehicles (TTT), total time of vehicle arriving early (TAE), total time of vehicle arriving late (TAL), number of vehicles (NVs), travel cost (TC), maintenance cost (MC), penalty cost (PC), insertion cost (IC), TOC, TOC gap, and NV Gap, are counted to make sense of the differences before and after optimization. The measurement units of each index are listed in Table 2, and the comparison results are listed in Table 3.

**Table 2**
Measurement units of relevant indexes.

| Index | Value |
| :--- | :--- |
| TC | $35 per unit time |
| PC | $35 per unit time for early and $55 per unit time for late |
| IC | $10 per quantity of pickup demand |
| MC | $100 per vehicle |

In Table 3, the gaps of NV and TOC in Fig. 1(a) and (b) are 2 and $850, respectively. The gaps of NV and TOC are 4 and $1602.5 before (Fig. 1 (a)) and after (Fig. 1(c)) optimization, respectively. The TTT has been reduced from 72.5 to 50, thereby directly reducing the TC from $2537.5 to $1750. The PC for violating time windows (including TAE and TAL) is decreased from $475 to $0. Meanwhile, the MC is diminished from $900 to $500 and the NV is reduced from 9 to 5. Although the insertion cost of performing the insertion strategy to arrange dynamic demands is $60, the cost saving in TC and MC is evident.

**Table 3**
Comparison before and after optimization.

| Scenario | TTT | TAE | TAL | TC ($) | PC ($) | IC ($) | MC ($) | NV | TOC ($) | Gap NV | Gap TOC ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| a | 72.5 | 2 | 8 | 2537.5 | 475 | 0 | 900 | 9 | 3912.5 | – | – |
| b | 67.5 | 0 | 0 | 2362.5 | 0 | 0 | 700 | 7 | 3062.5 | 2 | 850 |
| c | 50 | 0 | 0 | 1750 | 0 | 60 | 500 | 5 | 2310 | 4 | 1602.5 |

### 3.2. Theorem proof

This section aims to prove that the service integration and resource sharing of pickup and delivery depots can improve the service efficiency of the multi-depot network for dynamic pickup demands. Without loss of generality, a multi-depot network containing one delivery depot and $n$ ($1 \le n \le 2$) pickup depots is taken as an example to prove the effectiveness of resource integration. According to the queuing theory, some reasonable assumptions are as follows:

**Assumption 1.** The pickup and delivery depots operate independently in the non-collaborative network, indicating that the dynamic pickup demands can only be served by their corresponding pickup depots. However, the resources of pickup and delivery depots are integrated in the collaborative network, manifesting that all depots can serve the dynamic pickup demands in the multi-depot network.

**Assumption 2.** The dynamic pickup demand of each pickup depot satisfies a Poisson distribution with arrival rate $\lambda/n$, where $\lambda$ is a constant. Each depot meets a negative exponential distribution with service rate $\mu$, $(\lambda /n) > 0$, $\mu > 0$, $(\lambda /n) < \mu$, $\lambda > 0$.

**Assumption 3.** Two or more depots can form a collaborative alliance by sharing logistics resources. Besides, the service rule of each depot is the first-come-first-served rule.

Based on these assumptions, the service efficiencies of the non-collaborative and collaborative networks are compared in terms of the queue length, as shown below. It’s worthing that in the subsequent proof process, for example, in Eq. (3), $k$ is a variable that is used to help express the calculation method, and has no reality significance.

**Theorem 1.** When the $n$ ($n = 2$) pickup depots form an alliance, the service efficiency of the alliance outperforms that of single pickup depot when they operate without collaboration.

**Proof of Theorem 1.** Based on the Assumption 2, the arrival rate of dynamic pickup demands for the queuing system is equal to $(\lambda /n) \cdot n = \lambda$, and the traffic intensity of this system is $\rho_1 = \lambda/n\mu$. When these pickup depots operate independently, the queue length of each pickup depot is

$$ L_s = \frac{\rho_1 \cdot (\lambda/n)}{\mu - (\lambda/n)} = \frac{\rho_1^2}{(1 - \rho_1)} \tag{1} $$

However, when these pickup depots form an alliance, the queue length of this alliance is

$$
L_a = \frac{(n\rho_1)^n\cdot\rho_1}{n!(1-\rho_1)^2}\cdot P_0
\tag{2}
$$
where the $P_0$ is the state probability that there is no customer in the queuing system, which can be calculated by the following formula

$$ P_0 = \left[ \sum_{k=0}^{n-1} \frac{1}{k!} \cdot \left(\frac{\lambda}{\mu}\right)^k + \frac{1}{n!} \cdot \frac{1}{1 - \rho_1} \cdot \left(\frac{\lambda}{\mu}\right)^n \right]^{-1} = \frac{1 - \rho_1}{1 + \rho_1} \tag{3} $$

By dividing the queue length of the collaborative alliance by the queue length of single pickup depot without collaboration, we can obtain

$$ \frac{L_s}{L_a} = \frac{\rho_1^2}{(1 - \rho_1)} \cdot \frac{n!(1 - \rho_1)^2}{(n\rho_1)^n \cdot \rho_1 \cdot P_0} = \frac{\rho_1 \cdot 2!(1 - \rho_1)}{(2\rho_1)^2} \cdot \frac{1 + \rho_1}{1 - \rho_1} = \frac{1}{2} + \frac{1}{2\rho_1} \tag{4} $$

Due to the $(\lambda /n) < \mu$, the traffic intensity $\rho_1$ is less than 1. Then, with $\rho_1 \to 1$, we can get

$$ \frac{L_s}{L_a} = \frac{1}{2} + \frac{1}{2\rho_1} > 1 \tag{5} $$

Therefore, the collaboration and resource sharing among the $n$ pickup depots can improve service efficiency, and the proof of Theorem 1 is completed.

**Theorem 2.** When the delivery depot and $n$ pickup depots form an alliance, the service efficiency of the alliance is better than that of the non-collaborative network for dynamic pickup demands.

**Proof of Theorem 2.** When $n = 1$, the queuing process of the non-collaborative network conforms to the M/M/1 model, and that of the collaborative network conforms to the M/M/2 model. However, when $n = 2$, the non-collaborative network belongs to the $n$ M/M/1 systems, and the collaborative network satisfies the M/M/3 model. Note that the M/M/2 and M/M/3 models are two cases of the M/M/c model, where $c$ is a variable greater than 1. Due to the difference of used model, the following are discussed in two cases.

**Case 1.** ($n = 1$): when the two depots (i.e., pickup and delivery depots) operate independently, the traffic intensity $\rho_2 = \lambda/\mu$. The queue length of the logistic network is

$$ L'_s = \frac{\rho_2 \cdot \lambda}{\mu - \lambda} = \frac{(\rho_2)^2}{1 - \rho_2} \tag{6} $$

When the two depots operate together, the traffic intensity $\rho_3 = \lambda/2\mu = \rho_2/2$, and the state probability $P'_0$ is

$$ P'_0 = \left[ \sum_{k=0}^{(n+1)-1} \frac{1}{k!} \cdot \left(\frac{\lambda}{\mu}\right)^k + \frac{1}{(n+1)!} \cdot \frac{1}{1 - \rho_3} \cdot \left(\frac{\lambda}{\mu}\right)^{n+1} \right]^{-1} = \frac{2 - \rho_2}{2 + \rho_2} \tag{7} $$

Then, the queue length of the current alliance is

$$ L'_a = \frac{[(n+1)\rho_3]^{n+1} \cdot \rho_3}{(n+1)!(1 - \rho_3)^2} \cdot P'_0 = \frac{(\rho_2)^3 \cdot (2 - \rho_2)}{4 \cdot [1 - (\rho_2/2)]^2 \cdot (2 + \rho_2)} \tag{8} $$

By subtracting the queue lengths of the logistics network with and without collaboration, we can obtain:

$$ L'_s - L'_a = \frac{(\rho_2)^2}{1 - \rho_2} - \frac{(\rho_2)^3 \cdot (2 - \rho_2)}{4 \cdot [1 - (\rho_2/2)]^2 \cdot (2 + \rho_2)} = \frac{(\rho_2)^2 \cdot [(\rho_2 - 3)^2 - 1]}{4 \cdot (1 - \rho_2) \cdot [1 - (\rho_2/2)]^2 \cdot (2 + \rho_2)} \tag{9} $$

Due to $\mu > \lambda > 0$, we can get $0 < \rho_2 < 1$. Thus, the $4 \cdot (1 -\rho_2) \cdot [1 -(\rho_2/2)]^2 \cdot (2 + \rho_2) > 0$. Besides, when $\rho_2 \to 1$, the minimum value of $(\rho_2 -3)^2 -1$ is greater than zero. Therefore, the $L'_s - L'_a > 0$.

**Case 2.** ($n = 2$): when only two pickup depots integrate their resources, the traffic intensity $\rho_4 = \rho_1 = \lambda/2\mu$, and the state probability $P''_0$ and queue length $L''_s$ are

$$ P''_0 = P_0 = \frac{1 - \rho_1}{1 + \rho_1} \tag{10} $$

$$ L''_s = L_a = \frac{(n\rho_1)^n \cdot \rho_1}{n!(1 - \rho_1)^2} \cdot P_0 = \frac{2(\rho_1)^3}{1 - (\rho_1)^2} \tag{11} $$

When the delivery depot collaborates with the two pickup depots, the traffic intensity $\rho_5 = \lambda/3\mu = 2\rho_1/3$, and the state probability $P'''_0$ and queue length $L''_a$ are

$$ P'''_0 = \left[ \sum_{k=0}^{(n+1)-1} \frac{1}{k!} \cdot \left(\frac{\lambda}{\mu}\right)^k + \frac{1}{(n+1)!} \cdot \frac{1}{1 - \rho_5} \cdot \left(\frac{\lambda}{\mu}\right)^{n+1} \right]^{-1} = \frac{3 - 2\rho_1}{3 + 4\rho_1 + 2(\rho_1)^2} \tag{12} $$

$$ L''_a = \frac{[(n+1)\rho_5]^{n+1} \cdot \rho_5 \cdot P'''_0}{(n+1)!(1 - \rho_5)^2} = \frac{8(\rho_1)^4}{(3 - 2\rho_1)[3 + 4\rho_1 + 2(\rho_1)^2]} \tag{13} $$

By subtracting the queue length of collaborative logistics network from that of the non-collaborative logistics network, we can get

$$ L''_s - L''_a = \frac{2(\rho_1)^3}{1 - (\rho_1)^2} - \frac{8(\rho_1)^4}{(3 - 2\rho_1)[3 + 4\rho_1 + 2(\rho_1)^2]} = \frac{2(\rho_1)^3 \cdot [9 + 2\rho_1 - 2(\rho_1)^2]}{[1 - (\rho_1)^2] \cdot (3 - 2\rho_1) \cdot [3 + 4\rho_1 + 2(\rho_1)^2]} \tag{14} $$

Due to $0 < \rho_1 < 1$, when the $\rho_1 \to 1$, we can obtain $[1 - (\rho_1)^2] \cdot (3 - 2\rho_1) \cdot [3 + 4\rho_1 + 2(\rho_1)^2] > 0$. Besides, $9 + 2\rho_1 - 2(\rho_1)^2$ is a quadratic function with an opening downward. When $\rho_1 \to 1$ or $\rho_1 \to 0$, the function $9 + 2\rho_1 - 2(\rho_1)^2$ can obtain minimum value 9. Thus, the $2(\rho_1)^3 \cdot [9 + 2\rho_1 - 2(\rho_1)^2] > 0$, and $L''_s - L''_a > 0$.

The above proof process of Case 2 manifests that the service efficiency of the collaborative network outperforms the service efficiency of the alliance containing only two pickup depots. In addition, Theorem 1 proves that the service efficiency of the alliance is better than the service efficiency of single pickup depot in the non-collaborative network. Therefore, the service efficiency of the collaborative network exceeds that of the non-collaborative network, and the proof of Case 2 is completed.

In conclusion, the proofs of above two cases indicate that the resource sharing among delivery and pickup depots can improve service efficiency for dynamic pickup demands, and the proof of Theorem 2 is completed.

### 3.3. Assumptions and definitions

Based on the theorems in Section 3.2, resource sharing among delivery and pickup depots is considered in modeling MDPDTWDD. In addition, the nature of dynamic demands in this study is stochastic because the planner does not know in advance (when planning the static demands) when the dynamic pickup demands arrive. To narrow the discrepancy between the theory and practice, several reasonable assumptions are indispensable and described as follows (Li et al., 2018; Györgyi and Kis, 2019; Dubey and Tanksale, 2023):

**Assumption 4.** Three types of customer demands are considered, including static delivery, static pickup, and dynamic pickup demands.

**Assumption 5.** The data of customers with static demands are known and stable at least in one working day. The data of dynamic demands are presented after depots begin working during one working day. Each dynamic demand cannot be postponed for service and should be satisfied by arranging a new service route or inserting into an on-working service route.

**Assumption 6.** Vehicles are collaboratively deployed by depots, where vehicles can start from one depot and end at other depots, furthermore, one vehicle can be used for pickup and delivery services on the same route.

Notations and their descriptions used in modeling MDPDTWDD are listed in Table 4 (Guajardo et al., 2018; Asghari and Al-e-hashem, 2020).

**Table 4**
Notations in modeling MDPDTWDD.

| Notations              | Descriptions                                                                                                                                                                         |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sets**               |                                                                                                                                                                                      |
| $R$                    | Set of customers with static delivery demands, $R = \{\, i \mid i = 1, 2, 3, \dots, n_1 \,\}$, where $n_1$ is the total number of customers in $R$                                               |
| $S$                    | Set of customers with static pickup demands, $S = \{j = 1, 2, 3, \dots, n_2\}$, where $n_2$ is the total number of customers in $S$                                                  |
| $D$                    | Set of customers with dynamic pickup demands, $D = \{k = 1, 2, 3, \dots, n_3\}$, where $n_3$ is the total number of customers in $D$                                                 |
| $C$                    | Set of customers, $C = R \cup S \cup D$                                                                                                                                              |
| $V$                    | Set of vehicles, $V = \{v = 1, 2, 3, \dots, n_v\}$, where $n_v$ is the total number of vehicles                                                                                      |
| $W$                    | Set of DDs, $W = \{w = 1, 2, 3, \dots, n_w\}$, where $n_w$ is the total number of DDs                                                                                                |
| $O$                    | Set of PDs, $O = \{o = 1, 2, 3, \dots, n_p\}$, where $n_p$ is the total number of PDs                                                                                                |
| $F$                    | Set of DDs and PDs, $F = W \cup O$                                                                                                                                                   |
| **Parameters**         |                                                                                                                                                                                      |
| $[l_i, r_i]$           | Time windows of customer or depot $i$, $i \in C \cup F$                                                                                                                              |
| $Q_i$                  | Delivery quantity of customer $i$, $i \in C$                                                                                                                                         |
| $P_i$                  | Pickup quantity of customer $i$, $i \in C$                                                                                                                                           |
| $\partial_v$           | Capacity of vehicle $v$, $v \in V$                                                                                                                                                   |
| $\alpha_v$             | Travel speed of vehicle $v$, $v \in V$                                                                                                                                               |
| $f_v$                  | Fuel consumption rate per mile of vehicle $v$, $v \in V$                                                                                                                             |
| $p_v$                  | Fuel price per liter of vehicle $v$, $v \in V$                                                                                                                                       |
| $M_v$                  | Annual maintenance cost of vehicle $v$, $v \in V$                                                                                                                                    |
| $C_f$                  | Capacity of depot $f$, $f \in F$                                                                                                                                                     |
| $\beta_f$              | Fixed cost per working day of depot $f$, $f \in F$                                                                                                                                   |
| $T$                    | Number of working days per year                                                                                                                                                      |
| $d_{ij}$               | Distance between customers or depots $i$ and $j$, $i, j \in C \cup F$                                                                                                                |
| $t_{ij}$               | Travel time between customers or depots $i$ and $j$, $i, j \in C \cup F$                                                                                                             |
| $\varepsilon$          | Penalty coefficient per hour for early arrival                                                                                                                                       |
| $\omega$               | Penalty coefficient per hour for late arrival                                                                                                                                        |
| $\delta$               | Cost coefficient per delivery quantity                                                                                                                                               |
| $\chi$                 | Cost coefficient per pickup quantity                                                                                                                                                 |
| $\gamma$               | Insertion coefficient per dynamic pickup quantity                                                                                                                                    |
| $\tau$                 | A very large number                                                                                                                                                                  |
| $A_{vi}$               | Arriving time of vehicle $v$ at customer or depot $i$, $v \in V, i \in C \cup F$                                                                                                     |
| $B_v$                  | Time when vehicle $v$ begins to provide service for customers when it leaves from depot, $v \in V$                                                                                   |
| $B^v$                  | Time when vehicle $v$ ends its whole tasks and finally stops at depot, $v \in V$                                                                                                     |
| $N_{vj}$               | Quantities that need vehicle $v$ to delivery when it leaves customer $j$, $v \in V, j \in C$                                                                                         |
| $P_{vj}$               | Quantities that have been picked up by vehicle $v$ when it leaves from customer $j$, $v \in V, j \in C$                                                                              |
| $N_{vij}$              | Quantities that loaded on vehicle $v$ when it leaves from customer or depot $i$ to $j$, $v \in V, i, j \in C$                                                                        |
| **Decision variables** |                                                                                                                                                                                      |
| $x_{ij}^v$             | 1, if vehicle $v$ travels from customer or depot $i$ to $j$; 0, otherwise, $v \in V, i, j \in C \cup F$                                                                              |
| $x_{ikj}^v$            | 1, if customer $k$ is inserted in the middle service position between customers or depots $i$ and $j$ and served by vehicle $v$; 0, otherwise, $v \in V, k \in D, i, j \in C \cup F$ |
| $y_{if}^v$             | 1, if customer $i$ is served by vehicle $v$ that departs from depot $f$; 0, otherwise, $i \in C, v \in V, f \in F$                                                                   |
| $y_{f}^v$              | 1, if vehicle $v$ ends at depot $f$; 0, otherwise, $v \in V, f \in F$                                                                                                                |

### 3.4. Mathematical model

With the aforementioned assumptions and notations, the MDPDTWDD is formulated as a bi-objective mathematical model to minimize the TOC and NV. Eqs. (15) and (16) show the specific formulations of TOC and NV (Wong et al., 2018). The TOC (Eq. (15)) is composed of travel cost (TC, Eq. (17)), penalty cost (PC, Eq. (18)), maintenance cost (MC, Eq. (19)), insertion cost (IC, Eq. (20)), and fixed cost (FC, Eq. (21)). The related constraints are exhibited in Eqs. (22)–(48) (Li et al., 2018; Ouertani et al., 2020). The specific bi-objective mathematical model of the MDPDTWDD is stated as follows:

$$
\min{TOC} = TC + PC + MC + IC + FC
\tag{15}
$$

$$
\min{NV} = \sum_{v\in V}\sum_{i\in F}\sum_{j\in C} x_{ij}^{v}
\tag{16}
$$

$$
TC = \sum_{v\in V}\sum_{i\in C\cup F}\sum_{j\in (C\cup F)\setminus\{i\}} f_v\cdot p_v\cdot x_{ij}^{v}\cdot d_{ij}
\tag{17}
$$

$$
PC = \sum_{v\in V}\sum_{i\in C}\left(\varepsilon\cdot \max\{l_i-A_{vi},0\} + \omega\cdot \max\{A_{vi}-r_i,0\}\right)
\tag{18}
$$

$$
MC = \sum_{v\in V}\sum_{i\in F}\sum_{j\in C} \frac{M_v\cdot x_{ij}^{v}}{T}
\tag{19}
$$

$$
IC = \sum_{i\in D}\sum_{f\in F}\sum_{v\in V} y_{if}^{v}\cdot P_i\cdot \gamma
\tag{20}
$$

$$
FC
=
\sum_{f\in F}\beta_f
+
\delta\cdot\sum_{i\in R}\sum_{f\in F}\sum_{v\in V} y_{if}^{v}\cdot Q_i
+
\chi\cdot\sum_{i\in S\cup D}\sum_{f\in F}\sum_{v\in V} y_{if}^{v}\cdot P_i
\tag{21}
$$

Constraints of initial route optimization:

$$
\sum_{f\in F}\sum_{v\in V} y_{if}^{v} = 1,\ \forall i\in C\setminus D
\tag{22}
$$

$$
\sum_{i\in F}\sum_{j\in C\setminus D} x_{ij}^{v}
-
\sum_{i\in C\setminus D}\sum_{j\in F} x_{ij}^{v}
= 0,\ \forall v\in V
\tag{23}
$$

$$
\sum_{i\in R} y_{if}^{v}\cdot Q_i \le \partial_v,\ \forall f\in W,\ v\in V
\tag{24}
$$

$$
\sum_{i\in S} y_{if}^{v}\cdot P_i \le \partial_v,\ \forall f\in O,\ v\in V
\tag{25}
$$

$$
N_{vj}+P_{vj} = \left(\sum_{i\in C\setminus D} x_{ij}^{v}\cdot N_{vij}\right) - Q_j,\ \forall v\in V,\ j\in R
\tag{26}
$$

$$
N_{vj}+P_{vj} = \left(\sum_{i\in C\setminus D} x_{ij}^{v}\cdot N_{vij}\right) + P_j,\ \forall v\in V,\ j\in S
\tag{27}
$$

$$
N_{vj}+P_{vj} \le \partial_v,\ \forall v\in V,\ j\in C\setminus D
\tag{28}
$$

$$
x_{ij}^{v} - \sum_{f\in W} y_{if}^{v} = 0,\ \forall v\in V,\ i\in R,\ j\in C\setminus D
\tag{29}
$$

$$
x_{ij}^{v} - \sum_{f\in O} y_{f}^{v} = 0,\ \forall v\in V,\ i\in S,\ j\in C\setminus D
\tag{30}
$$

$$
l_f \le B_v - \tau\cdot (y_{if}^{v}-1),\ \forall v\in V,\ i\in C\setminus D,\ f\in F
\tag{31}
$$

$$
B_v - \tau\cdot(1-x_{ij}^{v}) \le r_j - \frac{d_{ij}}{\alpha_v},\ \forall v\in V,\ i\in F,\ j\in C\setminus D
\tag{32}
$$

$$
l_j - \frac{d_{ij}}{\alpha_v} \le B_v + \tau\cdot(1-x_{ij}^{v}),\ \forall v\in V,\ i\in F,\ j\in C\setminus D
\tag{33}
$$

$$
A_{vi} + \frac{d_{ij}}{\alpha_v} - \tau\cdot(1-x_{ij}^{v}) \le r_j,\ \forall v\in V,\ i,j\in (C\setminus D)\cup F
\tag{34}
$$

$$
l_j \le A_{vi} + \frac{d_{ij}}{\alpha_v} + \tau\cdot(1-x_{ij}^{v}),\ \forall v\in V,\ i,j\in (C\setminus D)\cup F
\tag{35}
$$

$$
B^v - \tau\cdot(1-y_{f}^{v}) \le r_f,\ \forall v\in V,\ f\in F
\tag{36}
$$

$$
B^v = B_v + \sum_{i\in F\cup(C\setminus D)}\sum_{j\in (C\setminus D)\cup(F\setminus\{i\})}\frac{d_{ij}}{\alpha_v}\cdot x_{ij}^{v},\ \forall v\in V
\tag{37}
$$

$$
\sum_{i\in C\setminus D}\sum_{j\in (R\cup S)\setminus\{i\}} x_{ij}^{v}
\le
\sum_{i\in C\setminus D} y_{if}^{v} - 1,\ \forall v\in V,\ f\in F
\tag{38}
$$

Constraints of dynamic route adjustment:

$$
\sum_{v\in V}\sum_{i\in F\cup C}\sum_{j\in F\cup C} x_{ikj}^{v} = 1,\ \forall k\in D
\tag{39}
$$

$$
\sum_{i\in F\cup C} x_{ik}^{v} - \sum_{j\in F\cup C} x_{kj}^{v} = 0,\ \forall k\in D,\ v\in V
\tag{40}
$$

$$
\sum_{i\in S\cup D} y_{if}^{v}\cdot P_i \le \partial_v,\ \forall f\in O,\ v\in V
\tag{41}
$$

$$
\left(N_{vij}+P_k\right)\cdot x_{ikj}^{v} \le \partial_v,\ \forall v\in V,\ k\in D,\ i,j\in C\cup F
\tag{42}
$$

$$
x_{ij}^{v} - \sum_{f\in W} y_{if}^{v} = 0,\ \forall v\in V,\ i\in R,\ j\in C
\tag{43}
$$

$$
x_{ij}^{v} - \sum_{f\in O} y_{f}^{v} = 0,\ \forall v\in V,\ i\in S\cup D,\ j\in C
\tag{44}
$$

$$
A_{vi} + \frac{d_{ik}}{\alpha_v} - \tau\cdot(1-x_{ikj}^{v}) \le r_k,\ \forall v\in V,\ k\in D,\ i,j\in C\cup F
\tag{45}
$$

$$
l_k \le A_{vi} + \frac{d_{ik}}{\alpha_v} + \tau\cdot(1-x_{ikj}^{v}),\ \forall i,j\in C\cup F,\ k\in D,\ v\in V
\tag{46}
$$

$$
B^v = B_v + \sum_{i\in C\cup F}\sum_{j\in (C\cup F)\setminus\{i\}}\frac{d_{ij}}{\alpha_v}\cdot x_{ij}^{v},\ \forall v\in V
\tag{47}
$$

$$
\sum_{i\in D}\sum_{j\in D\setminus\{i\}} x_{ij}^{v}
\le
\sum_{i\in D} y_{if}^{v} - 1,\ \forall v\in V,\ f\in F
\tag{48}
$$

Constraint (22) guarantees that each customer with static demands is visited only once by exactly one vehicle. Constraint (23) states that each vehicle cannot stop outside the depot. Constraints (24)–(28) assure that the goods quantities loaded on vehicles at each node do not exceed the capacity of vehicle. Constraints (29)–(30) determine the origin and destination of each route. Constraints (31)–(33) require that each vehicle departs within the time window of the corresponding depot. Constraints (34)–(35) indicate that vehicles are required to visit customers within their time windows. Constraints (36)–(37) assure that the return time of each vehicle does not exceed the depot’s time window. Constraint (38) eliminates the sub-tours of the routes for static demands. Constraint (39) ensures that each customer with dynamic pickup demand is only served once. Constraint (40) states the flow conservation at each customer with dynamic pickup demand. Constraints (41)–(42) guarantee that the loading status satisfies the vehicle’s capacity after route adjustment. Constraints (43)–(44) reassure the origin and destination of each route after arranging for dynamic demands. Constraints (45)–(46) are formulated to judge whether the service time is appropriate to insert dynamic demands based on time windows. Constraint (47) updates the return time for each vehicle after adjusting routes. Constraint (48) represents the elimination of sub-tours for the new routes for dynamic demands.

Binary decision constraints:
$x_{ij}^v = \{0, 1\}, \forall v \in V, i, j \in C \cup F$
$x_{ikj}^v = \{0, 1\}, \forall v \in V, i, j \in C \cup F, k \in D$
$y_{if}^v = \{0, 1\}, \forall i \in C, f \in F, v \in V$
$y_{f}^v = \{0, 1\}, \forall v \in V, f \in F$

## 4. Solution methodology

### 4.1. Two-stage hybrid algorithm

A two-stage hybrid algorithm composed of 3D AP clustering algorithm and ANSGA-II is developed to solve the MDPDTWDD. The elite iteration (including genetic operation, local search, and Pareto optimal) and dynamic insertion strategy are integrated and formed the ANSGA-II (Asghari and Al-e-hashem, 2020; Niu et al., 2021; Wang et al., 2022a). The symbols related to the 3DAPANSGA-II are listed in Table 5 and its flow chart is shown in Fig. 2.

In Fig. 2, the 3D AP clustering algorithm and ANSGA-II are executed to find the Pareto optimal solutions. The internal and interactional mechanisms of these parts push each other forward to update the found optimal solutions. Each process plays an indispensable role in the 3DAPANSGA-II, and the specific designs of the critical parts are explained as follows.

**Table 5**
Symbols and its descriptions related to 3DAPANSGA-II.

| Symbols     | Descriptions                                                  | Symbols             | Descriptions                                                     |
| :---------- | :------------------------------------------------------------ | :------------------ | :--------------------------------------------------------------- |
| $m$         | The current iteration number of 3D AP clustering              | $t$                 | Temporal distance’s coefficient                                  |
| $M$         | The maximum iteration number of 3D AP clustering              | $N_{IND}$           | Population size                                                  |
| $run$       | The current iteration number of elite iteration               | $L$                 | Length of chromosome                                             |
| $Run$       | The maximum iteration number of elite iteration               | $P$                 | Parent population                                                |
| $gen$       | The current iteration number of hybrid algorithm              | $F$                 | Offspring population                                             |
| $M_{gen}$   | The maximum iteration number of hybrid algorithm              | $NP$                | New population merged by P and F                                 |
| $gbest$     | Optimal solution                                              | $m_p$               | Mutation probability                                             |
| $R_{Lg}$    | A threshold used to determine whether to execute local search | $c_p$               | Crossover probability                                            |
| $S_{gbest}$ | A matrix used to store gbest of each iteration                | $i, L_{p1}, L_{p2}$ | Positive integers                                                |
| $n_{gbest}$ | The new gbest after executing the local search operator       | $c_{mp}$            | A random decimal                                                 |
| $R$         | Responsibility matrix                                         | $R_r$               | Remaining routes after removing some customers                   |
| $A$         | Availability matrix                                           | $v_n$               | Number of current vehicles                                       |
| $C_n$       | Number of customers in the current database                   | $Z$                 | A matrix used to storage feasible solutions                      |
| $\lambda'$  | Damping coefficient                                           | $Z_n$               | Number of existing feasible solutions saved in M                 |
| $s_{ij}$    | Similarity value between customers $i$ and $j$                | $R_{m+1}$           | Responsibility matrix in the m+1st iteration of 3D AP clustering |
| $s$         | Spatial distance’s coefficient                                | $A_{m+1}$           | Availability matrix in the m+1st iteration of 3D AP clustering   |
| $p$         | Sequence number of the chromosome                             |                     |                                                                  |

### 4.2. 3D AP clustering algorithm

The 3D AP clustering algorithm considers the characteristics of customers’ geographic locations and time windows to lower the computational complexity, and groups customers based on the messages (i.e., responsibility matrix marked with R and availability matrix marked with A) transmission among nodes (Liu et al., 2020; Wu et al., 2021). Fig. 3 presents an example of messages transmitted between R and A. This mechanism assumes that nodes $i, i', j$, and $j'$ represent customers/depots, and $R(i,j)$ and $A(i,j)$ are the values of responsibility and availability between nodes $i$ and $j$.

In Fig. 3(a), the $R(i,j)$ represents the accumulated information on how suitable node $j$ is as an exemplar for node $i$ with consideration of the other potential exemplars marked with node $j'$. In Fig. 3(b), the $A(i,j)$ shows the accumulated information on how appropriate it is for node $j$ to select node $i$ as its exemplar on comparing with selecting other nodes marked $i'$. The pseudocode of the 3D AP clustering algorithm is illustrated in Table 6.

Figure 2: Flow chart of 3DAPANSGA-II.
Figure 3: Message transportation in the 3D AP clustering algorithm.

**Table 6**
Pseudocode of the 3D AP clustering algorithm.

```pseudocode
Input: Database including d DDs, p PDs and Cn customers, parameters such as λ′, M
Output: Customer clusters
1 Initialize clustering centers with depots
2 Calculate the space-time distance between any two nodes
3 Generate the similarity matrix based on the space-time distance and set m = 1
4 Initialize responsibility matrix R and availability matrix A
5 While m ≤ M do
6     Calculate Rm
7     Calculate Am
8     Update Rm and Am by λʹ
9     Assign Cn customers to cluster centers with the value of Rm and Am
10    Update clusters and cluster centers
11    m = m+1
12    If cluster centers are not changed
13        Break;
14    End if
15 End while
16 Update cluster results
```

Meanwhile, three elements are critical during the clustering process. First, the space-time distance is used to generate the similarity matrix. Eq. (49) shows the specific calculation method of the space-time distance between nodes $i$ and $j$. Second, matrices $R_{m+1}$ (shown in Eq. (50)) and $A_{m+1}$ (shown in Eq. (51)), which determine the message transportation, are calculated. Third, the update mechanisms of $R_{m+1}$ and $A_{m+1}$ (shown in Eq. (52) and Eq. (53)) by adopting the damping coefficient $\lambda'$, which ensure the fluctuation range of $R$ and $A$.

$$STD_{ij} = s \cdot d_{ij} + t \cdot \min \{ |l_i - l_j|, |l_i - r_j|, |r_i - l_j|, |r_i - r_j| \} \cdot \alpha_v, \forall i, j \in C \cup F, v \in V \tag{49}$$

$$R_{m+1}(i,j) = S(i,j) - \max_{j' \ne j} \{\, A_m(i,j') + S(i,j') \,\} \tag{50}$$

$$ 
\begin{equation}
A_{m+1}(i,j)=
\begin{cases}
\min \left\{ 0,\; R_m(j,j)+\sum_{j' \notin \{i,j\}} \max \{0, R_m(j',j)\} \right\}, & \forall i,j \in C \cup F,\; i \neq j, \\[4pt]
\sum_{j' \neq j} \max \{0, R_m(j',j)\}, & \forall i,j \in C \cup F,\; i = j .
\end{cases}
\tag{51}
\end{equation}
$$

$$ R_{m+1}(i, j) = \lambda' \cdot R_m(i, j) + (1 - \lambda') \cdot R_{m+1}(i, j) \tag{52} $$

$$ A_{m+1}(i, j) = \lambda' \cdot A_m(i, j) + (1 - \lambda') \cdot A_{m+1}(i, j) \tag{53} $$

As shown in Eq. (49), $STD_{ij}$ is composed of space and time distances in a linearly weighted way. In Eq. (50), $R_{m+1}(i,j)$ describes the suitability of node $j$ as the clustering center for node $i$. In Eq. (51), $A_{m+1}(i,j)$ represents the suitability of node $i$ to select node $j$ as its clustering center. In Eqs. (52) and (53), the introduction of $\lambda'$ prevents drastic fluctuations in $R_{m+1}$ and $A_{m+1}$.

### 4.3. Elite iteration

In the designed elite iteration, three types of operations, including the genetic operation, the elite selection operation for Pareto optimal solutions, and the local search operation, are integrated into a comprehensive body. At the beginning of each elite iteration, genetic operation is performed to improve the population diversity (Asghari and Al-e-hashem, 2020). Next, the elite selection operations, such as nondominated sorting and crowding-distance sorting, are performed to form the offspring population (Zhu and Sheu, 2018; Srivastava et al., 2021). Finally, a local search operator is executed to escape to local optimal solutions (Karami et al., 2020; Zhao et al., 2021). The specific operation processes of genetic operation, local search operator, and Pareto optimal solution are presented in following subsections.

#### 4.3.1. Genetic operation

The population is randomly initialized as dispersed as possible throughout the entire solution space to amplify and enrich the population’s diversity at the beginning of the iteration (Srivastava et al., 2021). Table 7 shows the pseudocode of population initialization. Meanwhile, genetic operations, including selection, crossover, and mutation are developed in ANAGA-II to ensure the diversity of the solution space (Asghari and Al-e-hashem, 2020). The fitness value formulated by TOC and NV plays a crucial role during the selection (Eq. (54)).

Table 7
Pseudocode of population initialization.

```pseudocode
Input: Cluster results, L
Output: Population
1 p = 1
2 While p ≤ NIND do
3     Randomize the pth chromosome of population based on the clustering results and L
4     p = p+1
5 End while
```

$$ fit = \frac{1}{\frac{TOC}{TOC_{max}} + \frac{NV}{NV_{max}}} \tag{54} $$

In Eq. (54), $TOC_{max}$ and $NV_{max}$ are the maximum values of TOC and NV in the current population. The solution with the greater value of $fit$ is more likely to be selected for crossover and mutation. Several ways, such as order crossover, position-based crossover, and partial-mapped crossover (PMX) are available for crossover (Mamaghani and Davari, 2020; Srivastava et al., 2021). The PMX is adopted to stimulate the population’s diversity on account of computation speed and effect. Specifically, two solutions named chromosomes 1 and 2, are regarded as parents, and offsprings 1 and 2 are regarded as their children. The process of PMX is demonstrated in Fig. 4.

Figure 4: PMX operation process.

In Fig. 4, gene parts 9-7-3-1 and 2-1-9-4 are selected to perform a crossover in Step 1. In Step 2, some genes are duplicated or deleted on the current chromosome (i.e., genes 4 and 3 in m_chrom 1) after changing gene parts with each parent. The gene mapping relationship is presented according to selected gene parts to ensure the gene integrity in the chromosome. In Step 3, the mapping relationship of 9-7-3-1 and 2-1-9-4 is transitive and sequential and exists among genes 2, 9, and 3. Accordingly, the first gene 4 in m_chrom 1 is replaced by gene 1 and then by gene 7. The second gene 2 is replaced by gene 3, and m_chrom 1 is updated into offspring 1. After the crossover, mutation is another operation to prompt population’s diversity. The pseudocode of mutation is shown in Table 8.

Table 8
Pseudocode of mutation.

```pseudocode
Input: Population, mp, NIND
Output: Population
1 Set p = 1
2 While p ≤ NIND, do
3     Generate a random decimal cmp and cmp < 1
4     If cmp < mp, do
5         Generate two random positive integers Lp1 and Lp2, where Lp1 ≤ L and Lp2 ≤ L
6         Exchange genes at position Lp1 and Lp2 on the chromosome p
7         Update chromosome p
8     End if
9     p = p+1
10 End while
11 Update population
```

A formula (Eq. (55)) is designed to update $mp$ according to the iteration situation for reducing the influence of $mp$ on finding optimal solutions in the later stages of iteration.

$$
mp = mp\cdot\left(1-\frac{gen}{M_{gen}}\right)
\tag{55}
$$

Eq. (55) indicates that the value of $mp$ is larger at the beginning of the iteration and it approaches zero when $gen$ close to $M_{gen}$. In the early stage of iteration, a larger value of $mp$ facilitates inspiring population diversity. Meanwhile, when $gbest$ approaches the optimum solution, a slight disturbance in $mp$ is more suitable for updating the optimal solution.

#### 4.3.2. Local search operator

A local search operator is developed to avoid falling into a local optimal solution, in which the destroy and repair actions are interactively iterated to stimulate the current solution to be updated (Zhu and Sheu, 2018; Asghari and Al-e-hashem, 2020). Fig. 5 demonstrates the operations of the destroy and repair actions.

Figure 5: Example of destroy and repair actions.

During the destroy process (Fig. 5(a)), the first removed customer (i.e., customer 1) is randomly selected, and the similarity values between other customers and customer 1 are calculated. Then, according to the preset number of removed customers $R_c$, the customers (i.e., customers 2, 3, 4) with higher similarity values are selected for removal. During the repair process (Fig. 5(b)), removed customers 1, 2, 3, and 4 are reinserted into the vehicle routes. Eq. (56) shows the calculation of similarity value $s_{ij}$ between customers $i$ and $j$ (Zhu and Sheu, 2018).

$$ s_{ij} = \frac{1}{x_{ij}^v + \frac{d_{ij}}{\max\{d_{ij}\}}}, \forall v \in V, i, j \in C \tag{56} $$

Eq. (56) indicates that the similarity value between customers mainly depends on their distance and whether they are served on the same route before removing. Table 9 shows the pseudocode of local search operation.

Table 9
Pseudocode of local search operation.

```pseudocode
Input: Population, gbest, RLg, Rc
Output: Population, gbest
1 If gbest hasn’t changed in RLg times consecutive iterations, do
2     For gbest
3         Select a random customer as the first one to be removed
4         Calculate the similarity value between this customer and other customers
5         Select Rc customers to remove according similarity value and generate Rr
6         Re-inserting those Rc customers in Rr and then generate ngbest
7         If ngbest is outperformance than gbest, do
8             gbest = ngbest
9         End if
10        Update the population and gbest
11    End for
12 End if
```

#### 4.3.3. Pareto optimal solution

Nondominated sorting and crowding distance sorting are the major advantages of ANSGA-II, and the generated Pareto optimal solution depends on these operations (Mamaghani and Davari, 2020; Srivastava et al., 2021). First, the $N_{IND}$ individuals existing in populations P and F are merged into a population N, so the population N contains 2*$N_{IND}$ individuals. Second, the nondominated sorting is performed to classify the dominated levels of individuals in the population N, and then the population N is divided into multiple fronts $P_i$ ($i = 1,2,3, \dots, n$), where the individuals in front $P_1$ are definitely better than those in front $P_2$. Without loss of generality, the individuals in front $P_n$ are defined as the worst solutions. Third, the fronts are added into the new population NP successively, according to the dominated rank. When the front $P_m$ ($1 \le m \le n$) is placed into NP, the size of NP is exceeded, and then the crowding distance sorting is performed on the front $P_m$. Finally, partial solutions of $P_m$ are selected and added into NP. Fig. 6 illustrates the selection of Pareto optimal solution in the front $P_m$ through crowding distance sorting.

Figure 6: Crowding distance and Pareto optimal solution selection.

In Fig. 6, four individuals in the same front $P_m$, and in order to improve population diversity, the one with greater crowding distance is preferentially selected. The crowding distance of an individual can be calculated by the objective values of two individuals who are closest to that individual. Fig. 6 takes the individuals 2 and 3 as examples. The crowding distance of individual 2 is equal to the circumference of the blue rectangle with individuals 1 and 3 as vertices. Similarly, the circumference of the red rectangle represents the crowding distance of individual 3. By comparing the crowding distances of individuals 2 and 3, the crowding distance of individual 2 is greater than that of individual 3, so individual 2 is selected. Table 10 shows the nondominated and crowding distance sorting pseudocode.

Table 10
Pseudocode of nondominated and crowding distance sorting.

```pseudocode
Input: P and F
Output: NP and gbest
1 Generate N by merging P and F
2 Generate an empty population NP
3 For each individual of population N
4     Calculate objective values
5 End for
6 Execute nondominated sorting on N to generate fronts Pi (i = 1,2,3, …, n)
7 For i = 1:n
8     Add Pi into the population NP
9     If the size of NP is exceeded, do
10        Record the current sequence number i
11        Break
12    End if
13    Update the population NP
14 End for
15 Execute crowding distance sorting for Pi
16 Perform the optimal solution selection for Pi
17 Add the selected solutions of Pi into the NP
18 Update the population NP
19 Update optimal solution gbest
```

### 4.4. The insertion strategy for dynamic demands

The dynamic demand information is commonly sent out after vehicles depart from depots during the working day (Soeffker et al., 2021; Ulmer et al., 2021). Some adjustments must be carried out on the on-working vehicles to schedule the appropriate service routes for dynamic demands (Seyyedhasani and Dvorak, 2018; Karami et al., 2020). Accordingly, an insertion strategy composed of three types of insertion scenarios is proposed to deal with the emerging dynamic pickup demands by inserting them into the on-working service route or assigning a new vehicle to serve them (Zhu and Sheu, 2018; Wang et al., 2022b). The insertion strategy operation is visualized in Fig. 7.

Figure 7: The insertion strategy for dynamic pickup demands.

In Fig. 7, the insertion strategy is applied to evaluate whether the dispatched vehicles (i.e., Vehicles 1, 2, 3 in Fig. 7(a)) can satisfy the dynamic pickup demands in terms of route adjustment, and then the three insertion scenarios can occur (shown in Fig. 7(b), (c), and (d)). In the first insertion scenario (shown in Fig. 7(b)), the dynamic pickup demand (node 8) is inserted into the initial route, and the original vehicle (Vehicle 1) can serve node 8 by detouring. In the second insertion scenario (shown in Fig. 7(c)), the goods in the original vehicle (Vehicle 2) are transferred to another vehicle (Vehicle 3), so the original vehicle can release its capacity to serve the dynamic pickup demand (node 9). In the third insertion scenario (shown in Fig. 7(d)), a new vehicle (Vehicle 4) is arranged to serve the dynamic pickup demand (node 10) if no existing vehicle can satisfy it. The specific process of the insertion strategy is shown in Table 11.

Table 11
Pseudocode of the insertion strategy.

```pseudocode
Input: information of dynamic demands, gbest, database, Cn, distance matrix
Output: gbest, database, Cn, distance matrix
1 For each customer with the dynamic pickup demand
2     Update database, Cn and distance matrix when adding dynamic pickup demands’ information
3     Set Z to storage feasible solutions for dynamic demands in gbest, Zn to count the number of feasible solutions, Zn = 0
4     Set i = 1
5     While i ≤ vnum, do
6         Calculate the number of goods loaded on vehicle i
7         If vehicle i’s loading status is appropriate to accept the insertion of the dynamic pickup demand, do
8             Find out all feasible insertion positions for satisfying the dynamic pickup demand
9             Record the optimum position for inserting the dynamic pickup demand
10            Zn=Zn+1
11        Else
12            Zn=Zn
13        End if
14        i = i+1
15    End while
16    If Zn = 0, do
17        Arrange a new vehicle to meet the dynamic pickup demand
18    Else
19        Compare all feasible solutions in Z to find out the optimum arrangements for the dynamic pickup demand
20    End if
21    Update the gbest
22 End for
```

## 5. Implementation and analysis

### 5.1. Algorithm performance test

#### 5.1.1. Small-scale instances

In order to demonstrate the accuracy and effectiveness of the proposed 3DAPANSGA-II, the computational results of the CPLEX solver (i.e., ILOG CPLEX Optimization Studio 12.10), 3DAPANSGA-II, multi-objective ant colony optimization (MOACO), MOPSO, MOEA, multi-objective genetic algorithm (MOGA) and decomposition-based multi-objective evolutionary algorithm with tabu search (MOEA/D-TS) are compared on small-scale instances. 15 instances are generated based on the dataset Pr10 of Cordeau’s MDVRPTW benchmark, and these instances are divided into three groups according to the different number of customers. In each instance, customers are randomly selected from the dataset Pr10, and the selected customers are randomly set as one demand type of static delivery demand, static pickup demand, or dynamic pickup demand to ensure that the three demand types are included in the instance. Two depots furthest apart in the Pr10 are selected as the pickup and delivery depots in each instance. The CPLEX solver and other multi-objective algorithms are executed to obtain the minimum $TOC$ of the MDPDTWDD model, where the number of vehicles is merged into the $TOC$. The combination of Pareto optimization solution selection in the solution process may lead to the result of $TOC$ is not necessarily optimal (Mamaghani and Davari, 2020). The time limits of CPLEX solver are 1800 s, 3600 s, and 5600 s for the three groups of instances. Besides, the 3DAPANSGA-II, MOACO, MOPSO, MOEA, MOGA, and MOEAD-TS are implemented 20 runs for each instance, and the optimal results and corresponding computation times ($CT$s) are recorded within 20 runs. Table 12 and Table 13 compare the computational results of CPLEX solver and other six algorithms on the small instances.

In Tables 12 and 13 and in the first five instances, the longest computation time for the CPLEX solver is 1078.1 s, while the proposed 3DAPANSGA-II takes only 29.6 s to find out the solution with reasonable gap. In the instances of group 2, the computation time of the 3DAPANSGA-II is far less than that of the CPLEX solver, meaning that the APANSGA-II can help the manager to make quick decision. In the instance 12, the CPLEX solver takes 4835.4 s to obtain the optimal solution, while the 3DAPANSGA-II takes only 76.6 s. The average $CT$ of the CPLEX solver is 2776.6 s, and those of the 3DAPANSGA-II, MOACO, MOPSO, MOEA, MOGA and MOEAD-TS are 54.1 s, 63.5 s, 61.4 s, 57.7 s, 60.0 s, and 55.2 s, respectively. Besides, compared with the other five algorithms, the 3DAPANSGA-II has the lowest average $TOC$ gap with the CPLEX solver. Furthermore, the design of an elite iteration mechanism that integrates the genetic operation, local search, and insertion strategy improves the convergence performance and effectively avoids falling into the local search space, thereby enhancing the computational efficiency of the algorithm and improving the stability and reliability of the proposed algorithm in solving small-scale instances. Therefore, the proposed 3DAPANSGA-II exhibits the reliability and high-efficiency to solve the small-scale instances of the MDPDTWDD within a shorter computation time.

**Table 12**
Result comparison of the CPLEX solver, 3DAPANSGA-II, MOACO, and MOPSO.

| Groups | Instances | Number of customers | CPLEX | | | 3DAPANSGA-II | | | | MOACO | | | | MOPSO | | | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | | | TOC | NV | CT (s) | TOC | NV | CT (s) | TOC gap | TOC | NV | CT (s) | TOC gap | TOC | NV | CT (s) | TOC gap |
| 1 | 1 | 20 | 1098.9 | 3 | 702.7 | 1098.9 | 3 | 27.4 | 0.00 | 1098.9 | 3 | 36.4 | 0.00 | 1098.9 | 3 | 34.9 | 0.00 |
| | 2 | 20 | 1159.5 | 3 | 854.6 | 1159.5 | 3 | 28.2 | 0.00 | 1159.5 | 3 | 40.5 | 0.00 | 1159.5 | 3 | 38.1 | 0.00 |
| | 3 | 20 | 1174.6 | 3 | 731.5 | 1174.6 | 3 | 27.8 | 0.00 | 1187.4 | 3 | 31.9 | 1.09 | 1185.3 | 3 | 30.5 | 0.91 |
| | 4 | 20 | 1340.7 | 4 | 1078.1 | 1346.4 | 4 | 29.6 | 0.43 | 1353.9 | 4 | 36.7 | 0.98 | 1351.4 | 4 | 34.8 | 0.80 |
| | 5 | 20 | 1204.1 | 3 | 856.9 | 1204.1 | 3 | 28.5 | 0.00 | 1204.1 | 3 | 44.3 | 0.00 | 1204.1 | 3 | 40.2 | 0.00 |
| 2 | 6 | 30 | 1341.8 | 4 | 2719.3 | 1362.7 | 4 | 57.6 | 1.56 | 1371.5 | 4 | 61.5 | 2.21 | 1369.8 | 4 | 60.4 | 2.09 |
| | 7 | 30 | 1356.2 | 4 | 3244.9 | 1356.2 | 4 | 62.1 | 0.00 | 1365.8 | 4 | 68.5 | 0.71 | 1364.5 | 4 | 67.8 | 0.61 |
| | 8 | 30 | 1385.3 | 4 | 2887.5 | 1385.3 | 4 | 59.7 | 0.00 | 1385.3 | 4 | 71.4 | 0.00 | 1385.3 | 4 | 68.9 | 0.00 |
| | 9 | 30 | 1364.8 | 4 | 2413.7 | 1379.5 | 4 | 54.9 | 1.08 | 1394.2 | 4 | 60.2 | 2.15 | 1392.9 | 4 | 58.4 | 2.06 |
| | 10 | 30 | 1359.4 | 4 | 2659.2 | 1374.8 | 4 | 57.2 | 1.13 | 1385.6 | 4 | 63.2 | 1.93 | 1383.7 | 4 | 61.3 | 1.79 |
| 3 | 11 | 40 | 1559.6 | 5 | 4675.8 | 1559.6 | 5 | 75.4 | 0.00 | 1559.6 | 5 | 91.6 | 0.00 | 1559.6 | 5 | 88.9 | 0.00 |
| | 12 | 40 | 1564.7 | 5 | 4835.4 | 1564.7 | 5 | 76.6 | 0.00 | 1568.7 | 5 | 83.4 | 0.26 | 1565.8 | 5 | 81.5 | 0.07 |
| | 13 | 40 | 1506.5 | 5 | 4668.1 | 1543.9 | 5 | 75.3 | 2.48 | 1556.1 | 5 | 84.5 | 3.29 | 1552.4 | 5 | 82.6 | 3.05 |
| | 14 | 40 | 1583.1 | 6 | 4594.6 | 1602.2 | 6 | 74.5 | 1.21 | 1620.5 | 6 | 83.6 | 2.36 | 1619.2 | 6 | 81.9 | 2.28 |
| | 15 | 40 | 1555.9 | 5 | 4726.3 | 1555.9 | 5 | 76.1 | 0.00 | 1555.9 | 5 | 94.7 | 0.00 | 1555.9 | 5 | 90.1 | 0.00 |
| | Average | 30 | 1370.3 | 4 | 2776.6 | 1377.9 | 4 | 54.1 | 0.53 | 1384.5 | 4 | 63.5 | 1.00 | 1383.2 | 4 | 61.4 | 0.91 |

**Table 13**
Result comparison of the CPLEX solver, MOEA, MOGA, and MOEAD-TS.

| Groups | Instances | Number of customers | CPLEX  |     |        | MOEA   |     |        |         | MOGA   |     |        |         |  MOEA/D-TS |     |        |         |
| :----- | :-------- | :------------------ | :----- | :-- | :----- | :----- | :-- | :----- | :------ | :----- | :-- | :----- | :------ | :--------- | :-- | :----- | :------ |
|        |           |                     | TOC    | NV  | CT (s) | TOC    | NV  | CT (s) | TOC gap | TOC    | NV  | CT (s) | TOC gap | TOC        | NV  | CT (s) | TOC gap |
| 1      | 1         | 20                  | 1098.9 | 3   | 702.7  | 1098.9 | 3   | 30.2   | 0.00    | 1098.9 | 3   | 33.5   | 0.00    | 1098.9     | 3   | 28.1   | 0.00    |
|        | 2         | 20                  | 1159.5 | 3   | 854.6  | 1159.5 | 3   | 33.5   | 0.00    | 1159.5 | 3   | 36.7   | 0.00    | 1159.5     | 3   | 30.4   | 0.00    |
|        | 3         | 20                  | 1174.6 | 3   | 731.5  | 1182.5 | 3   | 28.6   | 0.67    | 1183.6 | 3   | 30.1   | 0.77    | 1179.3     | 3   | 26.5   | 0.40    |
|        | 4         | 20                  | 1340.7 | 4   | 1078.1 | 1349.4 | 4   | 33.4   | 0.65    | 1350.1 | 4   | 33.5   | 0.70    | 1348.2     | 4   | 31.3   | 0.56    |
|        | 5         | 20                  | 1204.1 | 3   | 856.9  | 1204.1 | 3   | 35.8   | 0.00    | 1204.1 | 3   | 38.9   | 0.00    | 1204.1     | 3   | 29.7   | 0.00    |
| 2      | 6         | 30                  | 1341.8 | 4   | 2719.3 | 1365.7 | 4   | 57.6   | 1.78    | 1368.3 | 4   | 59.8   | 1.97    | 1363.4     | 4   | 58.4   | 1.61    |
|        | 7         | 30                  | 1356.2 | 4   | 3244.9 | 1357.4 | 4   | 65.1   | 0.09    | 1361.6 | 4   | 65.9   | 0.40    | 1356.2     | 4   | 63.5   | 0.00    |
|        | 8         | 30                  | 1385.3 | 4   | 2887.5 | 1385.3 | 4   | 63.9   | 0.00    | 1385.3 | 4   | 66.7   | 0.00    | 1385.3     | 4   | 60.8   | 0.00    |
|        | 9         | 30                  | 1364.8 | 4   | 2413.7 | 1390.5 | 4   | 54.6   | 1.88    | 1392.8 | 4   | 56.8   | 2.05    | 1388.4     | 4   | 53.2   | 1.73    |
|        | 10        | 30                  | 1359.4 | 4   | 2659.2 | 1378.6 | 4   | 59.3   | 1.41    | 1380.9 | 4   | 60.4   | 1.58    | 1376.1     | 4   | 57.4   | 1.23    |
| 3      | 11        | 40                  | 1559.6 | 5   | 4675.8 | 1559.6 | 5   | 82.5   | 0.00    | 1559.6 | 5   | 85.7   | 0.00    | 1559.6     | 5   | 79.6   | 0.00    |
|        | 12        | 40                  | 1564.7 | 5   | 4835.4 | 1564.7 | 5   | 80.7   | 0.00    | 1564.7 | 5   | 82.9   | 0.00    | 1564.7     | 5   | 77.9   | 0.00    |
|        | 13        | 40                  | 1506.5 | 5   | 4668.1 | 1548.4 | 5   | 79.8   | 2.78    | 1550.9 | 5   | 81.2   | 2.95    | 1544.3     | 5   | 75.7   | 2.51    |
|        | 14        | 40                  | 1583.1 | 6   | 4594.6 | 1615.3 | 6   | 77.2   | 2.03    | 1618.1 | 6   | 80.5   | 2.21    | 1609.5     | 6   | 75.8   | 1.67    |
|        | 15        | 40                  | 1555.9 | 5   | 4726.3 | 1555.9 | 5   | 83.4   | 0.00    | 1555.9 | 5   | 87.6   | 0.00    | 1555.9     | 5   | 80.3   | 0.00    |
|        | Average   | 30                  | 1370.3 | 4   | 2776.6 | 1381.1 | 4   | 57.7   | 0.75    | 1382.3 | 4   | 60.0   | 0.84    | 1379.6     | 4   | 55.2   | 0.65    |

#### 5.1.2. Medium-large scale instances

This section verifies the performance of the proposed 3DAPANSGA-II on medium-large scale instances by comparing with MOACO (Li et al., 2019), MOPSO (Sarbijan and Behnamian, 2022), MOEA (Wang et al., 2021a), MOGA (Ghannadpour et al., 2020), and MOEAD-TS (Cai et al., 2024). The above five algorithms are multi-objective heuristic algorithms, and they are commonly used to solve the multi-depot vehicle routing problem with time windows. Compared with the proposed algorithm, the other five algorithms take the $TOC$ and $NV$ as the bi-objective function to design the selection process of Pareto optimization solutions. Besides, MOGA, MOACO, and MOPSO incorporate the elite retention with the local iteration, while MOEA and MOEAD-TS design a selective assignment mechanism between local iteration and global search, thereby improving the diversity and stability of the five algorithms in solving the bi-objective optimization problem. Therefore, the five approaches are selected for the comparative analysis in this study. [The Source codes](https://github.com/xiaogou-98/algorithm-code) of these six algorithms are available on a cloud platform. Furthermore, [30 instances](https://github.com/helloaiyoweily/Instance-and-case/tree/master) are constructed based on MDVRPTWs and PDVRPTWs benchmark instances provided on [NEO](https://neo.lcc.uma.es/vrp/vrp-instances/vehicle-routing-problem-with-pick-up-and-deliveries/). Given the differences between the MDPDTWDD and the instances provided on NEO, some adjustments such as merging and swapping on benchmark instances are necessary. Table 14 shows the information of the final tested benchmark instances. Besides, three indicators, such as $TOC$, $NV$, and $CT$ are calculated to assess the performance of above algorithms. The equipment utilized to test is a laptop with CPU Intel Core i7 3.3 GHz and 16 GB, and the six algorithms are coded in MATLAB 2016 and Python 3.8. Table 15 lists the related parameters of those algorithms, and Table 16 illustrates the optimum result of each algorithm in ten tests.

**Table 14**
Characteristics of the instances.

| Instances | DDs | PDs | Customers | Customers with static delivery demands | Customers with static pickup demands | Customers with dynamic pickup demands |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 1 | 1 | 48 | 25 | 18 | 5 |
| 2 | 1 | 1 | 72 | 34 | 28 | 10 |
| 3 | 1 | 1 | 96 | 48 | 43 | 5 |
| 4 | 1 | 1 | 120 | 57 | 53 | 10 |
| 5 | 1 | 1 | 150 | 77 | 63 | 10 |
| 6 | 1 | 2 | 48 | 25 | 18 | 5 |
| 7 | 1 | 2 | 72 | 34 | 28 | 10 |
| 8 | 1 | 2 | 96 | 48 | 43 | 5 |
| 9 | 1 | 2 | 120 | 57 | 53 | 10 |
| 10 | 1 | 2 | 150 | 77 | 63 | 10 |
| 11 | 2 | 1 | 48 | 25 | 18 | 5 |
| 12 | 2 | 1 | 72 | 34 | 28 | 10 |
| 13 | 2 | 1 | 96 | 48 | 43 | 5 |
| 14 | 2 | 1 | 120 | 57 | 53 | 10 |
| 15 | 2 | 1 | 150 | 77 | 63 | 10 |
| 16 | 2 | 2 | 48 | 25 | 18 | 5 |
| 17 | 2 | 2 | 72 | 34 | 28 | 10 |
| 18 | 2 | 2 | 96 | 48 | 43 | 5 |
| 19 | 2 | 2 | 120 | 57 | 53 | 10 |
| 20 | 2 | 2 | 150 | 77 | 63 | 10 |
| 21 | 1 | 3 | 48 | 25 | 18 | 5 |
| 22 | 1 | 3 | 72 | 34 | 28 | 10 |
| 23 | 1 | 3 | 96 | 48 | 43 | 5 |
| 24 | 1 | 3 | 120 | 57 | 53 | 10 |
| 25 | 1 | 3 | 150 | 77 | 63 | 10 |
| 26 | 3 | 1 | 48 | 25 | 18 | 5 |
| 27 | 3 | 1 | 72 | 34 | 28 | 10 |
| 28 | 3 | 1 | 96 | 48 | 43 | 5 |
| 29 | 3 | 1 | 120 | 57 | 53 | 10 |
| 30 | 3 | 1 | 150 | 77 | 63 | 10 |

**Table 15**
Parameter settings of the six multi-objective algorithms.

| Algorithms   | Parameters                    | Value          | Parameters                  | Value  | Parameters     | Value |
| :----------- | :---------------------------- | :------------- | :-------------------------- | :----- | :------------- | :---- |
| 3DAPANSGA-II | $M_{gen}$                     | 150            | $\alpha_v$                         | 30     | $T$            | 364   |
|              | $R_c$                         | Min (5, $C_n$) | $f_v$                       | 0.07   | $IR$           | 1.1   |
|              | $N_{IND}$                     | 100            | $p_v$                       | 7      | $\varepsilon$  | 20    |
|              | $cp$                          | 0.90           | $M_v$                       | 40,000 | $\omega$       | 30    |
|              | $mp$                          | 0.05           | $\chi$                  | 1      | $R_{Lg}$       | 15    |
|              | $gp$                          | 0.90           | $w$                         | 1.2    | $\delta$       | 1     |
|              | $\partial_v$                  | 100            | $C_e$                       | 2.7478 | $\gamma$       | 1     |
| MOACO        | Number of ants                | 40             | $\alpha$                  | 1      | $\beta$        | 3     |
|              | extraction rate               | 0.9            | $\rho_g$                    | 0.05   |                |       |
| MOPSO        | Personal learning coefficient | 1.25           | Global learning coefficient | 2      | inertia weight | 0.9   |
| MOEA         | Size of neighborhood          | 15             | $N_{IND}$                   | 80     | $cp$           | 0.8   |
| MOGA         | $N_{IND}$                     | 100            | Number of generations       | 100    | $cp$           | 0.8   |
|              | $mp$                          | 0.6            | Number of grids             | 5      |                |       |
| MOEA/D-TS    | Number of generations         | 50             | Number of vectors           | 2      | $N_{IND}$      | 100   |
|              | Size of archive               | 50             | $cp$                        | 0.5    |                |       |

In Table 16, several evidences state that the performance of the proposed algorithm outperforms other algorithms. First, the average values obtained by the proposed algorithm are better than that of the other five algorithms. Second, the t-test and p-value indicate that the proposed algorithm is distinctly different from other algorithms. Third, the optimum solutions of some instances, such as instances 6 and 11, are quickly obtained by the proposed algorithm compared with the other algorithms. Finally, in instances that consist of multiple depots (i.e., instances 5, 15, and 25), the optimum solution obtained by the proposed algorithm is better than that obtained by the other five algorithms.

**Table 16**
Results of these algorithms on each instance.

| Instances | 3DAPANSGA-II |     |        | MOACO    |          |          | MOPSO    |          |          | MOEA     |          |          | MOGA     |          |          | MOEA/D-TS |          |          |
| :-------- | :----------- | :-- | :----- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :-------- | :------- | :------- |
|           | TOC ($)      | NV  | CT (s) | TOC ($)  | NV       | CT (s)   | TOC ($)  | NV       | CT (s)   | TOC ($)  | NV       | CT (s)   | TOC ($)  | NV       | CT (s)   | TOC ($)   | NV       | CT (s)   |
| 1         | 1654         | 6   | 84     | 1715     | 6        | 107      | 1709     | 6        | 102      | 1654     | 6        | 92       | 1657     | 6        | 98       | 1654      | 6        | 85       |
| 2         | 2715         | 9   | 142    | 2894     | 9        | 174      | 2818     | 9        | 172      | 2723     | 9        | 156      | 2734     | 9        | 167      | 2715      | 9        | 149      |
| 3         | 3362         | 14  | 208    | 3456     | 14       | 239      | 3434     | 14       | 233      | 3387     | 14       | 224      | 3401     | 14       | 231      | 3364      | 13       | 196      |
| 4         | 8785         | 20  | 666    | 8961     | 20       | 735      | 8904     | 20       | 727      | 8804     | 20       | 683      | 8823     | 20       | 705      | 8790      | 20       | 672      |
| 5         | 13,177       | 21  | 481    | 14,635   | 24       | 493      | 14,631   | 24       | 487      | 14,460   | 24       | 487      | 14,579   | 24       | 494      | 14,351    | 24       | 490      |
| 6         | 1577         | 6   | 131    | 1757     | 6        | 169      | 1670     | 6        | 165      | 1577     | 6        | 154      | 1598     | 6        | 162      | 1577      | 6        | 142      |
| 7         | 2094         | 8   | 365    | 2180     | 8        | 428      | 2095     | 8        | 421      | 2105     | 8        | 406      | 2125     | 8        | 414      | 2090      | 8        | 371      |
| 8         | 2926         | 11  | 392    | 3087     | 11       | 416      | 2982     | 11       | 398      | 2926     | 11       | 378      | 2978     | 11       | 393      | 2926      | 11       | 372      |
| 9         | 5399         | 18  | 273    | 5614     | 19       | 318      | 5579     | 19       | 301      | 5478     | 18       | 289      | 5567     | 19       | 295      | 5427      | 18       | 280      |
| 10        | 5682         | 19  | 370    | 6038     | 20       | 409      | 6019     | 20       | 412      | 5858     | 20       | 381      | 5970     | 20       | 394      | 5842      | 20       | 374      |
| 11        | 1313         | 5   | 119    | 1385     | 5        | 162      | 1375     | 5        | 159      | 1313     | 5        | 140      | 1325     | 5        | 152      | 1313      | 5        | 135      |
| 12        | 1687         | 7   | 197    | 1685     | 7        | 245      | 1650     | 7        | 234      | 1687     | 7        | 213      | 1694     | 7        | 227      | 1687      | 7        | 201      |
| 13        | 3457         | 14  | 404    | 3583     | 14       | 468      | 3502     | 14       | 456      | 3457     | 14       | 428      | 3482     | 14       | 445      | 3467      | 14       | 413      |
| 14        | 3643         | 15  | 332    | 3793     | 15       | 353      | 3709     | 15       | 369      | 3680     | 15       | 345      | 3696     | 15       | 356      | 3650      | 15       | 339      |
| 15        | 17,252       | 31  | 430    | 18,874   | 35       | 443      | 18,842   | 35       | 435      | 18,644   | 35       | 418      | 18,752   | 35       | 421      | 18,369    | 34       | 426      |
| 16        | 1549         | 6   | 169    | 1697     | 6        | 192      | 1685     | 6        | 189      | 1549     | 6        | 183      | 1593     | 6        | 194      | 1549      | 6        | 167      |
| 17        | 2380         | 11  | 196    | 2507     | 11       | 227      | 2469     | 11       | 214      | 2380     | 11       | 192      | 2407     | 11       | 201      | 2380      | 11       | 198      |
| 18        | 2973         | 12  | 253    | 3189     | 12       | 314      | 3121     | 12       | 306      | 3045     | 12       | 281      | 3071     | 12       | 295      | 2985      | 12       | 269      |
| 19        | 3497         | 16  | 261    | 3639     | 16       | 329      | 3561     | 16       | 312      | 3476     | 16       | 287      | 3492     | 16       | 301      | 3461      | 16       | 265      |
| 20        | 4485         | 18  | 886    | 4780     | 19       | 936      | 4776     | 19       | 925      | 4613     | 18       | 903      | 4639     | 19       | 917      | 4510      | 18       | 873      |
| 21        | 1568         | 7   | 280    | 1762     | 7        | 304      | 1589     | 7        | 293      | 1568     | 7        | 278      | 1573     | 7        | 283      | 1568      | 7        | 275      |
| 22        | 2270         | 10  | 389    | 2421     | 11       | 435      | 2324     | 11       | 423      | 2273     | 10       | 411      | 2286     | 10       | 419      | 2262      | 10       | 396      |
| 23        | 3377         | 15  | 525    | 3519     | 15       | 556      | 3486     | 15       | 547      | 3398     | 15       | 544      | 3421     | 15       | 549      | 3384      | 15       | 531      |
| 24        | 3403         | 15  | 371    | 3581     | 15       | 417      | 3524     | 15       | 405      | 3472     | 15       | 389      | 3489     | 15       | 398      | 3452      | 15       | 375      |
| 25        | 6874         | 31  | 827    | 7382     | 32       | 888      | 7365     | 32       | 877      | 7255     | 33       | 864      | 7334     | 32       | 872      | 7161      | 33       | 841      |
| 26        | 1252         | 4   | 129    | 1391     | 4        | 156      | 1386     | 4        | 144      | 1252     | 4        | 137      | 1294     | 4        | 139      | 1252      | 4        | 125      |
| 27        | 2105         | 10  | 445    | 2375     | 10       | 478      | 2287     | 10       | 469      | 2105     | 10       | 453      | 2197     | 10       | 462      | 2105      | 10       | 449      |
| 28        | 4256         | 19  | 618    | 4364     | 19       | 659      | 4299     | 19       | 651      | 4256     | 19       | 639      | 4273     | 19       | 647      | 4229      | 19       | 620      |
| 29        | 3433         | 16  | 652    | 3840     | 19       | 678      | 3790     | 18       | 665      | 3701     | 17       | 635      | 3722     | 17       | 651      | 3667      | 17       | 649      |
| 30        | 4731         | 19  | 598    | 4884     | 19       | 681      | 4856     | 19       | 673      | 4787     | 19       | 648      | 4815     | 19       | 667      | 4764      | 19       | 595      |
| Average   | 4096         | 14  | 373    | 4366     | 14       | 414      | 4315     | 14       | 405      | 4229     | 14       | 388      | 4266     | 14       | 398      | 4198      | 14       | 376      |
| t-test    |              |     |        | -4.1E+00 | -2.6E+00 | -1.2E+01 | -3.2E+00 | -2.6E+00 | -1.0E+01 | -2.2E+00 | -2.1E+00 | -5.4E+00 | -2.6E+00 | -2.4E+00 | -8.3E+00 | -1.9E+00  | -1.9E+00 | -1.8E+00 |
| p-value   |              |     |        | 1.5E-04  | 6.8E-03  | 2.4E-13  | 1.6E-03  | 6.8E-03  | 2.6E-11  | 2.0E-02  | 2.3E-02  | 3.7E-06  | 7.8E-03  | 1.3E-02  | 1.7E-09  | 3.2E-02   | 3.6E-02  | 4.3E-02  |

In order to further measure the performance of above six algorithms, several performance metrics of multi-objective algorithm are used, such as the hyper-volume ($HV$), mean ideal distance ($MID$), number of Pareto optimal solutions ($NOP$), and diversity ($DI$) (Vahdani et al., 2019; Zarouk et al., 2022). Table 17 shows the computational results based on the first 15 instances. In Table 17, the computational results obtained by the proposed algorithm are obviously different from the results of the other five algorithms according to the p-values. The average $NOP$ value of 3DAPANSGA-II is 9.87, which is higher than that of other five multi-objective algorithms. The comparison of average $NOP$ values represents that the proposed algorithm can obtain more Pareto solutions. The proposed algorithm can get the nondominated solutions with the largest average $HV$ and lowest average $MID$, which indicates that the proposed algorithm performs better in terms of diversity and convergence. The $DI$ evaluates the spread degree of nondominated solutions, and the largest average value of $DI$ (17.43) can be obtained by the proposed algorithm, which means that its solutions are more widely distributed in the multi-objective space. Therefore, the proposed algorithm outperforms the other five algorithms in solving the MDPDTWDD.

**Table 17**
Computational results of four metrics.

| Instances | 3DAPANSGA-II | | | | MOACO | | | | MOPSO | | | | MOEA | | | | MOGA | | | | MOEAD-TS | | | |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| | NOP | HV | MID | DI | NOP | HV | MID | DI | NOP | HV | MID | DI | NOP | HV | MID | DI | NOP | HV | MID | DI | NOP | HV | MID | DI |
| 1 | 9 | 0.82 | 34.58 | 7.87 | 9 | 0.75 | 36.56 | 7.41 | 9 | 0.77 | 36.35 | 7.43 | 9 | 0.79 | 36.21 | 7.55 | 9 | 0.78 | 36.32 | 7.49 | 9 | 0.80 | 35.76 | 7.66 |
| 2 | 11 | 0.72 | 91.40 | 13.53 | 9 | 0.69 | 94.22 | 13.56 | 10 | 0.72 | 92.01 | 13.69 | 10 | 0.72 | 92.53 | 13.45 | 10 | 0.71 | 92.34 | 13.53 | 10 | 0.71 | 91.95 | 13.51 |
| 3 | 10 | 0.87 | 107.33 | 13.93 | 10 | 0.82 | 109.89 | 12.58 | 9 | 0.81 | 110.22 | 12.31 | 9 | 0.84 | 109.88 | 12.68 | 9 | 0.83 | 110.01 | 12.46 | 10 | 0.85 | 108.44 | 13.23 |
| 4 | 8 | 0.78 | 90.77 | 15.84 | 8 | 0.71 | 91.63 | 15.03 | 9 | 0.73 | 92.63 | 15.32 | 8 | 0.75 | 91.76 | 15.56 | 8 | 0.75 | 91.56 | 15.54 | 8 | 0.76 | 91.53 | 15.67 |
| 5 | 7 | 0.80 | 285.01 | 21.84 | 7 | 0.74 | 290.99 | 20.12 | 7 | 0.75 | 289.41 | 20.48 | 7 | 0.76 | 287.11 | 20.74 | 7 | 0.76 | 288.14 | 20.61 | 7 | 0.78 | 286.32 | 21.25 |
| 6 | 10 | 0.88 | 114.33 | 15.23 | 9 | 0.79 | 118.68 | 14.44 | 9 | 0.81 | 117.56 | 14.56 | 10 | 0.85 | 115.63 | 14.97 | 9 | 0.83 | 116.71 | 14.79 | 10 | 0.85 | 115.01 | 15.02 |
| 7 | 12 | 0.93 | 141.32 | 17.12 | 11 | 0.88 | 144.01 | 16.79 | 10 | 0.87 | 144.79 | 16.75 | 11 | 0.91 | 143.57 | 16.89 | 10 | 0.89 | 144.25 | 16.82 | 11 | 0.92 | 142.27 | 17.06 |
| 8 | 10 | 0.78 | 162.12 | 21.31 | 10 | 0.70 | 169.47 | 20.35 | 10 | 0.73 | 167.58 | 20.85 | 11 | 0.75 | 165.22 | 21.12 | 10 | 0.74 | 166.31 | 21.05 | 10 | 0.76 | 164.31 | 21.23 |
| 9 | 9 | 0.88 | 267.35 | 22.56 | 9 | 0.82 | 274.15 | 20.97 | 9 | 0.83 | 273.47 | 21.55 | 9 | 0.86 | 271.55 | 22.03 | 9 | 0.85 | 272.19 | 21.87 | 9 | 0.87 | 268.84 | 22.37 |
| 10 | 11 | 0.86 | 193.38 | 18.36 | 9 | 0.79 | 201.26 | 17.28 | 10 | 0.82 | 199.14 | 17.98 | 10 | 0.83 | 196.49 | 18.11 | 10 | 0.82 | 197.78 | 18.02 | 10 | 0.84 | 195.25 | 18.19 |
| 11 | 10 | 0.94 | 84.42 | 14.35 | 10 | 0.88 | 86.98 | 13.54 | 10 | 0.91 | 86.83 | 13.87 | 10 | 0.92 | 85.12 | 14.00 | 10 | 0.91 | 86.43 | 13.94 | 10 | 0.93 | 84.93 | 14.14 |
| 12 | 9 | 0.97 | 76.70 | 13.96 | 9 | 0.93 | 81.05 | 13.98 | 8 | 0.92 | 81.75 | 13.51 | 8 | 0.94 | 79.94 | 13.64 | 9 | 0.93 | 80.57 | 13.58 | 9 | 0.95 | 77.05 | 13.75 |
| 13 | 10 | 0.93 | 261.23 | 25.14 | 9 | 0.86 | 272.25 | 23.86 | 9 | 0.88 | 269.82 | 24.75 | 10 | 0.91 | 267.30 | 24.89 | 10 | 0.89 | 268.52 | 24.79 | 10 | 0.92 | 263.89 | 24.98 |
| 14 | 12 | 0.87 | 169.01 | 19.49 | 11 | 0.84 | 176.39 | 19.01 | 11 | 0.85 | 175.13 | 19.21 | 10 | 0.85 | 174.43 | 19.32 | 11 | 0.84 | 174.95 | 19.27 | 12 | 0.86 | 172.14 | 19.39 |
| 15 | 10 | 0.89 | 268.12 | 20.95 | 9 | 0.85 | 288.59 | 20.98 | 10 | 0.86 | 285.12 | 21.01 | 9 | 0.85 | 285.91 | 20.84 | 9 | 0.85 | 285.79 | 20.97 | 10 | 0.88 | 279.01 | 20.86 |
| Average | 9.87 | 0.86 | 156.47 | 17.43 | 9.27 | 0.80 | 162.41 | 16.66 | 9.33 | 0.82 | 161.45 | 16.88 | 9.40 | 0.84 | 160.18 | 17.05 | 9.33 | 0.83 | 160.79 | 16.98 | 9.67 | 0.85 | 158.45 | 17.22 |
| p-value | - | - | - | - | 3.52E-03 | 2.30E-09 | 1.71E-04 | 6.31E-05 | 7.39E-03 | 8.10E-08 | 1.16E-04 | 2.43E-04 | 1.45E-02 | 6.72E-08 | 2.10E-03 | 3.54E-04 | 3.04E-03 | 1.57E-10 | 5.68E-04 | 3.58E-04 | 4.12E-02 | 2.80E-07 | 5.33E-03 | 3.15E-04 |

### 5.2. Data description

A case from Chongqing city, China is adopted to test the practicality and applicability of the proposed approach. In this multi-depot network, six depots (i.e., DD1, DD2, DD3, PD1, PD2, and PD3) provide delivery and pickup services to 220 customers (i.e., C1, C2, C3, ..., and C220). Fig. 8 demonstrates the distribution of customers and depots. In Fig. 8, the customers served by the same depot are widely distributed and disorganized. Each depot provides service solely for its responsible customers, and the initial service routes of each depot are listed in Table 18. The vehicle capacity is set to 100 units, and the number in symbol $\pm$ represents customers’ demands. For example, the number 6 shown in symbol $C87^{+6}$ is the delivery demand of customer C87, and the number 22 shown in symbol $C121^{-22}$ indicates the pickup demand of customer C121. In Table 18, 41 service routes are arranged by these six depots to serve customers in the initial logistics network. No connection or collaboration exists among DDs and PDs. Each vehicle must return to its start after finishing the allotted tasks (i.e., delivery and pickup commodities). Table 19 lists nine indicators (e.g., travel distance $TD$) of each depot in the initial network. In Table 19, the $TAE$ and $TAL$ of each depot are equal to zero, which is probably because the customer's time windows are prioritized in the route design. The $TOC$ is 8372.6, and 41 vehicles are arranged to serve customers. Meanwhile, five service routes are scheduled to provide pickup services for customers with dynamic pickup demands.

**Fig. 8. Distribution of customers and depots.**

**Table 18**
Initial service routes.

| Depot   | Vehicle | Origin | Destination | Customer service order                                                                                                                |
| :------ | :------ | :----- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| **DD1** | V1      | DD1    | DD1         | C82 (20)$^a$ →C37 (16)$^a$ →C61 (15)$^a$ →C69 (15)$^a$ →C87 (6)$^a$                                                                   |
|         | V2      | DD1    | DD1         | C120 (23)$^a$ →C28 (17)$^a$ →C43 (4)$^a$ →C39 (7)$^a$ →C194 (3)$^a$ →C152 (6)$^a$                                                     |
|         | V3      | DD1    | DD1         | C16 (4)$^a$ →C187 (18)$^a$ →C109 (19)$^a$ →C178 (18)$^a$ →C18 (13)$^a$ →C48 (20)$^a$                                                  |
|         | V4      | DD1    | DD1         | C10 (19)$^a$ →C62 (7)$^a$ →C165 (8)$^a$ →C157 (15)$^a$ →C141 (11)$^a$ →C59 (15)$^a$                                                   |
|         | V5      | DD1    | DD1         | C173 (20)$^a$ →C49 (4)$^a$ →C85 (21)$^a$ →C196 (12)$^a$ →C195 (16)$^a$                                                                |
|         | V6      | DD1    | DD1         | C160 (16)$^a$ →C161 (14)$^a$ →C170 (11)$^a$ →C147 (11)$^a$ →C115 (21)$^a$ →C66 (6)$^a$                                                |
| **DD2** | V7      | DD2    | DD2         | C72 (19)$^a$ →C186 (15)$^a$ →C64 (16)$^a$                                                                                             |
|         | V8      | DD2    | DD2         | C156 (4)$^a$ →C132 (21)$^a$ →C111 (17)$^a$ →C3 (16)$^a$ →C171 (12)$^a$                                                                |
|         | V9      | DD2    | DD2         | C198 (6)$^a$ →C73 (17)$^a$ →C162 (7)$^a$ →C96 (7)$^a$ →C91 (15)$^a$ →C200 (11)$^a$                                                    |
|         | V10     | DD2    | DD2         | C6 (10)$^a$ →C36 (13)$^a$ →C83 (8)$^a$ →C97 (21)$^a$ →C174 (20)$^a$ →C193 (9)$^a$                                                     |
|         | V11     | DD2    | DD2         | C98 (21)$^a$ →C57 (11)$^a$ →C138 (15)$^a$ →C113 (4)$^a$ →C25 (10)$^a$ →C101 (14)$^a$                                                  |
|         | V12     | DD2    | DD2         | C183 (15)$^a$ →C76 (15)$^a$ →C93 (19)$^a$ →C197 (22)$^a$                                                                              |
| **DD3** | V13     | DD3    | DD3         | C14 (6)$^a$ →C77 (16)$^a$ →C118 (13)$^a$ →C140 (8)$^a$ →C31 (22)$^a$ →C13 (10)$^a$                                                    |
|         | V14     | DD3    | DD3         | C44 (8)$^a$ →C110 (9)$^a$ →C4 (11)$^a$ →C67 (6)$^a$ →C88 (7)$^a$ →C188 (18)$^a$                                                       |
|         | V15     | DD3    | DD3         | C139 (20)$^a$ →C114 (23)$^a$ →C89 (4)$^a$ →C46 (9)$^a$                                                                                |
|         | V16     | DD3    | DD3         | C180 (17)$^a$ →C135 (22)$^a$ →C94 (20)$^a$ →C119 (9)$^a$                                                                              |
|         | V17     | DD3    | DD3         | C158 (6)$^a$ →C26 (15)$^a$ →C131 (11)$^a$ →C184 (19)$^a$                                                                              |
| **PD1** | V18     | PD1    | PD1         | C121 (-22)$^*$ →C175 (-22)$^*$ →C177 (-19)$^*$ →C53 (-10)$^*$ →C9 (-10)*                                                              |
|         | V19     | PD1    | PD1         | C191 (-22)$^*$ →C103 (-9)$^*$ →C220 (-14)$^*$ →C58 (-3)$^*$ →C144 (-10)$^*$ →C8 (-12)$^*$ →C7 (-21)*                                  |
|         | V20     | PD1    | PD1         | C32 (-14)$^*$ →C136 (-12)$^*$ →C99 (-16)$^*$ →C12 (-21)$^*$ →C164 (-23)$^*$ → C128 (-9)*                                              |
|         | V21     | PD1    | PD1         | C17 (-11)$^*$ →C30 (-5)$^*$ →C216 (-15)$^*$ →C5 (-21)$^*$ →C126 (-19)$^*$ → C133 (-3)$^*$ →C90 (-23)*                                 |
|         | V22     | PD1    | PD1         | C127 (-10)$^*$ →C153 (-5)$^*$ →C212 (-12)$^*$ →C210 (-5)$^*$ →C214 (-21)$^*$ → C84 (-5)*                                              |
|         | V23     | PD1    | PD1         | C21 (-3)$^*$ →C125 (-14)$^*$ →C23 (-9)$^*$ → C166 (-16)$^*$ →C179 (-20)$^*$ →C65 (-21)*                                               |
|         | V24     | PD1    | PD1         | C159 (-3)$^b$ →C163 (-23)$^b$ →C63 (-9)$^b$ →C105 (-7)$^b$ →C151 (-14)$^b$                                                            |
|         | V25     | PD1    | PD1         | C130 (-15)$^*$ →C207 (-11)$^*$ →C52 (-19)$^*$ →C155 (-10)$^*$ →C51 (-16)$^*$ → C213 (-10)*                                            |
|         | V26     | PD1    | PD1         | C181 (-4)$^*$ →C24 (-4)$^*$ →C54 (-18)$^*$ → C208 (-8)$^*$ →C124 (-5)*                                                                |
|         | V27     | PD1    | PD1         | C95 (-23)$^b$ →C20 (-12)$^b$ →C60 (-17)$^b$                                                                                           |
| **PD2** | V28     | PD2    | PD2         | C22 (-4)$^*$ →C42 (-6)$^*$ →C215 (-7)$^*$ → C204 (-18)$^*$ →C134 (-11)$^*$ →C75 (-10)$^*$ →C148 (-6)*                                 |
|         | V29     | PD2    | PD2         | C19 (-3)$^*$ →C206 (-4)$^*$ →C154 (-12)$^*$ →C71 (-9)$^*$ →C185 (-21)$^*$ → C182 (-6)$^*$ →C219 (-12)$^*$ →C203 (-4)$^*$ →C145 (-17)* |
|         | V30     | PD2    | PD2         | C2 (-14)$^*$ →C117 (-9)$^*$ →C209 (-10)$^*$ →C27 (-6)$^*$ →C150 (-9)$^*$ →C56 (-7)*                                                   |
|         | V31     | PD2    | PD2         | C78 (-18)$^*$ →C112 (-3)$^*$ →C68 (-15)$^*$ →C137 (-9)$^*$ →C35 (-20)$^*$ → C199 (-10)$^*$ →C122 (-9)*                                |
|         | V32     | PD2    | PD2         | C33 (-15)$^*$ →C70 (-5)$^*$ →C100 (-17)$^*$ →C29 (-17)*                                                                               |
|         | V33     | PD2    | PD2         | C172 (-13)$^*$ →C149 (-12)$^*$ →C192 (-13)$^*$ →C189 (-6)$^*$ →C79 (-12)$^*$ → C205 (-10)*                                            |
|         | V34     | PD2    | PD2         | C176 (-17)$^b$ →C50 (-8)$^b$ →C168 (-13)$^b$                                                                                          |
| **PD3** | V35     | PD3    | PD3         | C81 (-18)$^*$ →C55 (-17)$^*$ →C86 (-8)$^*$ → C146 (-22)$^*$ →C123 (-7)*                                                               |
|         | V36     | PD3    | PD3         | C116 (-20)$^*$ →C74 (-5)$^*$ →C1 (-14)$^*$ → C40 (-15)$^*$ →C80 (-3)*                                                                 |
|         | V37     | PD3    | PD3         | C142 (-6)$^*$ →C92 (-8)$^*$ →C102 (-15)$^*$ →C129 (-22)$^*$ →C218 (-12)$^*$ → C15 (-19)*                                              |
|         | V38     | PD3    | PD3         | C47 (-22)$^*$ →C169 (-6)$^*$ →C104 (-18)$^*$ →C11 (-15)*                                                                              |
|         | V39     | PD3    | PD3         | C167 (-6)$^*$ →C38 (-5)$^*$ →C106 (-9)$^*$ → C41 (-16)$^*$ →C217 (-23)$^*$ →C143 (-14)$^*$ →C190 (-17)*                               |
|         | V40     | PD3    | PD3         | C201 (-11)$^b$ →C202 (-15)$^b$ →C211 (-16)$^b$                                                                                        |
|         | V41     | PD3    | PD3         | C107 (-13)$^b$ →C45 (-22)$^b$ →C108 (-16)$^b$ →C34 (-21)$^b$                                                                          |

$^a$ Customer with static delivery demand.
$^*$: Customer with static pickup demand.
$^b$ Customer with dynamic pickup demand.

**Table 19**
Initial indicators of each depot.

| Depots | TD (km) | TAE (h) | TAL (h) | TC | PC | MC | FC | TOC | NV |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DD1 | 208.9 | 0 | 0 | 102.3 | 0 | 659.3 | 500.6 | 1262.2 | 6 |
| DD2 | 115.7 | 0 | 0 | 56.7 | 0 | 659.3 | 451 | 1167 | 6 |
| DD3 | 125 | 0 | 0 | 61.3 | 0 | 549.5 | 354.6 | 965.4 | 5 |
| PD1 | 421.5 | 0 | 0 | 206.6 | 0 | 1098.9 | 906.8 | 2212.3 | 10 |
| PD2 | 238.9 | 0 | 0 | 117.1 | 0 | 769.2 | 497 | 1383.3 | 7 |
| PD3 | 218.8 | 0 | 0 | 107.2 | 0 | 769.2 | 506 | 1382.4 | 7 |
| **Total** | **1328.8** | **0** | **0** | **651.2** | **0** | **4505.4** | **3216** | **8372.6** | **41** |

### 5.3. Optimization results

#### 5.3.1. Customer clustering result analysis

We assume that six depots, including DD1, DD2, DD3, PD1, PD2, and PD3, agree to collaborate and share resources with each other to optimize the multi-depot network. Therefore, customers are reallocated and balanced among multiple depots by customer clustering. Fig. 9 demonstrates the clustering results. In Fig. 9, the customers are grouped into clusters on the basis of spatial and temporal distances. The customer clusters served by DD1 and PD2 and those served by DD3 and PD3 do not exist in Fig. 9(a)–(c), respectively. The boundaries of clusters are ambiguous and convoluted on account of customers’ time windows. After the customer clustering, the service relationship between customers and depots has been changed and updated, and the foundation of subsequent route optimization has been built.

**Fig. 9. Customer clustering results.**

#### 5.3.2. Stability analysis for parameter selection

Heuristic methodologies are sensitive to initial parameters, the key parameter settings have a significant influence on finding the optimal solutions (Wang et al., 2021b; Dasdemir et al., 2022). Selecting suitable parameter values can improve the stability and effectiveness of the proposed algorithm. Two key parameters are tuned by calculating the $TOC$ and standard deviation ($SD$) for different parameter values, including the mutation probability (i.e., $mp$) and crossover probability (i.e., $cp$). Each result runs the proposed algorithm 20 times using different parameter values. Table 20 compares the results based on the different parameter values. In Table 20, the lowest $TOC$ and $SD$ can be obtained when $mp = 0.05$ and $cp = 0.9$, which means that $mp = 0.05$ and $cp = 0.9$ make the proposed algorithm more stable and efficient compared with other mutation and crossover probability values. Therefore, the mutation and crossover probabilities are set to 0.05 and 0.9, respectively.

**Table 20**
Comparison of computational results among different parameter values.

| Scenario |          | $mp$     |       |     |         | $cp$     |       |
| :------- | :------- | :------- | :---- | :-- | :------ | :------- | :---- |
|          | Value    | TOC      | SD    |     | Value   | TOC      | SD    |
| 1        | 0.01     | 7160     | 13    |     | 0.1     | 7057     | 21    |
| 2        | 0.02     | 7053     | 10    |     | 0.2     | 6934     | 19    |
| 3        | 0.03     | 7227     | 7     |     | 0.3     | 7033     | 17    |
| 4        | 0.04     | 6981     | 2     |     | 0.4     | 6835     | 18    |
| 5        | **0.05** | **6736** | **1** |     | 0.5     | 6847     | 14    |
| 6        | 0.06     | 6836     | 3     |     | 0.6     | 6773     | 7     |
| 7        | 0.07     | 7026     | 4     |     | 0.7     | 7055     | 8     |
| 8        | 0.08     | 7116     | 4     |     | 0.8     | 6854     | 3     |
| 9        | 0.09     | 6870     | 13    |     | **0.9** | **6736** | **2** |
| 10       | 0.10     | 7055     | 11    |     | 1.0     | 6915     | 4     |
| 11       | 0.11     | 6954     | 9     |     | 1.1     | 7053     | 10    |
| 12       | 0.12     | 6856     | 11    |     | 1.2     | 6857     | 10    |
| 13       | 0.13     | 7029     | 9     |     | 1.3     | 6957     | 14    |
| 14       | 0.14     | 6976     | 7     |     | 1.4     | 6947     | 17    |
| 15       | 0.15     | 6892     | 13    |     | 1.5     | 6840     | 14    |
| 16       | 0.16     | 6883     | 5     |     | 1.6     | 7037     | 12    |
| 17       | 0.17     | 7111     | 10    |     | 1.7     | 6932     | 13    |
| 18       | 0.18     | 7055     | 13    |     | 1.8     | 6851     | 9     |
| 19       | 0.19     | 6993     | 8     |     | 1.9     | 6853     | 11    |
| 20       | 0.20     | 6859     | 11    |     | 2.0     | 7047     | 19    |

**Table 21**
Vehicle routes after the MDPDTWDD optimization.

| Vehicle | Origin | Destination | Customer service order                                                                                                                                           |     |     |
| :------ | :----- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- | --- |
| V1      | DD1    | PD1         | C143 (-14)$^*$→C93 (19)$^a$→C155 (-10)$^*$→C51 (-16)$^*$→C160 (16)$^a$→C213 (-10)$^*$→C161 (14)$^a$→C120 (23)$^a$→C68 (-15)$^*$→C137 (-9)$^*$                    |     |     |
| V2      | DD1    | PD1         | C195 (16)$^a$→C153 (-5)$^*$→C49 (4)$^a$→C54 (-18)$^*$→C127 (-10)$^*$→C84 (-5)$^*$                                                                                |     |     |
| V3      | DD1    | PD1         | C173 (20)$^a$→C208 (-8)$^*$→C4 (11)$^a$→C124 (-5)$^*$→C152 (6)$^a$→C63 (-9)$^b$→C24 (-4)$^*$→C110 (9)$^a$→C163 (-23)$^b$→C159 (-3)$^b$→C181 (-4)$^*$→C88 (7)$^a$ |     |     |
| V4      | DD1    | PD3         | C212 (-12)$^*$→C85 (21)$^a$→C196 (12)$^a$→C210 (-5)$^*$→C62 (7)$^a$→C151 (-14)$^b$→C214 (-21)$^*$→C165 (8)$^a$→C15 (-19)$^*$→C218 (-12)$^*$→C69 (15)$^a$         |     |     |
| V5      | DD1    | PD3         | C10 (19)$^a$→C105 (-7)$^b$→C1 (-14)$^*$→C207 (-11)$^*$→C74 (-5)$^*$→C141 (11)$^a$→C157 (15)$^a$→C116 (-20)$^*$→C211 (-16)$^b$→C115 (21)$^a$                      |     |     |
| V6      | DD1    | PD3         | C16 (4)$^a$→C95 (-23)$^b$→C134 (-11)$^*$→C190 (-17)$^*$→C20 (-12)$^b$→C83 (8)$^a$                                                                                |     |     |
| V7      | DD1    | PD3         | C40 (-15)$^*$→C87 (6)$^a$→C66 (6)$^a$→C52 (-19)$^*$→C80 (-3)$^*$→C72 (19)$^a$→C130 (-15)$^*$→C186 (15)$^a$→C59 (15)$^a$→C147 (11)$^a$                            |     |     |
| V8      | DD2    | PD1         | C34 (-21)$^b$→C187 (18)$^a$→C112 (-3)$^*$→C45 (-22)$^b$→C107 (-13)$^b$→C109 (19)$^a$→C30 (-5)$^*$                                                                |     |     |
| V9      | DD2    | PD1         | C11 (-15)$^*$→C167 (-6)$^*$→C38 (-5)$^*$→C90 (-23)$^*$→C35 (-20)$^*$→C188 (18)$^a$                                                                               |     |     |
| V10     | DD2    | PD2         | C198 (6)$^a$→C73 (17)$^a$→C185 (-21)$^*$→C71 (-9)$^*$→C154 (-12)$^*$→C189 (-6)$^*$→C79 (-12)$^*$→C13 (10)$^a$→C205 (-10)$^*$                                     |     |     |
| V11     | DD2    | PD2         | C47 (-22)$^*$→C25 (10)$^a$→C169 (-6)$^*$→C206 (-4)$^*$→C19 (-3)$^*$→C182 (-6)$^*$→C104 (-18)$^*$→C219 (-12)$^*$→C96 (7)$^a$                                      |     |     |
| V12     | DD2    | PD2         | C57 (11)$^a$→C98 (21)$^a$→C138 (15)$^a$→C108 (-16)$^b$→C78 (-18)$^*$→C122 (-9)$^*$→C99 (-16)$^*$                                                                 |     |     |
| V13     | DD2    | PD2         | C101 (14)$^a$→C145 (-17)$^*$→C5 (-21)$^*$→C113 (4)$^a$→C162 (7)$^a$→C42 (-6)$^*$→C22 (-4)$^*$→C216 (-15)$^*$                                                     |     |     |
| V14     | DD2    | PD3         | C193 (9)$^a$→C197 (22)$^a$→C183 (15)$^a$→C6 (10)$^a$→C174 (20)$^a$→C76 (15)$^a$→C148 (-6)$^*$→C217 (-23)$^*$→C75 (-10)$^*$→C67 (6)$^a$                           |     |     |
| V15     | DD2    | PD3         | C203 (-4)$^*$→C86 (-8)$^*$→C126 (-19)$^*$→C132 (21)$^a$→C146 (-22)$^{*}$ → C201 (-11)$^{b}$ → C102 (-15)$^{*}$ → C111 (17)$^{a}$ → C202 (-15)$^{b}$              |     |     |
| V16     | DD2    | PD3         | C204 (-18)$^*$→C82 (20)$^a$→C36 (13)$^a$→C97 (21)$^a$→C60 (-17)$^b$→C170 (11)$^{a}$ → C123 (-7)$^{*}$ → C92 (-8)$^{*}$ → C3 (16)$^{a}$ → C142 (-6)$^{*}$         |     |     |
| V17     | DD2    | PD3         | C171 (12)$^a$ → C156 (4)$^a$ → C64 (16)$^a$ → C81 (-18)$^*$ → C133 (-3)$^*$ → C215 (-7)$^*$ → C55 (-17)$^*$→ C37 (16)$^a$→ C61 (15)$^a$→ C129 (-22)$^*$          |     |     |
| V18     | DD3    | PD1         | C209 (-10)$^*$→C184 (19)$^a$→C27 (-6)$^*$→C175 (-22)$^*$→C121 (-22)$^*$→C194 (3)$^a$→C114 (23)$^a$→C89 (4)$^a$                                                   |     |     |
| V19     | DD3    | PD1         | C23 (-9)$^*$→C150 (-9)$^*$→C8 (-12)$^*$→C168 (-13)$^b$→C7 (-21)$^*$→C200 (11)$^a$→C41 (-16)$^*$→C106 (-9)$^*$→C28 (17)$^a$→C17 (-11)$^*$                         |     |     |
| V20     | DD3    | PD1         | C21 (-3)$^*$→C18 (13)$^a$→C178 (18)$^a$→C125 (-14)$^*$→C50 (-8)$^b$→C70 (-5)$^*$→C29 (-17)$^*$→C65 (-21)$^*$→C9 (-10)$^*$                                        |     |     |
| V21     | DD3    | PD1         | C43 (4)$^a$→C53 (-10)$^*$→C139 (20)$^a$→C100 (-17)$^*$→C46 (9)$^a$→C39 (7)$^a$                                                                                   |     |     |
| V22     | DD3    | PD1         | C117 (-9)$^*$→C158 (6)$^a$→C26 (15)$^a$→C177 (-19)$^*$→C131 (11)$^a$→C44 (8)$^a$→C48 (20)$^a$                                                                    |     |     |
| V23     | DD3    | PD2         | C135 (22)$^a$→C179 (-20)$^*$→C94 (20)$^a$→C103 (-9)$^*$→C56 (-7)$^*$→C140 (8)$^a$                                                                                |     |     |
| V24     | DD3    | PD2         | C128 (-9)$^*$→C91 (15)$^a$→C199 (-10)$^*$→C164 (-23)$^*$→C12 (-21)$^*$→C180 (17)$^a$                                                                             |     |     |
| V25     | DD3    | PD2         | C14 (6)$^a$→C166 (-16)$^*$→C77 (16)$^a$→C58 (-3)$^*$→C172 (-13)$^*$→C192 (-13)$^*$→C149 (-12)$^*$                                                                |     |     |
| V26     | DD3    | PD2         | C144 (-10)$^*$→C119 (9)$^a$→C2 (-14)$^*$→C118 (13)$^a$→C31 (22)$^a$                                                                                              |     |     |
| V27     | PD2    | PD2         | C220 (-14)$^*$→C191 (-22)$^*$→C176 (-17)$^b$→C33 (-15)$^*$→C32 (-14)$^*$→C136 (-12)$^*$                                                                          |     |     |

- $^a$ customer with static delivery demand
- $^b$ customer with dynamic pickup demand
- $^*$ customer with static pickup demand

**Fig. 10. Optimized routes for static demands with and without performing insertion strategy.**

**Table 22**
Comparison of indicators among four scenarios.

| Scenario                   | TD (km) | TAE (h) | TAL (h) | TC    | PC    | IC  | MC     | FC   | NV  | TOC    | Gap NV | Gap TOC |
| :------------------------- | :------ | :------ | :------ | :---- | :---- | :-- | :----- | :--- | :-- | :----- | :----- | ------- |
| Initial                    | 1328.8  | 0       | 0.00    | 651.2 | 0.0   | 0   | 4505.4 | 3216 | 41  | 8372.6 |        |         |
| Postponed service strategy | 706.7   | 0       | 10.54   | 346.4 | 316.2 | 0   | 3104.5 | 3216 | 29  | 6983.1 | 12     | 1389.5  |
| Non-insertion strategy     | 727.2   | 0       | 0.00    | 379.1 | 0.0   | 0   | 3296.7 | 3216 | 30  | 6891.8 | 11     | 1480.8  |
| Insertion strategy         | 598.0   | 0       | 0.00    | 293.0 | 0.0   | 260 | 2967.0 | 3216 | 27  | 6736.0 | 14     | 1636.6  |

**Fig. 11. Comparison of results among four scenarios.**
#### 5.3.3. MDPDTWDD optimization results
Based on the previous clustering results and key parameter settings, 
the optimized routes can be obtained by the proposed algorithm. 
Table 21shows the optimized routes. Fig. 10presents the optimized 
routes for static demands with and without performing the insertion 
strategy.
In Table 20, multiple depots jointly arrange 27 vehicle routes to serve 
the delivery and pickup demands, including 26 open routes. In Fig. 10
(a)–(b), resources are shared among depots, and vehicles are arranged to 
execute pickup and delivery services simultaneously. For example, in 
Fig. 10(a), the vehicle provides delivery and pickup services in the route 
DD1→C195→C153→C49→C54→C24→C110→C181→C48→PD1. The 
service routes only for static demands in Fig. 10(a) are more than those 
in Fig. 10(b) due to the insertion strategy. In addition, the postponed 
service strategy is also commonly adopted for handling dynamic pickup 
demands (Ulmer et al., 2018; Lan et al., 2024). Table 22and Fig. 11
compare the indicator results among the four scenarios of initial, post
poned service strategy, non-insertion strategy, and insertion strategy (i. 
e., non-postponed service strategy).
In Table 22and Fig. 11, the NVs in four scenarios are 41, 29, 30, and 
27, which indicates the difference in the scenarios of the postponed 
service, non-insertion, and insertion strategies. In addition, the gap of 
TOC between the scenarios of non-insertion and insertion strategies is 
$155.8, and the gap of TOCs between the postponed service and un- 
postponed service strategies is $247.1. This finding proves that the 
insertion of dynamic demands has not caused the TOC to skyrocket. In 
the comparison between the initial and the insertion strategy scenarios, 
the gaps of TOC and NV reached $1636.6 and 14, respectively, directly 
verifying the significant performance of optimization approach in 
solving the MDPDTWDD.

### 5.4. Analysis and discussion

#### 5.4.1. Comparison of different types for time windows

In order to investigate the effects of different time window types on the optimization results, three scenarios are designed and compared, including Scenarios 1, 2, and 3. In Scenario 1, the time window of each customer is its real time window in the case study. In Scenario 2, the start time of the time window for each customer is unchanged, and the end time of the time window for each customer is adjusted to half. In Scenario 3, the start time of the time window for each customer is unchanged, and the end time of the time window for each customer is expanded by a factor of two. Table 23 and Fig. 12 compare the optimization results of the above three scenarios. In Table 23 and Fig. 12, the $TOC$s in three scenarios are 6736.0, 7349.8, and 6487.6. The $NV$s in three scenarios are 27, 30, and 25. Since the end time of each time window is shortened, the $PC$ for time window violations in Scenario 2 is increased by 268.8 compared to Scenario 1. The extension of the end time for each customer reduces the $TOC$ from 6736.0 in Scenario 1 to 6487.6 in Scenario 3. Therefore, the different time window types have an impact on the multiple operational metrics, such as $TOC$, $PC$, and $NV$.

**Table 23**
Result comparison of different types for time windows.

| Scenarios | TD (km) | TAE (h) | TAL (h) | TC | PC | IC | MC | FC | NV | TOC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 598.0 | 0 | 0.00 | 293.0 | 0.0 | 260 | 2967.0 | 3216 | 27 | 6736.0 |
| 2 | 659.6 | 0 | 8.96 | 323.3 | 268.8 | 245 | 3296.7 | 3216 | 30 | 7349.8 |
| 3 | 509.4 | 0 | 0.00 | 249.7 | 0.0 | 260 | 2761.9 | 3216 | 25 | 6487.6 |

**Fig. 12. Comparison of optimal results under the different time window types.**

#### 5.4.2. Comparison of different vehicle capacities

This section further explores the impact of different vehicle capacities on the optimization results. Five scenarios (i.e., Scenarios 1, 2, 3, 4, and 5) with different vehicle capacities are compared, and the vehicle capacities of Scenarios 1 to 5 are 50 units, 75 units, 100 units, 125 units, and 150 units. Table 24 and Fig. 13 show the optimization results under the different vehicle capacities. In Table 24 and Fig. 13, the $NV$s in Scenarios 1 to 5 are 31, 29, 27, 26, and 25, indicating that the $NV$ decreases with the increase in the vehicle capacity. However, an increase of vehicle capacity does not necessarily result in a decrease in $TOC$. The $TOC$s in five scenarios are 7193.7, 6946.7, 6736.0, 6753.3, and 6789.0, while the $TOC$ in Scenario 3 is the lowest value compared to the other scenarios. Therefore, as the vehicle load increases, the $NV$ gradually decreases, while the $TOC$ first decreases and then increases.

**Table 24**
Optimization results under the different vehicle capacities.

| Scenarios | Vehicle capacity (unit) | TD (km) | TAE (h) | TAL (h) | TC | PC | IC | MC | FC | NV | TOC |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 50 | 894.5 | 0.0 | 0.0 | 438.5 | 0 | 233 | 3306.2 | 3216 | 31 | 7193.7 |
| 2 | 75 | 765.4 | 0.0 | 0.0 | 375.2 | 0 | 251 | 3104.5 | 3216 | 29 | 6946.7 |
| 3 | 100 | 598 | 0.0 | 0.0 | 293.0 | 0 | 260 | 2967.0 | 3216 | 27 | 6736.0 |
| 4 | 125 | 570.2 | 3.2 | 4.1 | 279.5 | 187 | 260 | 2810.8 | 3216 | 26 | 6753.3 |
| 5 | 150 | 549.8 | 4.9 | 7.3 | 269.5 | 317 | 260 | 2726.5 | 3216 | 25 | 6789.0 |

**Fig. 13. Optimization objectives under the different vehicle capacities.**

#### 5.4.3. Comparison of different cases for resource sharing

In order to further investigate the effect of resource sharing on the different collaboration patterns, three cases marked C1, C2, and C3 are compared and discussed. In C1, two alliances are marked {DD1, DD2, DD3} and {PD1, PD2, PD3}, and the customer resources are internally shared in each alliance. When the six depots are equally divided into two alliances, the optimization results of all collaborative combinations considering the resource integration of pickup and delivery depots are compared, and the combination with the lowest TOC is selected and set as C2. In C2, two alliances marked {DD1, DD2, PD3} and {DD3, PD1, PD2} are formed, and this case supports the construction of close-open mixed service routes. A major alliance {DD1, DD2, DD3, PD1, PD2, PD3} is established and set as C3. Table 25 states the situation of the three cases.

In Tables 25 and in the C2 and C3, due to the resource sharing among pickup and delivery depots, the vehicles can perform pickup and delivery activities simultaneously. Besides, the insertion strategy is not adopted in these cases, expressing that the dynamic pickup demands are satisfied by arranging new routes. The optimization results of the three cases are presented in Table 26 and Fig. 14.

In Table 26 and Fig. 14, the optimization results (i.e., $NV$ and $TOC$) are reduced by integrating the logistics resources of pickup and delivery depots. For example, the $TOC$ of C2 is decreased by $526.1 compared to C1. Besides, the collaboration pattern in C3 outperforms other patterns in C1 and C2. On the one hand, the $TOC$s of the three cases are $7983.9, $7457.8, and $6891.8, and the C3 obtains the lowest $TOC$ among these cases. On the other hand, C3 only arranges 30 vehicles to provide service for all customers, and the value of this indicator means that the resource configuration in C3 outperforms those in other cases. Therefore, the resource integration and sharing of pickup and delivery depots can contribute to maximize resource utilization and cost reduction.

**Table 25**
Statements of the three cases.

| Case | Alliance | Open-closed route | Closed route | Non-insertion strategy |
| :--- | :--- | :--- | :--- | :--- |
| C1 | {DD1, DD2, DD3}, {PD1, PD2, PD3} | | Yes | Yes |
| C2 | {DD1, DD2, PD3}, {DD3, PD1, PD2} | Yes | | Yes |
| C3 | {DD1, DD2, DD3, PD1, PD2, PD3} | Yes | | Yes |

**Table 26**
Comparison of optimization results in the three cases.

| Cases | Alliance                                 | TD (km) | TC (\$) | PC (\$) | MC (\$) | IC (\$) | FC (\$) |  NV | TOC (\$) |
| :---- | :--------------------------------------- | ------: | ------: | ------: | ------: | ------: | ------: | --: | -------: |
| C1    | $\{DD1, DD2, DD3\}$, $\{PD1, PD2, PD3\}$ |  1021.6 |   500.6 |       0 |  4267.3 |       0 |    3216 |  40 |   7983.9 |
| C2    | $\{DD1, DD2, PD3\}$, $\{DD3, PD1, PD2\}$ |   953.7 |   467.3 |       0 |  3774.5 |       0 |    3216 |  36 |   7457.8 |
| C3    | $\{DD1, DD2, DD3, PD1, PD2, PD3\}$       |   727.2 |   379.1 |       0 |  3296.7 |       0 |    3216 |  30 |   6891.8 |

**Fig. 14.** Result comparison of the three cases.

#### 5.4.4. Result comparison of insertion strategies adopted in different scenarios

Three different scenarios considering integration of pickup and delivery services are discussed to clarify the effect of insertion strategy on optimization results, namely S1, S2, and S3. In S1, two alliances marked {DD1, DD2, PD3} and {DD3, PD1, PD2} are set, manifesting that the vehicle can travel from DD1 to PD3 and serve pickup and delivery demands simultaneously. The optimization results of all two-four collaboration combinations considering the resource sharing of pickup and delivery depots are calculated, and the collaboration pattern with the lowest $TOC$ is set as S2. Two alliances marked {PD1, DD3} and {PD2, PD3, DD1, DD2} are established in S2, and the major alliance {DD1, DD2, DD3, PD1, PD2, PD3} is set as S3. Due to the resource integration of pickup and delivery depots, the open-closed routes can be constructed in each scenario. Besides, the insertion strategy is adopted in each scenario to verify its effectiveness, and the calculation results before and after performing the insertion strategy are shown in Table 27 and Fig. 15.

In Table 27 and Fig. 15, both $NV$ and $TOC$ are reduced by implementing the insertion strategy in each case. For example, the $NV$ and $TOC$ in S3 are decreased from 30 to 6891.8 to 27 and 6736.0, respectively. The collaboration pattern in S3 outperforms those in S1 and S2 on the basis of result comparison. The $TOC$ and $NV$ in the state SA of S3 are `$6736.0` and 27 respectively, indicating that the S3 obtains the lowest $TOC$ and $NV$ among these scenarios. Therefore, the insertion strategy can reduce the number of vehicles and total operating cost, and the collaboration pattern found in S3 can realize significant improvement for this logistics network than other scenarios. Fig. 16 shows the service routes for dynamic pickup demands in the three scenarios.

In Fig. 16(b)–(d), new routes are arranged to meet dynamic pickup demands, and the long-distance transportation still exists because of their collaboration patterns. For instance, in Fig. 16(b)–(d), the vehicle needs to depart from PD1 to serve customers 151 and 105. In Fig. 16(f), the major alliance allows all depots (i.e., pickup depots and delivery depots) to share resources for avoiding long-distance transportation, and all dynamic pickup demands can be reasonably inserted into the on-working service routes to reduce the number of vehicles. The integration of pickup and delivery services is achieved in the major alliance to save transportation resources and improve the possibility of dynamic demand insertion, such as the route $DD2 \rightarrow 203 \rightarrow 86 \rightarrow 126 \rightarrow 132 \rightarrow 146 \rightarrow 201 \rightarrow 102 \rightarrow 111 \rightarrow 202 \rightarrow PD3$. Besides, the number of new routes in S1 and S2 is reduced by four and three after executing the insertion strategy, respectively. Compared with Fig. 16(e), the insertion strategy is performed in Fig. 16(f) to avoid the generation of five new routes, improving the service efficiency. Therefore, the insertion strategy can effectively reduce $NV$ of each scenario, and the alliance pattern S3 outperforms other patterns in terms of resource utilization.

**Table 27**
Comparison of results before and after executing the insertion strategy.

| Scenario | Alliance                                 | State | TD (km) | TC (\$) | PC (\$) | MC (\$) | IC (\$) | FC (\$) |  NV | TOC (\$) |
| :------- | :--------------------------------------- | :---- | ------: | ------: | ------: | ------: | ------: | ------: | --: | -------: |
| S1       | $\{DD1, DD2, PD3\}$, $\{DD3, PD1, PD2\}$ | SB    |   953.7 |   467.3 |       0 |  3774.5 |       0 |    3216 |  36 |   7457.8 |
|          |                                          | SA    |   812.3 |   398.1 |       0 |  3475.8 |     210 |    3216 |  32 |   7299.9 |
| S2       | $\{PD1, DD3\}$, $\{PD2, PD3, DD1, DD2\}$ | SB    |   872.6 |   427.6 |       0 |  3626.4 |       0 |    3216 |  35 |   7270.0 |
|          |                                          | SA    |   751.1 |   368.0 |       0 |  3356.7 |     222 |    3216 |  31 |   7162.7 |
| S3       | $\{DD1, DD2, DD3, PD1, PD2, PD3\}$       | SB    |   727.2 |   379.1 |       0 |  3296.7 |       0 |    3216 |  30 |   6891.8 |
|          |                                          | SA    |   598.0 |   293.0 |       0 |  2967.0 |     260 |    3216 |  27 |   6736.0 |

**Fig. 15.** Comparison of the objective results in the three scenarios.

**Fig. 16.** Service routes for dynamic demands of three cases.

## 5.5. Management insights

This study focuses on improving the service efficiency of multi-depot network for the dynamic pickup demands by adopting a reasonable insertion strategy and integrating the logistics resources of pickup and delivery depots. Several management insights can be drawn from this study for enterprises to manage their logistics operation.

(1) Collaboration and resource sharing in multi-depot network optimization facilitate balancing and reallocating depot resources (i.e., customers, transportation resources, and storage capacity). Unnecessary costs, such as long-distance service for goods deliveries and pickups, can be effectively avoided. The joint service for customer demands and the integration of delivery and pickup services not only help in improving the quality of services but also promote the sustainable operation of the multi-depot network.

(2) The presented mathematical model and hybrid algorithm 3DAPANSGA-II for optimizing multi-depot delivery and pickup logistics networks can be integrated into logistics service providers’ operation systems to improve their operating efficiency. Irrational service schedules cause the low efficiency in the operation, but the appropriate delivery and pickup service schedules can be arranged by adopting the proposed optimization approach. In addition, the total operating cost and number of vehicles can be reduced by integrating delivery and pickup services. The resource sharing among pickup and delivery depots and the optimization methodology could assist logistics service providers in building an environmental and resource-friendly operational decision support system and maintaining their operating efficiency.

(3) With the rapid development of information technology and digital-driven technology, AI has endowed urban logistics systems with strong intelligent and data-driven processing capabilities. However, in the current urban logistics distribution system, how to quickly respond to customers’ dynamic demands and perform flexible vehicle scheduling provides application scenarios for the AI technology. The machine learning mechanism for dynamic pickup patterns in AI can allow us to predict dynamic pickup demands and design open-closed pickup and delivery vehicle routes considering reasonable idle times in the initial routes. Furthermore, AI will also achieve comprehensive perception, accurate identification, real-time tracking, and intelligent decision-making of urban logistics systems. Additionally, the proposed optimization algorithm can be integrated with the emerging information technology, including AI, Internet of Things, blockchain, digital twin, and Big Data, to not only promote the sustainable development of multi-depot networks but also facilitate constructing smarter and more intelligent logistics systems and further enhancing the resilience of the logistics industry.

## 6. Conclusions

This study incorporates the collaboration and insertion strategies to solve the MDPDTWDD. The collaboration strategy among multi-depots and the insertion strategy for dynamic pickup demands are modeled in a bi-objective optimization model to reduce the total operating costs and number of vehicles. The insertion of dynamic pickup demands, the construction of vehicle routes to integrate delivery and pickup activities, and the formulation of open-closed service routes is considered as a constraint to find an optimal service schedule.

To optimize the MDPDTWDD, a two-stage hybrid heuristic algorithm 3DAPANSGA-II composed of 3D AP clustering algorithm and ANSGA-II is developed to find the Pareto optimal solution. The 3D AP clustering algorithm uses the space-time distance to regroup customers and reduce the computational complexity. The elite iteration mechanism ensures the stability of the algorithm’s optimization direction. Genetic operation and local search operator are developed to maintain the population’s diversity and avoid falling into local optimal solutions. A more crucial design is the insertion strategy, and three types of insertion scenarios are considered to handle dynamic demands by comparing and judging each on-duty vehicle’s loading status.

The correctness and applicability of the proposed model and algorithm are tested on the small-scale instances by comparing with CPLEX solver, and verified on the medium-large scale instances by comparing with MOACO, MOPSO, MOEA, MOGA, and MOEA/D-TS. The numerical results of a case study in Chongqing city, China suggest that significant improvements can be achieved by adopting the proposed approach. The total operating cost in the case study is optimized from 8372.6 to 6736.0, and the number of vehicles is reduced from 41 to 27. The effects of different time window types and different vehicle capacities on the optimization results are discussed and analyzed separately. In addition, the optimization results of different collaboration patterns confirm that the significant improvement of service efficiency can be obtained by encouraging depots to participate in collaboration and share resources. The comparison of optimization results before and after performing the insertion strategy proves that the proposed insertion strategy has remarkable effectiveness in controlling the cost.

In the practical aspect, this study encourages logistics service providers to improve their operational decision support systems through collaboration and resource sharing. On the one hand, the operating cost can be saved, and the service efficiency can be improved. On the other hand, the negative impact of logistics activities on the environment can be mitigated. For future research, some other dynamic factors, such as dynamic travel time and dynamic service time, can be considered in the MDPDTWDD. In addition, the heterogeneous fleet and multi-type commodities can be incorporated into the problem.
