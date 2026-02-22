class City:

    def __init__(self, energy_dict, budget):
        self.energy = energy_dict.copy()
        self.budget = budget
        self.adoption = {b: {} for b in self.energy}

    def apply_measure(self, measure, building_type):

        current = self.adoption[building_type].get(measure.name, 0)

        if current >= measure.max_adoption:
            return False

        effective_effect = measure.effect * (1 - current)

        self.energy[building_type] *= (1 - effective_effect)
        self.budget -= measure.cost

        self.adoption[building_type][measure.name] = min(
            measure.max_adoption,
            current + 0.1
        )

        return True

    def total_energy(self):
        return sum(self.energy.values())