# strategies/adp.py

import numpy as np
import random


class ADPStrategy:

    def __init__(self, alpha=0.00005, gamma=0.95, epsilon=0.1):
        """
        alpha   – learning rate
        gamma   – discount factor
        epsilon – exploration probability
        """
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        # 3 енергії + бюджет
        self.weights = np.zeros(4)

    # ---------- STATE FEATURES ----------
    def features(self, city):
        return np.array([
            city.energy["apartments"] / 100000,
            city.energy["houses"] / 20000,
            city.energy["public"] / 5000,
            city.budget / 1000
        ])

    # ---------- VALUE FUNCTION ----------
    def value(self, city):
        return np.dot(self.weights, self.features(city))

    # ---------- ACTION SELECTION ----------
    def choose_action(self, city, measures, prices):

        possible_actions = []

        for b in city.energy:
            for m in measures:

                current = city.adoption[b].get(m.name, 0)

                if current >= m.max_adoption:
                    continue

                if city.budget < m.cost:
                    continue

                possible_actions.append((b, m))

        if not possible_actions:
            return None

        # 🔥 Exploration
        if random.random() < self.epsilon:
            return random.choice(possible_actions)

        # 🔥 Greedy selection via value approximation
        best_score = -1e9
        best_choice = None

        for (b, m) in possible_actions:

            current = city.adoption[b].get(m.name, 0)
            effective_effect = m.effect * (1 - current)

            energy_before = city.energy[b]
            energy_after = energy_before * (1 - effective_effect)

            reward = (energy_before - energy_after) * prices[b]

            score = reward + self.gamma * self.value(city)

            if score > best_score:
                best_score = score
                best_choice = (b, m)

        return best_choice

    # ---------- TD TRAINING STEP ----------
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