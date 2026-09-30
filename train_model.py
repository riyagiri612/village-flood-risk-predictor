import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv("village_data.csv")

X = df[["rainfall_mm", "river_level_m", "elevation_m"]]
y = df["flooded_before"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

with open("flood_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as flood_model.pkl")