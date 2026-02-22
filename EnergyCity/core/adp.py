# strategies/adp.py

import numpy as np


class ADPStrategy:

    def __init__(self, alpha=0.0005, gamma=0.95):
        self.alpha = alpha
        self.gamma = gamma
        self.weights = np.zeros(4)

    def features(self, city):
        return np.array([
            city.energy["apartments"],
            city.energy["houses"],
            city.energy["public"],
            city.budget
        ])

    def value(self, city):
        return np.dot(self.weights, self.features(city))

    def choose_action(self, city, measures, prices):

        best_score = -1e9
        best_choice = None

        for b in city.energy:
            for m in measures:

                current = city.adoption[b].get(m.name, 0)

                if current >= m.max_adoption:
                    continue

                if city.budget < m.cost:
                    continue

                effective_effect = m.effect * (1 - current)

                energy_before = city.energy[b]
                energy_after = energy_before * (1 - effective_effect)

                reward = (energy_before - energy_after) * prices[b]

                score = reward + self.gamma * self.value(city)

                if score > best_score:
                    best_score = score
                    best_choice = (b, m)

        return best_choice

    def train_step(self, city, measures, prices):

        state_features = self.features(city)
        state_value = self.value(city)

        action = self.choose_action(city, measures, prices)

        if action is None:
            return

        b, m = action

        energy_before = city.energy[b]
        city.apply_measure(m, b)
        energy_after = city.energy[b]

        reward = (energy_before - energy_after) * prices[b]

        next_value = self.value(city)

        td_error = reward + self.gamma * next_value - state_value

        self.weights += self.alpha * td_error * state_features