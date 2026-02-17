class ESComplex:
    def __init__(self, enzyme, radius=9):
        self.enzyme = enzyme  # reference to bound enzyme
        self.radius = radius

    @property
    def x(self):
        return self.enzyme.x

    @property
    def y(self):
        return self.enzyme.y
