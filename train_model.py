import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load the dataset you created earlier
df = pd.read_csv("village_data.csv")

# X = the inputs the model learns from, y = what it's trying to predict
X = df[["rainfall_mm", "river_level_m", "elevation_m"]]
y = df["flooded_before"]

# Split data: 70% to train the model, 30% to test how good it is
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Check how accurate it is on data it hasn't seen
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the trained model to a file so app.py can use it later
with open("flood_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as flood_model.pkl")