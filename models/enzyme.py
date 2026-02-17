from .particle import Particle

class Enzyme(Particle):
    def __init__(self, x, y, km, optimal_temp, optimal_pH):
        super().__init__(x, y, radius=4, speed=2.0)
        self.km = km
        self.optimal_temp = optimal_temp
        self.optimal_pH = optimal_pH
        self.bound = False  # <-- enzyme is free by default
