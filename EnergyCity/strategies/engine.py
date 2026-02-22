# simulation/engine.py

from core.city import City
from core.measures import default_measures
from core.price_model import StochasticPriceModel


class SimulationEngine:

    def __init__(self, strategy, years=10):
        self.strategy = strategy
        self.years = years
        self.measures = default_measures()

    def run(self, initial_energy=154.8, initial_budget=100):

        city = City(initial_energy, initial_budget)
        price_model = StochasticPriceModel()

        history = []

        for year in range(self.years):

            price = price_model.next_price()
            energy_before = city.energy

            self.strategy.choose_measures(city, self.measures, price)

            energy_after = city.energy

            savings = (energy_before - energy_after) * price

            city.add_savings(savings)
            city.add_base_budget()

            history.append({
                "year": year + 1,
                "energy": city.energy,
                "budget": city.budget,
                "price": price
            })

        return history