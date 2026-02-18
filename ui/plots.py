import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def render_plot_and_table(sim, fig=None):
    """Plot product vs time and compute statistics over sampled intervals."""

    # --- Create or reuse figure ---
    if fig is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    else:
        ax = fig.axes[0] if fig.axes else fig.add_subplot(111)
        ax.clear()

    # --- Plot product vs time ---
    ax.plot(sim.time_history, sim.product_history, color="green")
    ax.set_xlabel("Time")
    ax.set_ylabel("Product")
    ax.set_title("Product vs Time")
    ax.grid(True)

    # --- Create raw time-course dataframe (THIS IS NEW) ---
    df_progress = pd.DataFrame({
        "Time": sim.history_time_sampled,
        "Product": sim.history_product_sampled
    })

    # --- Compute statistics for sampled intervals ---
    if sim.history_product_sampled:
        interval_production = np.diff([0] + sim.history_product_sampled)

        stats = {
            "Min": np.min(interval_production),
            "Mean": np.mean(interval_production),
            "Std Dev": np.std(interval_production),
            "Max": np.max(interval_production)
        }

        df_stats = pd.DataFrame(stats, index=["Products per 50 steps"])
    else:
        df_stats = pd.DataFrame(
            {"Min": [0], "Mean": [0], "Std Dev": [0], "Max": [0]},
            index=["Products per 50 steps"]
        )

    # --- Return THREE objects now ---
    return fig, df_stats, df_progress
