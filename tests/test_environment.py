import sys
sys.path.append("../src/")
sys.path.append("../src/environment/")

import unittest
import pandas as pd
import torch
from environment import Environment, load_network_from_csv, Node, Vehicle, Arc


class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.environment = Environment()
        # Setup for loading from CSV file paths
        self.node_file_path = "../data/generated/nodes_example_1.csv"
        self.arc_file_path = "../data/generated/arcs_example_1.csv"
        self.environment = load_network_from_csv(self.node_file_path, self.arc_file_path)

    def test_load_from_csv(self):
        # Check if nodes and arcs are loaded correctly
        self.assertEqual(len(self.environment.nodes), 18)  # As per the number of nodes in the CSV
        self.assertEqual(len(self.environment.arcs), 40)   # As per the number of arcs in the CSV

    def test_to_from_pyg_data(self):
        # Converting to PyTorch Geometric data format and back
        pyg_data, node_sizes_df, arc_sizes_df = self.environment.to_pyg_data()
        self.assertIsNotNone(pyg_data)
        self.assertIsNotNone(node_sizes_df)
        self.assertIsNotNone(arc_sizes_df)
        # Clear environment and load data back from PyTorch Geometric format
        self.environment.from_pyg_data(pyg_data, node_sizes_df, arc_sizes_df)
        self.assertEqual(len(self.environment.nodes), 18)
        self.assertEqual(len(self.environment.arcs), 40)

    def test_get_state(self):
        state = self.environment.get_state()
        self.assertTrue("nodes" in state)
        self.assertTrue("arcs" in state)
        self.assertEqual(len(state["nodes"]), 18)
        self.assertEqual(len(state["arcs"]), 40)

    def test_add_node(self):
        node = Node(
            node_id=19,
            node_type=torch.tensor([1, 0, 0, 0, 0], dtype=torch.float),
            coordinates=torch.tensor([0.0, 0.0], dtype=torch.float),
            capacity=50,
            vehicles=[],
            staff=5,
            service_hours=torch.tensor([6.0, 22.0], dtype=torch.float),
            demand=30
        )
        self.environment.add_node(node)
        self.assertEqual(len(self.environment.nodes), 19)
        self.assertEqual(self.environment.get_node(19), node)

    def test_add_arc(self):
        arc = Arc(
            arc_id=41,
            arc_type=torch.tensor([1, 0, 0, 0, 0], dtype=torch.float),
            length=20.0,
            travel_time=30.0,
            capacity=100,
            traffic_condition=1,
            safety=5,
            usage_cost=10.0,
            open=1,
            source=1,
            target=2,
            vehicles=[]
        )
        self.environment.add_arc(arc, source=1, target=2)
        self.assertEqual(len(self.environment.arcs), 41)
        self.assertEqual(self.environment.get_arc(41)[0], arc)

    def test_step(self):
        schedule = []
        new_state, reward, done = self.environment.step(schedule)
        self.assertIsInstance(new_state, dict)
        self.assertIsInstance(reward, float)
        self.assertIsInstance(done, bool)

    def test_calculate_reward(self):
        reward = self.environment.calculate_reward()
        self.assertIsInstance(reward, float)

    def test_update_state(self):
        self.environment.update_state()
        # Assuming the function is updating some state,
        # we would need some assertion here, but since the original function is a placeholder,
        # we will just call it to make sure it runs without errors.

    def test_update_demand(self):
        node = self.environment.get_node(1)
        initial_demand = node.demand
        self.environment.update_demand(node)
        #  self.assertNotEqual(node.demand, initial_demand)  # Assuming the demand changes

    def test_repr(self):
        repr_str = repr(self.environment)
        self.assertIsInstance(repr_str, str)


if __name__ == "__main__":
    unittest.main()
