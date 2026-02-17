import numpy as np

def check_collision(p1, p2):
    dist = np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
    return dist < (p1.radius + p2.radius)
