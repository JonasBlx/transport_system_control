import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Define the phases and their durations
phases = {
    'Phase 1: Understanding the project': (0, 1),
    'Phase 2: Choice of solution to be explored': (0, 2),
    'Phase 3: Framework': (1, 3),
    'Phase 4: Literature search': (1, 3),
    'Phase 5: Conception and planification': (2, 4),
    'Phase 6: Prototype development': (4, 11),
    'Phase 7: Train and test': (11, 12),
    'Phase 8: Improve': (12, 16)
}

# Create a color gradient without yellow (viridis is already a good choice, but we'll avoid the lightest color)
colors = plt.cm.viridis(np.linspace(0, 0.9, len(phases)))

# Create a Gantt chart with color gradient
fig, ax = plt.subplots(figsize=(12, 6))

# Add bars for each phase, in reverse order to have the earliest at the top, with different colors
for i, ((phase, (start, end)), color) in enumerate(zip(reversed(list(phases.items())), colors)):
    ax.broken_barh([(start, end-start)], (i-0.4, 0.8), facecolors=color)
    ax.text(end + 0.5, i, phase, ha='left', va='center', color=color, fontsize=9, weight='bold')

# Customize the chart
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([''] * len(phases))  # Remove the labels on the y-axis
ax.set_xticks(range(21))
ax.set_xticklabels(range(21))
ax.set_xlim(0, 20)  # Extend the x-axis limit to 20
ax.set_xlabel('Weeks')
ax.set_title('Project Gantt Chart')

plt.show()
