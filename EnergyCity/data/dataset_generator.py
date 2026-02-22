import pandas as pd
import random
from config.city_config import CityConfig
from strategies.adaptive import AdaptiveStrategy
from simulation.engine import run_single_simulation

def generate_dataset(samples=10000):

    rows = []

    for _ in range(samples):

        config = CityConfig(
            apartments=random.randint(20000, 150000),
            houses=random.randint(2000, 30000),
            public=random.randint(100, 2000)
        )

        strategy = AdaptiveStrategy()

        final_energy, final_budget = run_single_simulation(
            strategy,
            config
        )

        rows.append({
            "apartments": config.energy["apartments"],
            "houses": config.energy["houses"],
            "public": config.energy["public"],
            "final_energy": final_energy,
            "final_budget": final_budget
        })

    df = pd.DataFrame(rows)
    df.to_csv("city_dataset.csv", index=False)