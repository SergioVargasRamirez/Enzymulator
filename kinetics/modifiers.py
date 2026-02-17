import numpy as np

def temperature_modifier(enzyme, env):
    sigma = 5
    temp = env["temperature"]        # use key instead of attribute
    return np.exp(-((temp - enzyme.optimal_temp) ** 2) / (2 * sigma ** 2))

def ph_modifier(enzyme, env):
    sigma = 0.8
    pH = env["pH"]                  # use key instead of attribute
    return np.exp(-((pH - enzyme.optimal_pH) ** 2) / (2 * sigma ** 2))

def activity_modifier(enzyme, env):
    return temperature_modifier(enzyme, env) * ph_modifier(enzyme, env)
