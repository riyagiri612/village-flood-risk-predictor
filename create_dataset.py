import pandas as pd
import random

random.seed(42)

states_villages = {
    "Uttar Pradesh": ["Rampur", "Sitapur", "Ganeshpur", "Devgarh", "Kishanpur"],
    "Bihar": ["Lalganj", "Bhavpur", "Nandgaon", "Shivpur", "Rajnagar"],
    "Assam": ["Chandpur", "Harigaon", "Madhopur", "Ramnagar", "Ashokpur"],
    "West Bengal": ["Bardhaman", "Nadiapur", "Suri", "Bolpur", "Katwa"],
    "Kerala": ["Alappuzha Rural", "Kuttanad", "Chengannur", "Pathanamthitta Rural", "Cherthala"],
    "Odisha": ["Bhadrak Rural", "Puri Rural", "Kendrapara", "Jagatsinghpur Rural", "Baleswar Rural"],
}

data = {"village": [], "state": [], "rainfall_mm": [], "river_level_m": [], "elevation_m": [], "flooded_before": []}

for state, villages in states_villages.items():
    for v in villages:
        rainfall = random.randint(30, 350)
        river_level = round(random.uniform(2.0, 10.5), 1)
        elevation = random.randint(20, 200)
        # Simple rule to make the mock data realistic: high rainfall + high river + low elevation = more likely flooded
        flood_score = (rainfall / 350) + (river_level / 10.5) + (1 - elevation / 200)
        flooded = 1 if flood_score > 1.6 else 0

        data["village"].append(v)
        data["state"].append(state)
        data["rainfall_mm"].append(rainfall)
        data["river_level_m"].append(river_level)
        data["elevation_m"].append(elevation)
        data["flooded_before"].append(flooded)

df = pd.DataFrame(data)
df.to_csv("village_data.csv", index=False)
print(f"Dataset created with {len(df)} villages across {len(states_villages)} states!")
print(df.head(10))