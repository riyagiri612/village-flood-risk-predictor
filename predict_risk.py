import pickle

# Load the trained model you saved in Step 4
with open("flood_model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_risk(rainfall_mm, river_level_m, elevation_m):
    # Model expects the input in the same shape as training: a list of lists
    input_data = [[rainfall_mm, river_level_m, elevation_m]]

    # predict_proba gives probability of [no flood, flood] — we want the "flood" one
    flood_probability = model.predict_proba(input_data)[0][1]

    # Bucket the probability into risk levels
    if flood_probability < 0.33:
        risk = "Low"
    elif flood_probability < 0.66:
        risk = "Medium"
    else:
        risk = "High"

    return risk, round(flood_probability * 100, 1)

# --- test it here ---
if __name__ == "__main__":
    risk, confidence = predict_risk(rainfall_mm=250, river_level_m=9.0, elevation_m=40)
    print(f"Risk level: {risk} ({confidence}% flood probability)")