# models/substrate.py
from .particle import Particle

class Substrate(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, radius=2, speed=4.0)  # moves faster
