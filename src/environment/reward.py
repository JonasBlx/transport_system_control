import numpy as np

class RewardCalculator:
    def __init__(self, weight_mean=0.7, weight_std=0.3, alpha=0.1, beta=0.1):
        """
        Initialise le calculateur de récompense avec les poids et paramètres spécifiés pour 
        la moyenne et l'écart-type des demandes.
        
        Args:
        - weight_mean (float): Poids attribué à la demande moyenne dans le calcul de la récompense.
        - weight_std (float): Poids attribué à l'écart-type des demandes dans le calcul de la récompense.
        - alpha (float): Paramètre de décroissance exponentielle pour la moyenne.
        - beta (float): Paramètre de décroissance exponentielle pour l'écart-type.
        """
        self.weight_mean = weight_mean
        self.weight_std = weight_std
        self.alpha = alpha
        self.beta = beta

    def calculate_reward(self, demands):
        """
        Calcule la récompense basée sur la moyenne et l'écart-type des demandes.
        La récompense est plus élevée quand la moyenne est basse et l'écart-type est faible.
        
        Args:
        - demands (np.array): Un tableau numpy contenant les demandes de chaque noeud.
        
        Returns:
        - float: La valeur de la récompense calculée.
        """
        if len(demands) == 0:
            return 0  # Gestion du cas où le tableau serait vide

        # Calcul de la moyenne et de l'écart-type
        mean_demand = np.mean(demands)
        std_demand = np.std(demands)

        # Calcul de la récompense en utilisant la décroissance exponentielle
        mean_reward = np.exp(-self.alpha * mean_demand)
        std_reward = np.exp(-self.beta * std_demand)

        # Ponderation des récompenses avec les poids spécifiés
        total_reward = self.weight_mean * mean_reward + self.weight_std * std_reward

        return total_reward

# Exemple d'utilisation
reward_calculator = RewardCalculator(weight_mean=0.7, weight_std=0.3, alpha=0.1, beta=0.1)
demands = np.array([10, 20, 30, 40, 50])
reward = reward_calculator.calculate_reward(demands)
print("Calculated Reward:", reward)
