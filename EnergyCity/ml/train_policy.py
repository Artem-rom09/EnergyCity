from sklearn.ensemble import RandomForestClassifier

# X = стан міста
# y = тип будівлі з найкращим ROI

model_policy = RandomForestClassifier(n_estimators=200)
model_policy.fit(X, y)