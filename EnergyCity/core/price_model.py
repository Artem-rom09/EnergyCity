import numpy as np


class MultiPriceModel:

    def __init__(self, volatility_scale=1.0):

        self.prices = {
            "apartments": 1.0,
            "houses": 1.0,
            "public": 1.0
        }

        self.growth = {
            "apartments": 0.04,
            "houses": 0.05,
            "public": 0.06
        }

        self.vol = {
            "apartments": 0.02 * volatility_scale,
            "houses": 0.03 * volatility_scale,
            "public": 0.04 * volatility_scale
        }

    def next_price(self):

        common_shock = np.random.normal()

        for k in self.prices:

            local_shock = np.random.normal()

            self.prices[k] *= np.exp(
                self.growth[k] +
                0.7 * self.vol[k] * common_shock +
                0.3 * self.vol[k] * local_shock
            )

        return self.prices.copy()