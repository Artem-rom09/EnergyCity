import joblib
import numpy as np

model_energy = joblib.load("model_energy.pkl")
model_budget = joblib.load("model_budget.pkl")

def predict(city_config):

    X = np.array([[
        city_config.energy["apartments"],
        city_config.energy["houses"],
        city_config.energy["public"]
    ]])

    return {
        "predicted_energy": model_energy.predict(X)[0],
        "predicted_budget": model_budget.predict(X)[0]
    }