import numpy as np
import matplotlib.pyplot as plt

weight = 0.01
# Définir la fonction
def f(x,weight):
    return np.exp(-weight * x)

# Générer des données x
x = np.linspace(0, 400, 1000)
y = f(x,weight)
# Création du graphique
plt.figure(figsize=(10, 6))
plt.plot(x, y, label=f'f(x) = exp(-{weight}*x)', color='blue')
plt.title(f'Graph of f(x) = exp(-{weight}*x)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()
plt.show()
