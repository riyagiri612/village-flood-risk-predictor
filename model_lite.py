import json
import math

with open("model_weights.json") as f:
    W = json.load(f)

class LiteModel:
    def predict_proba(self, rows):
        results = []
        for row in rows:
            z = W["bias"]
            for i, value in enumerate(row):
                z += W["weights"][i] * ((value - W["mean"][i]) / W["std"][i])
            p = 1 / (1 + math.exp(-z))
            results.append([1 - p, p])
        return results

model = LiteModel()