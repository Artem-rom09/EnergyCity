import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train():

    df = pd.read_csv("city_dataset.csv")

    X = df[["apartments", "houses", "public"]]
    y_energy = df["final_energy"]
    y_budget = df["final_budget"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_energy, test_size=0.2
    )

    model_energy = RandomForestRegressor(n_estimators=200)
    model_energy.fit(X_train, y_train)

    print("Energy R2:", model_energy.score(X_test, y_test))

    joblib.dump(model_energy, "model_energy.pkl")