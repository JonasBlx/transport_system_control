# Problem Description

## State
- **Statistical Data**: Current graph configuration, including the structure of nodes and arcs, and the capacities of each node and arc.
- **Dynamic Data**: Customer requests at each node, current location of vehicles, vehicle status (whether they are en route or not), and current demand.

## Action
Generate a new schedule for the departures and routes of trucks. This involves deciding for each vehicle when it departs, from which node, to which node, and possibly the route it takes.

## Action Space
All possible schedules for the vehicles. This includes all combinations of departures, routes, and timings.

## Transition Function
Update the schedule of vehicles. This involves moving vehicles on the graph according to the generated schedule and updating the dynamic state (vehicle positions, satisfied demands, etc.).

## Reward
- **Primary Objective**: Minimize unsatisfied demand (high weight).
- **Secondary Objective**: Minimize the standard deviation between the demands of different nodes (low weight).

## Initial State
No vehicle has started, and there is an initial demand.

## Horizon
Infinite, meaning the problem continues indefinitely with evolving demand over time.
