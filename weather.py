import requests

API_KEY = "9c70d14b3f4bab4f066c75fbafb973be"

# Since exact village coordinates aren't publicly available, we use the
# nearest major city per state as a real-world weather reference point.
CITY_FOR_STATE = {
    "Uttar Pradesh": "Gorakhpur",
    "Bihar": "Patna",
    "Assam": "Guwahati",
    "West Bengal": "Kolkata",
    "Kerala": "Alappuzha",
    "Odisha": "Bhubaneswar",
}

def get_live_weather(state):
    city = CITY_FOR_STATE.get(state)
    if not city:
        return None

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return None

        return {
            "city": city,
            "temp": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].title(),
            "rain_last_hour": data.get("rain", {}).get("1h", 0)
        }
    except Exception:
        return None