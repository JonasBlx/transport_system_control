# transport_system_control

State : Graph + a customer request for every node, vehicles locations.
State space : Static data. Dynamic data : possible customer requests, for any vehicle; in journey or not ? Possible locations for any vehicle.
Action : Generate a new schedule
Action space : Possible schedules.
Transmission function : Update the scheduling
Reward : Minimize the demand (high weight) and the standard deviation between demands (low weight)
Initial state : No vehicle started and a demand
Horizon : infinite

Demand : evolve through time