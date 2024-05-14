## Phase 1: Understanding the project

### The project is made up of 3 or 4 sub-problems

#### 1. **Network Design Modeling**
- **Objective**: Develop a computational model that simulates the network design for rural multimodal transportation systems.
- **Details**: This model will incorporate elements of both Capacitated Network Design (CND) and Multimodal Network Design (MND), ensuring that the network can handle specific capacities and integrates various transport modes effectively. The model will be designed for modifiability to adapt to changing needs or conditions.

#### 2. **Scheduling Constraints Modeling**
- **Objective**: Model the scheduling constraints of vehicles within the transportation network.
- **Details**: The model will address multiple scheduling challenges including Multimodal Transport Scheduling (MTS), Vehicle Routing Problem with Time Windows (VRPTW), Resource-Constrained Project Scheduling (RCPS), Crew Scheduling (CrS), and Capacitated Scheduling (CaS). This will enable the system to optimize resource allocation and timing across different modes of transport.

#### 3. **Integrated Network and Scheduling Model**
- **Objective**: Create a unified model that integrates both the network design and the scheduling constraints.
- **Details**: This model aims to address various Vehicle Routing Problems (VRPs), specifically Capacitated Vehicle Routing Problem (CVRP), Vehicle Routing Problem with Time Windows (VRPTW), Pickup and Delivery Problem (PDP), Multi-depot Vehicle Routing Problem (MDVRP), and Multimodal Vehicle Routing Problem (MVRP). The integration ensures that the design supports efficient operational scheduling and vice versa.

#### 4. **Machine Learning Approach (Optional)**
- **Objective**: Explore the possibility of enhancing the model with Machine Learning techniques.
- **Details**: This involves creating or sourcing a dataset relevant to rural multimodal transportation and training the model to predict and optimize network and scheduling operations dynamically.


## Phase 2: Choice of solution to be explored
* State of art, find solutions that have already been explored.

#### Overview of the Work Already Done

