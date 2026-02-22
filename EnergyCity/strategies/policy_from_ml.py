import joblib
import numpy as np

class MLPolicyStrategy:

    def __init__(self):
        self.model = joblib.load("model_policy.pkl")

    def choose_measures(self, city, measures, prices):

        X = np.array([[
            city.energy["apartments"],
            city.energy["houses"],
            city.energy["public"]
        ]])

        building_type = self.model.predict(X)[0]

        # застосувати найкращий захід для цього типу