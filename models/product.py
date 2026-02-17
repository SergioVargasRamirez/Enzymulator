# models/product.py
from .particle import Particle

class Product(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, radius=6, speed=6.0)
