import torch
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool
import torch.nn.functional as F
import torch_geometric.transforms as T
from torch.nn import Linear

class GraphEmbedder(torch.nn.Module):
    def __init__(self, input_node_feature_size, output_feature_size):
        super(GraphEmbedder, self).__init__()
        self.input_node_feature_size = input_node_feature_size
        self.output_feature_size = output_feature_size
        self.conv1 = GCNConv(input_node_feature_size, 2 * output_feature_size)
        self.conv2 = GCNConv(2 * output_feature_size, output_feature_size)
        self.transform = T.Compose([T.NormalizeFeatures(), T.NormalizeScale()])

    def forward(self, data):
        # Normalisation et échelle des caractéristiques des nœuds
        data = self.transform(data)

        # Padding des caractéristiques des nœuds si nécessaire
        if data.x.size(1) < self.input_node_feature_size:
            padding = torch.zeros((data.num_nodes, self.input_node_feature_node - data.x.size(1)))
            data.x = torch.cat([data.x, padding], dim=1)
        elif data.x.size(1) > self.input_node_feature_size:
            data.x = data.x[:, :self.input_node_feature_size]

        # Application des couches GCN
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))

        # Pooling pour obtenir une représentation globale du graphe
        x = global_mean_pool(x, data.batch)  # Assurez-vous que data.batch est bien défini si vous traitez un lot de graphes

        return x

    def prepare_graph(self, graph):
        # Assurez-vous que le graphe a des attributs 'x' et 'edge_index'
        if graph.x is None:
            graph.x = torch.zeros((graph.num_nodes, self.input_node_feature_size))
        return self.forward(graph)
