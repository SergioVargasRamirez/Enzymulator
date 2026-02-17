import numpy as np

class Particle:
    def __init__(self, x, y, radius=5, speed=1.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed  # base scale of random motion

    def move(self, width, height, speed_factor=1.0):
        """
        Move particle randomly within bounds.
        speed_factor multiplies the base speed (for temperature effects).
        """
        dx = np.random.uniform(-1, 1) * self.speed * speed_factor
        dy = np.random.uniform(-1, 1) * self.speed * speed_factor
        self.x = np.clip(self.x + dx, 0, width)
        self.y = np.clip(self.y + dy, 0, height)
