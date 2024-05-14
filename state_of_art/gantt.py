# Create a color gradient without yellow (viridis is already a good choice, but we'll avoid the lightest color)
colors = plt.cm.viridis(np.linspace(0, 0.9, len(phases)))

# Create a Gantt chart with color gradient
fig, ax = plt.subplots(figsize=(10, 6))

# Add bars for each phase, in reverse order to have the earliest at the top, with different colors
for i, ((phase, (start, end)), color) in enumerate(zip(reversed(list(phases.items())), colors)):
    ax.broken_barh([(start, end-start)], (i-0.4, 0.8), facecolors=color)
    ax.text(start - 0.5, i, phase, ha='right', va='center', color=color, fontsize=10, weight='bold')

# Customize the chart
ax.set_yticks(range(len(phases)))
ax.set_yticklabels([''] * len(phases))  # Remove the labels on the y-axis
ax.set_xticks(range(17))
ax.set_xticklabels(range(17))
ax.set_xlabel('Weeks')
ax.set_title('Project Gantt Chart')

plt.show()
