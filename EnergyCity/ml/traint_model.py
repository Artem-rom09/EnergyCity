import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib


def train():

    df = pd.read_csv("city_dataset.csv")

    X = df[[
        "apartments_energy",
        "houses_energy",
        "public_energy"
    ]]

    y_energy = df["final_energy"]
    y_budget = df["final_budget"]

    model_energy = RandomForestRegressor(n_estimators=100)
    model_budget = RandomForestRegressor(n_estimators=100)

    model_energy.fit(X, y_energy)
    model_budget.fit(X, y_budget)

    joblib.dump(model_energy, "model_energy.pkl")
    joblib.dump(model_budget, "model_budget.pkl")

    print("Models trained and saved.")