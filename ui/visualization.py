# ui/visualization.py
import matplotlib.pyplot as plt

def render_simulation(sim, fig=None):
    """
    Render particle simulation.
    If fig is provided, reuse it to avoid creating a new figure each step.
    """
    if fig is None:
        fig, ax = plt.subplots(figsize=(6,4))
    else:
        ax = fig.axes[0] if fig.axes else fig.add_subplot(111)
        ax.clear()  # clear previous plot

    # Plot setup
    ax.set_xlim(0, sim.width)
    ax.set_ylim(0, sim.height)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('#f0f0f0')

    # Enzymes
    ax.scatter([e.x for e in sim.enzymes],
               [e.y for e in sim.enzymes],
               s=40, c='blue', marker='o', label='Enzyme')

    # Substrates
    ax.scatter([s.x for s in sim.substrates],
               [s.y for s in sim.substrates],
               s=20, c='green', marker='s', label='Substrate')

    # Products
    ax.scatter([p.x for p in sim.products],
               [p.y for p in sim.products],
               s=15, c='red', marker='^', label='Product')

    # ES Complexes
    if sim.complexes:
        ax.scatter([c.x for c in sim.complexes],
                   [c.y for c in sim.complexes],
                   s=80, c='purple', marker='*', label='ES Complex')

    ax.legend(loc='upper right', fontsize=8)

    return fig
