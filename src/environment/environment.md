The environment consist in a dynamic graph composed of nodes and arcs with vehicles transporting packages or people.

Each vehicle as an ID and is either on a node or on an arc. Package or people ID is an attribute of the vehicle, we also know at any time the remaining capacity of the vehicle

Each node has all the other nodes in attributes to know the demand for each one starting from.

penser à modéliser l'

à partir du livre : détailler les différents composants, 

l'environnement a la fonction step, prend une action et un état pour renvoyer un état et une récompense
que sont les états, les rewards, les actions

comment on prend la décision ? on met à jour les trajet
pas de temps = évolution des décisions

reward : distance totale


Chaque véhicule de notre simulation à un ID et est un attribut du noeud/arc sur lequel il se trouve. Aussi, il a une variable prochain départ.


https://pytorch-geometric.readthedocs.io/en/latest/notes/heterogeneous.html

https://github.com/wouterkool/attention-learn-to-route

https://github.com/ai4co/rl4co <<

https://github.com/cpwan/RLOR