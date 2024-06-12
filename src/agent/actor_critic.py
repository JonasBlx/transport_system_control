import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool

class ActorCritic(nn.Module):
    def __init__(self, input_dim, num_gnn_layers, units_per_gnn_layer, num_lstm_layers, units_per_lstm_layer, actor_output_dim, critic_output_dim):
        super(ActorCritic, self).__init__()

        # Définir les couches de GNN pour l'actor
        self.actor_convs = nn.ModuleList()
        for i in range(num_gnn_layers):
            in_channels = input_dim if i == 0 else units_per_gnn_layer
            self.actor_convs.append(GCNConv(in_channels, units_per_gnn_layer))

        # Couches LSTM partagées
        self.shared_lstm = nn.LSTM(input_size=input_dim, hidden_size=units_per_lstm_layer, num_layers=num_lstm_layers // 2, batch_first=True)

        # Couches LSTM séparées pour l'actor
        self.actor_lstm = nn.LSTM(input_size=units_per_lstm_layer, hidden_size=units_per_lstm_layer, num_layers=num_lstm_layers // 2, batch_first=True)

        # Couches LSTM séparées pour le critic
        self.critic_lstm = nn.LSTM(input_size=units_per_lstm_layer, hidden_size=units_per_lstm_layer, num_layers=num_lstm_layers // 2, batch_first=True)

        # Têtes de réseau pour l'actor et le critic
        self.actor_head = nn.Linear(units_per_lstm_layer, actor_output_dim)
        self.critic_head = nn.Linear(units_per_lstm_layer, critic_output_dim)

    def forward(self, graph_data, sequence_data):
        x, edge_index, batch = graph_data.x, graph_data.edge_index, graph_data.batch
        
        # Passer les données de graphe à travers les GNN
        for conv in self.actor_convs:
            x = F.relu(conv(x, edge_index))
        x = global_mean_pool(x, batch)  # Réduire les caractéristiques des nœuds à des caractéristiques de graphe

        # Passer les données séquentielles à travers les LSTM partagés
        shared_lstm_out, _ = self.shared_lstm(sequence_data)
        
        # Passer la sortie des LSTM partagés aux LSTM spécifiques à l'actor
        actor_lstm_out, _ = self.actor_lstm(shared_lstm_out)
        
        # Passer la sortie des LSTM partagés aux LSTM spécifiques au critic
        critic_lstm_out, _ = self.critic_lstm(shared_lstm_out)

        # Générer des probabilités d'action et des valeurs d'état
        action_probs = F.softmax(self.actor_head(actor_lstm_out[:, -1, :]), dim=-1)
        state_value = self.critic_head(critic_lstm_out[:, -1, :])

        return action_probs, state_value

# Paramètres de l'architecture
input_dim = 10
num_gnn_layers = 2
units_per_gnn_layer = 16
num_lstm_layers = 4
units_per_lstm_layer = 32
actor_output_dim = 4
critic_output_dim = 1

# Créer le modèle
model = ActorCritic(input_dim, num_gnn_layers, units_per_gnn_layer, num_lstm_layers, units_per_lstm_layer, actor_output_dim, critic_output_dim)

# Données factices (remplacer par des données réelles adaptées)
graph_data = type('GraphData', (object,), {'x': torch.rand(10, input_dim), 'edge_index': torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]]), 'batch': torch.tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])})
sequence_data = torch.rand(1, 5, input_dim)  # Taille de lot de 1, longueur de séquence de 5

# Passer les données à travers le modèle
action_probs, state_value = model(graph_data, sequence_data)
