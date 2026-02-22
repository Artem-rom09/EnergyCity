# train_adp.py

import numpy as np
import matplotlib.pyplot as plt

from strategies.adp import ADPStrategy
from simulation.engine import run_single_simulation
from config.city_config import CityConfig


def train(episodes=5000):

    strategy = ADPStrategy(alpha=0.00005, gamma=0.95, epsilon=0.2)

    rewards_history = []

    for ep in range(episodes):

        config = CityConfig(
            apartments=40000,
            houses=5000,
            public=300
        )

        energy, budget = run_single_simulation(strategy, config, training=True)

        # Використовуємо бюджет як проксі для policy value
        rewards_history.append(budget)

        if ep % 500 == 0:
            print(f"Episode {ep}")

    # ---------------------------
    # ЗГЛАДЖЕНА КРИВА НАВЧАННЯ
    # ---------------------------

    window = 200
    moving_avg = np.convolve(
        rewards_history,
        np.ones(window) / window,
        mode='valid'
    )

    # Можемо прибрати перші 200 для чистішої картинки
    moving_avg = moving_avg[200:]

    # Переведемо в мільйони для красивішої осі
    moving_avg = moving_avg / 1_000_000

    plt.figure(figsize=(8, 5))
    plt.plot(moving_avg)
    plt.title("Convergence of ADP Policy")
    plt.xlabel("Training Episode")
    plt.ylabel("Policy Value (millions)")
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("adp_training_convergence.png")
    plt.show()

    # ---------------------------
    # ЗБЕРЕЖЕННЯ ВАГ
    # ---------------------------

    np.save("adp_weights.npy", strategy.weights)

    print("Training complete.")


if __name__ == "__main__":
    train()