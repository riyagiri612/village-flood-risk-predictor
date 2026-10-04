import requests
import math

API_KEY = "9c70d14b3f4bab4f066c75fbafb973be"

STATE_INFO = {
    "Uttar Pradesh": {"city": "Gorakhpur", "lat": 26.7606, "lon": 83.3732},
    "Bihar": {"city": "Patna", "lat": 25.5941, "lon": 85.1376},
    "Assam": {"city": "Guwahati", "lat": 26.1445, "lon": 91.7362},
    "West Bengal": {"city": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    "Kerala": {"city": "Alappuzha", "lat": 9.4981, "lon": 76.3388},
    "Odisha": {"city": "Bhubaneswar", "lat": 20.2961, "lon": 85.8245},
    "Maharashtra": {"city": "Kolhapur", "lat": 16.7050, "lon": 74.2433},
    "Gujarat": {"city": "Surat", "lat": 21.1702, "lon": 72.8311},
    "Rajasthan": {"city": "Kota", "lat": 25.2138, "lon": 75.8648},
    "Madhya Pradesh": {"city": "Hoshangabad", "lat": 22.7500, "lon": 77.7167},
    "Tamil Nadu": {"city": "Thanjavur", "lat": 10.7870, "lon": 79.1378},
    "Karnataka": {"city": "Kalaburagi", "lat": 17.3297, "lon": 76.8343},
    "Andhra Pradesh": {"city": "Vijayawada", "lat": 16.5062, "lon": 80.6480},
    "Punjab": {"city": "Patiala", "lat": 30.3398, "lon": 76.3869},
    "Himachal Pradesh": {"city": "Mandi", "lat": 31.7084, "lon": 76.9319},
    "Jharkhand": {"city": "Dumka", "lat": 24.2676, "lon": 87.2497},
    "Chhattisgarh": {"city": "Bilaspur", "lat": 22.0797, "lon": 82.1409},
    "Uttarakhand": {"city": "Haridwar", "lat": 29.9457, "lon": 78.1642},
    "Telangana": {"city": "Warangal", "lat": 17.9689, "lon": 79.5941},
    "Tripura": {"city": "Agartala", "lat": 23.8315, "lon": 91.2868},
    "Haryana": {"city": "Karnal", "lat": 29.6857, "lon": 76.9905},
    "Goa": {"city": "Panaji", "lat": 15.4909, "lon": 73.8278},
    "Jammu and Kashmir": {"city": "Srinagar", "lat": 34.0837, "lon": 74.7973},
    "Manipur": {"city": "Imphal", "lat": 24.8170, "lon": 93.9368},
    "Meghalaya": {"city": "Shillong", "lat": 25.5788, "lon": 91.8933},
    "Mizoram": {"city": "Aizawl", "lat": 23.7271, "lon": 92.7176},
    "Nagaland": {"city": "Kohima", "lat": 25.6751, "lon": 94.1086},
    "Sikkim": {"city": "Gangtok", "lat": 27.3389, "lon": 88.6065},
    "Arunachal Pradesh": {"city": "Itanagar", "lat": 27.0844, "lon": 93.6053},
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def find_nearest_state(user_lat, user_lon):
    closest_state = None
    closest_distance = float('inf')
    for state, info in STATE_INFO.items():
        dist = haversine_distance(user_lat, user_lon, info["lat"], info["lon"])
        if dist < closest_distance:
            closest_distance = dist
            closest_state = state
    return closest_state

_coord_cache = {}


def get_village_coordinates(village, state):
    """Finds lat/lon for a village using OpenWeather's geocoding. Returns None if not found."""
    key = (village, state)
    if key in _coord_cache:
        return _coord_cache[key]
    result = None
    name = village.replace(" Rural", "")
    try:
        response = requests.get(
            "https://api.openweathermap.org/geo/1.0/direct",
            params={"q": f"{name},IN", "limit": 5, "appid": API_KEY},
            timeout=5,
        )
        for place in response.json():
            if place.get("state", "").lower() == state.lower():
                result = (place["lat"], place["lon"])
                break
    except Exception:
        pass
    _coord_cache[key] = result
    return result


def get_live_weather(state, village=None):
    info = STATE_INFO.get(state)
    if not info:
        return None

    coords = get_village_coordinates(village, state) if village else None
    if coords:
        params = {"lat": coords[0], "lon": coords[1], "appid": API_KEY, "units": "metric"}
        label = village
    else:
        params = {"q": f"{info['city']},IN", "appid": API_KEY, "units": "metric"}
        label = info["city"]

    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params, timeout=5)
        data = response.json()
        if response.status_code != 200:
            return None
        return {
            "city": label, "approximate": not coords, "temp": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["description"].title(),
            "rain_last_hour": data.get("rain", {}).get("1h", 0)
        }
    except Exception:
        return None