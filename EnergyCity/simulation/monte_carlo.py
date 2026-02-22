# simulation/monte_carlo.py

import numpy as np
from simulation.engine import run_single_simulation
from strategies.adaptive import AdaptiveStrategy
from strategies.adp import ADPStrategy


def run_monte_carlo(strategy, config, simulations=500):

    energies = []
    budgets = []

    for _ in range(simulations):

        # 🔥 Створюємо нову стратегію кожного разу
        if isinstance(strategy, AdaptiveStrategy):
            strat = AdaptiveStrategy()
        else:
            strat = ADPStrategy()
            strat.weights = strategy.weights.copy()

        e, b = run_single_simulation(strat, config, training=False)

        energies.append(e)
        budgets.append(b)

    return np.array(energies), np.array(budgets)