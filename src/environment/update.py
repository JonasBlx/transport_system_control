import numpy as np
from scipy.stats import norm

# Paramètres réalistes pour les gaussiennes
mu = [2, 2, 2, 2, 4, 6, 8, 10, 10, 10, 8, 6, 4, 2, 2, 2, 2, 4, 6, 8, 10, 8, 6, 4]  # Demande moyenne avec pics matin et soir
sigma = 1.5  # Écart type fixe pour toutes les heures

def additional_demand(hour):
    """
    Calcule la demande additionnelle pour une heure donnée en utilisant des gaussiennes différentes.
    
    Args:
    - hour (int): L'heure pour laquelle calculer la demande additionnelle (doit être entre 0 et 23 inclus).
    
    Returns:
    - float: La demande additionnelle calculée à partir d'une gaussienne.
    """
    if hour < 0 or hour >= 24:
        raise ValueError("L'heure doit être entre 0 et 23 inclus.")

    # Calculer la demande additionnelle
    # Nous utilisons une gaussienne centrée sur mu_hour avec un écart type de sigma_hour
    demand = norm.pdf(hour, mu[hour], sigma)
    
    if demand < 0:
        demand = int(0)
        return demand

    return round(demand)

# Exemple d'utilisation
if __name__ == "__main__":
    for hour in range(24):
        print(f"Demande additionnelle à {hour}h: {additional_demand(hour)}")


