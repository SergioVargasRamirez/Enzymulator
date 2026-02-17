class NonCompetitiveModel:
    Ki = 20

    def binding_modifier(self, sim):
        return 1.0

    def catalysis_modifier(self, sim):
        return 1 / (1 + sim.inhibitor_count / self.Ki)
