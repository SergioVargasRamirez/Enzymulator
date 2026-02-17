# simulation/engine.py

import numpy as np
from simulation.collision import check_collision
from models.product import Product
from models.complex import ESComplex
from kinetics.modifiers import activity_modifier

def step_simulation(sim):
    """
    Perform one simulation step:
    - Move all particles (with temperature-dependent speed)
    - Bind free enzymes to substrates
    - Catalyze product formation
    - Track per-step product and sampled histories
    """

    # --- Compute speed factor from temperature ---
    speed_factor = sim.base_speed * sim.temperature_speed_factor()

    # --- Move all particles ---
    for p in sim.enzymes + sim.substrates + sim.products:
        p.move(sim.width, sim.height, speed_factor)

    # --- Enzyme-substrate binding ---
    for enzyme in list(sim.enzymes):
        if enzyme.bound:
            continue  # skip busy enzymes

        for substrate in list(sim.substrates):
            if check_collision(enzyme, substrate):
                # Activity modifier based on temperature/pH
                act = activity_modifier(enzyme, sim.environment)
                bind_prob = 0.2 * act * sim.kinetic_model.binding_modifier(sim)

                if np.random.rand() < bind_prob:
                    # Form complex
                    sim.substrates.remove(substrate)
                    enzyme.bound = True
                    sim.complexes.append(ESComplex(enzyme))

                    break  # one substrate per enzyme

    # --- Catalysis step ---
    product_formed_this_step = 0

    for complex in list(sim.complexes):
        act = activity_modifier(complex.enzyme, sim.environment)
        cat_prob = 0.1 * act * sim.kinetic_model.catalysis_modifier(sim)

        if np.random.rand() < cat_prob:
            # Product formation
            sim.complexes.remove(complex)
            complex.enzyme.bound = False
            sim.products.append(Product(complex.x, complex.y))
            product_formed_this_step += 1

    # --- Update time and histories ---
    sim.time += 1
    sim.time_history.append(sim.time)
    sim.product_history.append(len(sim.products))
    sim.rate_history.append(product_formed_this_step)  # per-step production

    # --- Sampling every N steps for statistics ---
    sim.step_counter += 1
    if sim.step_counter % sim.sample_interval == 0:
        sim.history_time_sampled.append(sim.time)
        sim.history_product_sampled.append(len(sim.products))
