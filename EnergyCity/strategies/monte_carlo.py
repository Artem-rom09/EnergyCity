# simulation/monte_carlo.py

import numpy as np


def run_monte_carlo(engine, simulations=1000):

    final_energies = []
    final_budgets = []

    for _ in range(simulations):
        history = engine.run()
        final_energies.append(history[-1]["energy"])
        final_budgets.append(history[-1]["budget"])

    return np.array(final_energies), np.array(final_budgets)