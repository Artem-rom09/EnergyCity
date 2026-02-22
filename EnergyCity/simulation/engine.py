from core.city import City
from core.measures import default_measures
from core.price_model import MultiPriceModel

BASE_BUDGET = 100
YEARS = 10


def run_single_simulation(strategy, config, training=False):

    city = City(config.energy.copy(), 100)
    measures = default_measures()
    price_model = MultiPriceModel(
        volatility_scale=config.volatility
    )
    for _ in range(YEARS):

        prices = price_model.next_price()
        energy_before = city.energy.copy()

        if training:
            strategy.train_step(city, measures, prices)
        else:
            action = strategy.choose_action(city, measures, prices)
            if action:
                b, m = action
                city.apply_measure(m, b)

        savings = 0
        for b in city.energy:
            diff = energy_before[b] - city.energy[b]
            savings += diff * prices[b]

        city.budget = BASE_BUDGET + city.budget + savings

    return city.total_energy(), city.budget