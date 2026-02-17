import streamlit as st
import time
import matplotlib.pyplot as plt

from simulation.state import SimulationState
from simulation.engine import step_simulation
from kinetics.base_model import NoInhibitorModel
from kinetics.competitive import CompetitiveModel
from kinetics.noncompetitive import NonCompetitiveModel
from ui.controls import tab_controls
from ui.visualization import render_simulation
from ui.plots import render_plot_and_table

# ---------------------------------------------------
# Page setup
# ---------------------------------------------------
st.set_page_config(layout="wide")
st.title("Enzyme Kinetics Particle Simulator")

# ---------------------------------------------------
# Helper to render table larger
# ---------------------------------------------------
def render_html_table(df, font_size=18):
    html = df.to_html(index=True)
    return f"""
    <div style="font-size:{font_size}px">
        {html}
    </div>
    """

#simulator mode
advanced = st.toggle("Advanced Mode")

# ---------------------------------------------------
# Tabs and models
# ---------------------------------------------------
if advanced:
    tab_labels = ["No Inhibitor", "Competitive", "Non-Competitive"]
    models = {
        "No Inhibitor": NoInhibitorModel(),
        "Competitive": CompetitiveModel(),
        "Non-Competitive": NonCompetitiveModel()
    }
else:
    tab_labels = ["No Inhibitor"]
    models = {
        "No Inhibitor": NoInhibitorModel()
    }

tabs = st.tabs(tab_labels)

# ---------------------------------------------------
# Main tab loop
# ---------------------------------------------------
for tab, label in zip(tabs, tab_labels):
    with tab:

        sim_key = f"sim_{label}"
        start_key = f"start_{label}"

        # Initialize simulation state
        if sim_key not in st.session_state:
            st.session_state[sim_key] = SimulationState(models[label])

        sim = st.session_state[sim_key]

        # Layout columns
        col_sim, col_right = st.columns([2, 1])

        with col_sim:
            sim_placeholder = st.empty()

        with col_right:
            plot_placeholder = st.empty()
            table_placeholder = st.empty()

        # ---------------------------------------------------
        # Controls (ONLY called once!)
        # ---------------------------------------------------
        config = tab_controls(label)

        # ---------------------------------------------------
        # Handle Clean (clears screen only)
        # ---------------------------------------------------
        if config.get("clean", False):

            #reset simulation state
            st.session_state[sim_key] = SimulationState(models[label])

            sim_placeholder.empty()
            plot_placeholder.empty()
            table_placeholder.empty()

            if f"fig_sim_{label}" in st.session_state:
                del st.session_state[f"fig_sim_{label}"]
            if f"fig_plot_{label}" in st.session_state:
                del st.session_state[f"fig_plot_{label}"]

            st.session_state[start_key] = False

            st.success("Simulator reset! Remember to modify the settings before running your next simulation!!!")
            st.stop()


        # ---------------------------------------------------
        # Update simulation parameters
        # ---------------------------------------------------
        sim.update_environment(config)
        sim.enzyme_count = config["enzyme_count"]
        sim.substrate_count = config["substrate_count"]

        if label != "No Inhibitor":
            sim.inhibitor_count = config["inhibitor"]
        else:
            sim.inhibitor_count = 0

        # Reinitialize particles if counts changed
        if (
            sim.enzyme_count != len(sim.enzymes)
            or sim.substrate_count != len(sim.substrates)
        ):
            sim.initialize_particles()

        # --- Only run simulation if Start pressed ---
        if config.get("start", False):

            # --- Clean simulation data (keep user-selected parameters) ---
            sim.initialize_particles()        # re-generate enzyme & substrate positions
            sim.products = []
            sim.complexes = []
            sim.time = 0
            sim.step_counter = 0
            sim.time_history = []
            sim.product_history = []
            sim.rate_history = []
            sim.history_time_sampled = []
            sim.history_product_sampled = []
    
            # Clear placeholders
            sim_placeholder.empty()
            plot_placeholder.empty()
            table_placeholder.empty()
    
            # Delete figures so new ones are created
            if f"fig_sim_{label}" in st.session_state:
                del st.session_state[f"fig_sim_{label}"]
            if f"fig_plot_{label}" in st.session_state:
                del st.session_state[f"fig_plot_{label}"]

            # Reset start flag to prevent loops from overlapping
            st.session_state[start_key] = True

            # Reload sim reference
            sim = st.session_state[sim_key]

            # --- Initialize reusable figures ---
            st.session_state[f"fig_sim_{label}"], _ = plt.subplots(figsize=(6, 4))
            st.session_state[f"fig_plot_{label}"], _ = plt.subplots()
    
            # --- Continuous simulation loop ---
            running = True
            plateau_threshold = 1        # minimal products per interval
            plateau_intervals = 2        # consecutive low-activity intervals

            while running:
                step_simulation(sim)

                # Particle animation
                fig_sim = render_simulation(sim, fig=st.session_state[f"fig_sim_{label}"])
                sim_placeholder.pyplot(fig_sim)

                # Product plot + stats table
                fig_plot, df_stats = render_plot_and_table(sim, fig=st.session_state[f"fig_plot_{label}"])
                plot_placeholder.pyplot(fig_plot)
                table_placeholder.markdown(
                    render_html_table(df_stats, font_size=18),
                    unsafe_allow_html=True
                )

                # Plateau stop rule
                if len(sim.history_product_sampled) >= plateau_intervals + 1:
                    recent_samples = sim.history_product_sampled[-(plateau_intervals + 1):]
                    diffs = [recent_samples[i+1] - recent_samples[i] for i in range(plateau_intervals)]
                    if all(diff <= plateau_threshold for diff in diffs):
                        running = False
                        st.success("Simulation finished: product formation plateau reached.")

                # Stop if all substrate consumed
                if len(sim.substrates) == 0:
                    running = False
                    st.success("Simulation finished: all substrates consumed.")

            time.sleep(0.05)
