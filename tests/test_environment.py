# test_environment.py

import unittest
from environment.environment import TransportNetwork
from src.environment.nodes import Node
from src.environment.arcs import Arc
import torch

class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.network = TransportNetwork()
        self.node1 = Node(
            node_id="N1",
            node_type="Bus Stop",
            coordinates=(48.8566, 2.3522),
            capacity=100,
            resources={"vehicles": 5, "staff": 2},
            operating_hours=(6, 22)
        )
        self.node2 = Node(
            node_id="N2",
            node_type="Railway Station",
            coordinates=(48.8588, 2.3200),
            capacity=300,
            resources={"vehicles": 10, "staff": 5},
            operating_hours=(5, 23)
        )
        self.arc = Arc(
            arc_id="A1",
            arc_type="Road",
            length=15.5,
            travel_time=30,
            capacity=100,
            traffic_conditions="moderately congested",
            infrastructure_quality="good",
            safety="low accident rate",
            usage_cost=2.5,
            accessibility="no restrictions",
            dynamic_data={"current_traffic": "free-flowing", "incidents": "none"}
        )

    def test_add_node(self):
        self.network.add_node(self.node1)
        self.assertEqual(len(self.network.nodes), 1)
        self.network.add_node(self.node2)
        self.assertEqual(len(self.network.nodes), 2)
        self.assertIn("N1", self.network.nodes)
        self.assertIn("N2", self.network.nodes)

    def test_add_arc(self):
        self.network.add_node(self.node1)
        self.network.add_node(self.node2)
        self.network.add_arc(self.arc, "N1", "N2")
        self.assertEqual(len(self.network.arcs), 1)
        self.assertIn("A1", self.network.arcs)
        self.assertEqual(self.network.arcs["A1"][1], "N1")
        self.assertEqual(self.network.arcs["A1"][2], "N2")

    def test_network_state(self):
        self.network.add_node(self.node1)
        self.network.add_node(self.node2)
        self.network.add_arc(self.arc, "N1", "N2")
        state = self.network.get_state()
        self.assertIn("nodes", state)
        self.assertIn("arcs", state)
        self.assertEqual(len(state["nodes"]), 2)
        self.assertEqual(len(state["arcs"]), 1)

    def test_apply_action_update_capacity(self):
        self.network.add_node(self.node1)
        action = {
            "type": "update_node_capacity",
            "node_id": "N1",
            "new_capacity": 120
        }
        self.network.apply_action(action)
        self.assertEqual(self.network.get_node("N1").get_capacity(), 120)

    def test_apply_action_update_dynamic_data(self):
        self.network.add_node(self.node1)
        self.network.add_node(self.node2)
        self.network.add_arc(self.arc, "N1", "N2")
        action = {
            "type": "update_arc_dynamic_data",
            "arc_id": "A1",
            "key": "current_traffic",
            "value": "highly congested"
        }
        self.network.apply_action(action)
        self.assertEqual(self.network.get_arc("A1")[0].get_dynamic_data()["current_traffic"], "highly congested")

    def test_to_pyg_data(self):
        self.network.add_node(self.node1)
        self.network.add_node(self.node2)
        self.network.add_arc(self.arc, "N1", "N2")
        pyg_data = self.network.to_pyg_data()
        
        # Check node features
        self.assertEqual(pyg_data.num_nodes, 2)
        self.assertTrue(torch.equal(pyg_data.x, torch.tensor([[100], [300]], dtype=torch.float)))

        # Check edge indices
        self.assertEqual(pyg_data.num_edges, 1)
        self.assertTrue(torch.equal(pyg_data.edge_index, torch.tensor([[0], [1]], dtype=torch.long)))

        # Check edge attributes
        self.assertTrue(torch.equal(pyg_data.edge_attr, torch.tensor([[15.5, 30.0]], dtype=torch.float)))

if __name__ == "__main__":
    unittest.main()
