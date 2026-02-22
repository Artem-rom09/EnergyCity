from config.city_config import CityConfig
from strategies.adp import ADPStrategy
from ml.predictor import predict

config = CityConfig(80000, 10000, 500)

result = predict(config)

print(result)