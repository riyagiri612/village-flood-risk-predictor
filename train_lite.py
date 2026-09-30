import pandas as pd
import numpy as np
import json

df = pd.read_csv("village_data.csv")

X = df[["rainfall_mm", "river_level_m", "elevation_m"]].values.astype(float)
y = df["flooded_before"].values.astype(float)

# Scale the inputs so training is stable
mean = X.mean(axis=0)
std = X.std(axis=0)
Xs = (X - mean) / std

# Split: 70% train, 30% test
rng = np.random.default_rng(42)
idx = rng.permutation(len(Xs))
split = int(0.7 * len(Xs))
train_idx, test_idx = idx[:split], idx[split:]

# Logistic regression using gradient descent
w = np.zeros(3)
b = 0.0
lr = 0.1

for _ in range(5000):
    z = Xs[train_idx] @ w + b
    p = 1 / (1 + np.exp(-z))
    error = p - y[train_idx]
    w -= lr * (Xs[train_idx].T @ error) / len(train_idx)
    b -= lr * error.mean()

# Check accuracy on data the model has not seen
z_test = Xs[test_idx] @ w + b
p_test = 1 / (1 + np.exp(-z_test))
predictions = (p_test >= 0.5).astype(float)
accuracy = (predictions == y[test_idx]).mean()
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Save the learned numbers to a file
with open("model_weights.json", "w") as f:
    json.dump({"weights": w.tolist(), "bias": float(b),
               "mean": mean.tolist(), "std": std.tolist()}, f)

print("Model saved as model_weights.json")