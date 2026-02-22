import random


class AdaptiveStrategy:

    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def choose_action(self, city, measures, prices):

        possible_actions = []

        for b in city.energy:
            for m in measures:

                current = city.adoption[b].get(m.name, 0)

                if current >= m.max_adoption:
                    continue

                if city.budget < m.cost:
                    continue

                effective_effect = m.effect * (1 - current)

                delta_energy = city.energy[b] * effective_effect
                delta_money = delta_energy * prices[b]

                roi = delta_money / m.cost

                possible_actions.append((roi, b, m))

        if not possible_actions:
            return None

        if random.random() < self.epsilon:
            _, b, m = random.choice(possible_actions)
            return (b, m)

        # Сортуємо тільки по ROI
        possible_actions.sort(key=lambda x: x[0], reverse=True)

        _, b, m = possible_actions[0]

        return (b, m)