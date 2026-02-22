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

        # Додаємо параметр волатильності
        self.volatility = volatility

        # Базове споживання (місячне)
        self.base_consumption = {
            "apartments": 250,
            "houses": 400,
            "public": 3000
        }

        # Кількість будівель
        self.counts = {
            "apartments": apartments,
            "houses": houses,
            "public": public
        }

        # Початковий бюджет
        self.initial_budget = 100