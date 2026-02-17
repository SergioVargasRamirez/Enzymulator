import numpy as np
from models.enzyme import Enzyme
from models.substrate import Substrate

class SimulationState:
    def __init__(self, model):
        self.model = model

        # --- Environment ---
        self.environment = {"temperature": 37, "pH": 7.0}
        self.kinetic_model = model

        # --- Particle counts ---
        self.enzyme_count = 10
        self.substrate_count = 100
        self.inhibitor_count = 0

        # --- Simulation space ---
        self.width = 200
        self.height = 100

        # --- Time & step counters ---
        self.time = 0
        self.step_counter = 0
        self.sample_interval = 50  # sample every 50 steps

        # --- Particles ---
        self.enzymes = []
        self.substrates = []
        self.products = []
        self.complexes = []

        # --- History tracking ---
        self.time_history = []
        self.product_history = []
        self.rate_history = []

        # --- Sampled histories for stats ---
        self.history_time_sampled = []
        self.history_product_sampled = []

        # --- Default enzyme parameters ---
        self.default_km = 0.5
        self.default_optimal_temp = 37
        self.default_optimal_pH = 7.0

        # --- Base particle speed ---
        self.base_speed = 1.0

        # --- Initialize particles ---
        self.initialize_particles()

    def initialize_particles(self):
        """Create enzyme and substrate particles with random positions."""

        # --- Enzymes ---
        self.enzymes = [
            Enzyme(
                x=np.random.uniform(0, self.width),
                y=np.random.uniform(0, self.height),
                km=self.default_km,
                optimal_temp=self.default_optimal_temp,
                optimal_pH=self.default_optimal_pH
            )
            for _ in range(self.enzyme_count)
        ]

        # --- Substrates ---
        self.substrates = [
            Substrate(
                x=np.random.uniform(0, self.width),
                y=np.random.uniform(0, self.height)
            )
            for _ in range(self.substrate_count)
        ]

        # --- Reset products and complexes ---
        self.products = []
        self.complexes = []

    def update_environment(self, config):
        """
        Update environment and enzyme parameters from controls.
        config = dict from tab_controls
        """
        # Update temperature and pH
        self.environment["temperature"] = config.get("temperature", 37)
        self.environment["pH"] = config.get("pH", 7.0)

        # Update default enzyme properties
        self.default_km = config.get("km", self.default_km)
        self.default_optimal_temp = config.get("optimal_temp", self.default_optimal_temp)
        self.default_optimal_pH = config.get("optimal_pH", self.default_optimal_pH)

    def temperature_speed_factor(self):
        """
        Compute particle speed factor based on temperature.
        Faster at higher temperatures, slower at lower temperatures.
        """
        temp_diff = self.environment["temperature"] - self.default_optimal_temp
        factor = 1.0 + 0.05 * temp_diff  # 5% speed change per degree
        return max(factor, 0.1)  # minimum speed to prevent zero or negative
