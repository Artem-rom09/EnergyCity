class CityConfig:

    def __init__(
        self,
        apartments=40000,
        houses=5000,
        public=300,
        volatility=1.0
    ):

        self.apartments = apartments
        self.houses = houses
        self.public = public

        self.volatility = volatility

        # Базове споживання (місячне)
        base = {
            "apartments": 250,
            "houses": 400,
            "public": 3000
        }

        counts = {
            "apartments": apartments,
            "houses": houses,
            "public": public
        }

        # 🔥 ОЦЕ КЛЮЧОВЕ
        self.energy = {
            k: base[k] * counts[k]
            for k in base
        }

        self.initial_budget = 100