|                   | Full optimization | Genetics algorithm | Only neural network | Reinforcement learning |
|-------------------|-------------------|--------------------|----------------|------------------------|
| Network design    | [Yes<sup>1</sup>](#1) | [Yes<sup>2</sup>](#2) | No | [Yes<sup>5</sup>](#5) |
| Scheduling/Sizing | [Yes<sup>1</sup>](#1) | [Yes<sup>2</sup>](#3) | No | [Yes<sup>6</sup>](#6) |
| Time computing    | [Yes<sup>1</sup>](#1) | [Yes<sup>2,3</sup>](#2) | [Yes<sup>4</sup>](#4) | [Yes<sup>5,6</sup>](#5) |

#### References
1. [Design of multimodal transport networks: A hierarchical approach, Van Nes, R. (2002)](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=9a60449caa1b9548f7a0c0bd71986449d85fa473)
2. [Performance of a genetic algorithm for solving the multi-objective, multimodal transportation network design problem, T Brands, EC Van Berkum (2014)](https://www.researchgate.net/profile/Ties-Brands/publication/287579094_Performance_of_a_Genetic_Algorithm_for_Solving_the_Multi-Objective_Multimodal_Transportation_Network_Design_Problem/links/567aa24108ae051f9addcfe4/Performance-of-a-Genetic-Algorithm-for-Solving-the-Multi-Objective-Multimodal-Transportation-Network-Design-Problem.pdf)
3. [Research on Optimizing Multimodal Transport Path under the Schedule Limitation Based on Genetic Algorithm, Cheng Jiang (2022)](https://iopscience.iop.org/article/10.1088/1742-6596/2258/1/012014/pdf)
4. [Short & long term forecasting of multimodal transport passenger flows with machine learning methods, Florian Toqué; Mostepha Khouadjia; Etienne Come; Martin Trepanier; Latifa Oukhellou (2017)](https://ieeexplore.ieee.org/abstract/document/8317939)
5. [Online Multimodal Transportation Planning using Deep Reinforcement Learning, Amirreza Farahani; Laura Genga; Remco Dijkman (2021)](https://ieeexplore.ieee.org/abstract/document/9658943)
6. [Deep reinforcement learning of passenger behavior in multimodal journey planning with proportional fairness, Kai-Fung Chu, Weisi Guo (2023)](https://link.springer.com/article/10.1007/s00521-023-08733-4)

&rarr; We focus on an approach using deep reinforcement learning. For a more in-depth look, let's explore the different varieties of network design, scheduling and time computing. Let's explore different deep reinforcement learning architectures. 



|Type of NN in DRL| DNN | CNN | RNN | LSTM | GNN | 
|-------------------|-------------------|-------------------|--------------------|----------------|------------------------|
| CND | [Yes<sup>8</sup>](#8) | No | No | No | No |
| MND | [Yes<sup>8</sup>](#8) | No | No | No | No |
| MTS | [Yes<sup>8</sup>](#8) | No | No | No | No |
| TNDFSP | No | No | No | No | [Yes<sup>9</sup>](#9) |
| VRPTW    | [Yes<sup>8</sup>](#8) | [Yes<sup>7</sup>](#7) | No | No | No |
| RCPS    | No | No | No | No | No |
| CaS    | [Yes<sup>8</sup>](#8) | No | No | No | No |
| CrS    | No | No | No | No | No |
| CVRP | No | [Yes<sup>7</sup>](#7) | No | No | No |
| PDP    | No | [Yes<sup>7</sup>](#7) | No | No | No |
| MDVRP    | No | No | No | No | No |
| MVRP    | No | No | No | No | No |


#### References
7. [Interterminal Truck Routing Optimization Using Deep Reinforcement Learning, Taufik Nur Adi, Y. Iskandar, Hyerim Bae (2020)](https://consensus.app/papers/truck-routing-optimization-using-deep-reinforcement-adi/7c02a7b554335993a3e376f418fbd06c/)

8. [Online Multimodal Transportation Planning using Deep Reinforcement Learning, Amirreza Farahani; Laura Genga; Remco Dijkman (2021)](https://ieeexplore.ieee.org/document/9658943)

9. [Optimising Public Bus Transit Networks Using Deep Reinforcement Learning, Ahmed Darwish, Momen Khalil, and Karim Badawi (2021)](https://ieeexplore.ieee.org/document/9294710)

## Phase 3: Framework

### Definition of project keywords : 

- **Multimodal Transportation**
- **Network Design**
- **Scheduling Optimization**
- **Transportation**
- **Network flow**
- **Logistics**
- **Travel Time Prediction**
- **Machine Learning**
- **Deep Learning**
- **Neural Network**
- **Rural Area**
- **Transfert Learning**
- **Constraint**
- **Transfert Learning**
- **IoT**
- **VRP**
- **VRPTW**
- **CVRP**
- **Graph**
- **Data**
- **Graph neural network**
- **Link prediction**
- **GNN**
- **Deep Reinforcement Learning**
- **Recommander system**
- **Q-Learning**
- **Data mining**
- **Policy**
- **Environment**


## Phase 4: Literature search

1. [Graph Neural Networks for Intelligent Transportation Systems: A Survey, Saeed Rahmani ,Asiye Baghbani ,Nizar Bouguila (2023)](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10077454)

2. [Graph Neural Networks for Recommender System, Chen Gao, Xiang Wang, PictureXiangnan He, PictureYong Li (2022)](https://dl.acm.org/doi/pdf/10.1145/3488560.3501396)

3. [Interterminal Truck Routing Optimization Using Deep Reinforcement Learning, Taufik Nur Adi, Y. Iskandar, Hyerim Bae (2020)](https://consensus.app/papers/truck-routing-optimization-using-deep-reinforcement-adi/7c02a7b554335993a3e376f418fbd06c/)


4. [Travel Time Prediction in a Multimodal Freight Transport Relation Using Machine Learning Algorithms, Nikolaos Servos, Xiaodi Liu, Michael Teucke, Michael Freitag (2019)](https://www.mdpi.com/2305-6290/4/1/1)

5. [GMDNet: A Graph-Based Mixture Density Network for Estimating Packages’ Multimodal Travel Time Distribution, Xiaowei Mao, Huaiyu Wan, Haomin Wen, Fan Wu, Jianbin Zheng, Yuting Qiang, Shengnan Guo, Lixia Wu, Haoyuan Hu, Youfang Lin (2023)](https://ojs.aaai.org/index.php/AAAI/article/view/25578)

6.  [Travel Time Prediction by Advanced Neural Network, Lajos Kisgyörgy, Laurence R. Rilett (2002)](https://pp.bme.hu/ci/article/view/617)

7. [Graph neural networks-based scheduler for production planning problems using reinforcement learning MSA Hameed, A Schwung - Journal of Manufacturing Systems, 2023](https://arxiv.org/pdf/2009.03836)

8. [Learning to Optimize Permutation Flow Shop Scheduling via Graph-based Imitation Learning, Longkang Li, Siyuan Liang, Zihao Zhu, Chris Ding, Hongyuan Zha, Baoyuan Wu (2023)](https://arxiv.org/pdf/2210.17178)

9. [Online Multimodal Transportation Planning using Deep Reinforcement Learning, Amirreza Farahani; Laura Genga; Remco Dijkman (2021)](https://ieeexplore.ieee.org/document/9658943)

10. [Optimising Public Bus Transit Networks Using Deep Reinforcement Learning, Ahmed Darwish, Momen Khalil, and Karim Badawi (2021)](https://ieeexplore.ieee.org/document/9294710)


## Phase 5: Conception and planification

#### Plan project implementation

##### Problem modelization :

###### Environment : 
Set the environment, the environment is the state of the graph, here is how we define nodes and arcs in the graph

**Node** :
&rarr; Type : Bus stop, Railway station, Seaport, Airport or Multimodal interconnection (hub)
&rarr; Coordinates : Latitude, Longitude
→ Capacity : Capacity for handling passengers simultaneously
→ Resource Availability : Number of available vehicles, Types of available vehicles (buses, trains, ships, airplanes), Staff level (number of drivers, maintenance personnel, etc.)
→ Operating Hours : Opening and closing hours, Service frequency (interval between departures)

**Arc** :
→ Type : Road, Railway, Canal, Maritime route, Air route
→ Length and Travel Time : Distance in kilometers, Average travel time (including possible variations)
→ Capacity : Maximum number of vehicles that can travel simultaneously, Maximum number of passengers that can be transported simultaneously
→ Traffic Conditions : Congestion level (highly congested, moderately congested, free-flowing), Historical traffic data
→ Infrastructure Quality : Road/track condition (good, average, poor), Presence of tolls or restrictions
→ Safety : Number of reported accidents, Safety level (presence of surveillance, signage, etc.)
→ Usage Cost : Maintenance cost, Usage cost (tolls, fuel costs, maintenance fees)
→ Accessibility : Access restrictions (specific hours, specific vehicles), Accessibility for people with reduced mobility
→ Dynamic Data : Real-time traffic variability, Ongoing incidents (accidents, construction, road closures)

###### Agent : 
Develop the agent, here is a brief description of agent caracteritics

**Algorithm** :
→ Proximal Policy Optimization

**NN architecture** :
→ Graph neural network

**States** :
→ The state is the current configuration of the transport network, including node and arc attributes as described above:

    Nodes: Type, Coordinates, Capacity, Resource Availability, Operating Hours.
    Arcs: Type, Length and Travel Time, Capacity, Traffic Conditions, Infrastructure Quality, Safety, Usage Cost, Accessibility, Dynamic Data. 

**Actions** :
→ Adjust Scheduling: Change the scheduling of vehicles and routes (e.g., rescheduling departure times, adjusting service frequencies).
→ Resource Allocation: Reallocate vehicles and staff to different parts of the network to optimize performance (e.g., assigning more buses during peak hours, redistributing maintenance personnel).

**Rewards** :
→ Minimize Total Travel Time: Reward the agent for reducing the overall travel time across the network.
→ Maximize Passenger Satisfaction: Reward for reducing wait times, avoiding overcrowding, and improving overall service quality.
→ Minimize Operational Costs: Include factors like fuel costs, maintenance expenses, and toll fees.
→ Enhance Accessibility: Ensure compliance with accessibility requirements and reward efforts to reduce congestion and improve accessibility for all users.

**Exploration strategy** :
→ Noisy Network : Encourage the exploration of diverse strategies

## Phase 6: Prototype development
Implement a first version of the project

## Phase 7: Train and test
Train the model and assess performance

## Phase 8: Improve
Improving and fine-tuning modeling


# Project gantt chart :

<p align="center">
  <img src="https://github.com/JonasBlx/transport_system_control/blob/main/figures/project_gantt.png" alt="Project gantt chart">
</p>


-- 

<p align="center">
  <img src="https://github.com/JonasBlx/transport_system_control/blob/main/figures/from%20Understanding%20Graph%20Neural%20Networks%20Part1%20by%20DeepFindr.png" alt="Edge prediction example">
</p>

- Predict new edges between nodes (i.e. new routes between points to be served) to optimize the graph.
- (Harder) Predict new nodes and new edges to optimize the graph.

* Scheduling :
Each node has a set of features and the scheduling constraints are "hard constraints".