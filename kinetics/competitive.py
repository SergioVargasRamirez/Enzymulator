class CompetitiveModel:
    Ki = 20

    def binding_modifier(self, sim):
        return 1 / (1 + sim.inhibitor_count / self.Ki)

    def catalysis_modifier(self, sim):
        return 1.0
