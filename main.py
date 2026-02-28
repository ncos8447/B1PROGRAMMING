
import json
from datetime import datetime

eu_capitals = [
    {"city": "Vienna", "country": "Austria", "lat": 48.2082, "lon": 16.3738},
    {"city": "Brussels", "country": "Belgium", "lat": 50.8503, "lon": 4.3517},
    {"city": "Sofia", "country": "Bulgaria", "lat": 42.6977, "lon": 23.3219},
    {"city": "Zagreb", "country": "Croatia", "lat": 45.8150, "lon": 15.9819},
    {"city": "Nicosia", "country": "Cyprus", "lat": 35.1856, "lon": 33.3823},
    {"city": "Prague", "country": "Czechia", "lat": 50.0755, "lon": 14.4378},
    {"city": "Copenhagen", "country": "Denmark", "lat": 55.6761, "lon": 12.5683},
    {"city": "Tallinn", "country": "Estonia", "lat": 59.4370, "lon": 24.7536},
    {"city": "Helsinki", "country": "Finland", "lat": 60.1695, "lon": 24.9354},
    {"city": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"city": "Berlin", "country": "Germany", "lat": 52.5200, "lon": 13.4050},
    {"city": "Athens", "country": "Greece", "lat": 37.9838, "lon": 23.7275},
    {"city": "Budapest", "country": "Hungary", "lat": 47.4979, "lon": 19.0402},
    {"city": "Dublin", "country": "Ireland", "lat": 53.3498, "lon": -6.2603},
    {"city": "Rome", "country": "Italy", "lat": 41.9028, "lon": 12.4964},
    {"city": "Riga", "country": "Latvia", "lat": 56.9496, "lon": 24.1052},
    {"city": "Vilnius", "country": "Lithuania", "lat": 54.6872, "lon": 25.2797},
    {"city": "Luxembourg", "country": "Luxembourg", "lat": 49.6116, "lon": 6.1319},
    {"city": "Valletta", "country": "Malta", "lat": 35.8989, "lon": 14.5146},
    {"city": "Amsterdam", "country": "Netherlands", "lat": 52.3676, "lon": 4.9041},
    {"city": "Warsaw", "country": "Poland", "lat": 52.2297, "lon": 21.0122},
    {"city": "Lisbon", "country": "Portugal", "lat": 38.7223, "lon": -9.1393},
    {"city": "Bucharest", "country": "Romania", "lat": 44.4268, "lon": 26.1025},
    {"city": "Bratislava", "country": "Slovakia", "lat": 48.1486, "lon": 17.1077},
    {"city": "Ljubljana", "country": "Slovenia", "lat": 46.0569, "lon": 14.5058},
    {"city": "Madrid", "country": "Spain", "lat": 40.4168, "lon": -3.7038},
    {"city": "Stockholm", "country": "Sweden", "lat": 59.3293, "lon": 18.0686}
]

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle (light)",
    53: "Drizzle (moderate)",
    55: "Drizzle (dense)",
    56: "Freezing Drizzle (light)",
    57: "Freezing Drizzle (dense)",
    61: "Rain (slight)",
    63: "Rain (moderate)",
    65: "Rain (heavy)",
    66: "Freezing Rain (light)",
    67: "Freezing Rain (heavy)",
    71: "Snow fall (slight)",
    73: "Snow fall (moderate)",
    75: "Snow fall (heavy)",
    77: "Snow grains",
    80: "Rain showers (slight)",
    81: "Rain showers (moderate)",
    82: "Rain showers (violent)",
    85: "Snow showers (slight)",
    86: "Snow showers (heavy)",
    95: "Thunderstorm",
    96: "Thunderstorm (slight hail)",
    97: "Thunderstorm (heavy hail)"
}

def fetch_weather(lat, lon):
    today = datetime.now().strftime("%Y-%m-%d")

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "temperature_2m,precipitation_probability,weather code",
        "start_date": today,
        "end_date": today,
        "timezone": "auto"
    }

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"API error: {e}")
        return None


def main():
    all_weather = {}

    for capital in eu_capitals:
        city = capital["city"]
        country = capital["country"]

        print(f"Fetching weather for {city}...")

        data = fetch_weather(capital["lat"], capital["lon"])
        if not data:
            continue

        try:
            current = data["current_weather"]

            city_data = {
                "country": country,
                "coordinates": {
                    "latitude": capital["lat"],
                    "longitude": capital["lon"]
                },
                "current_weather": {
                    "temperature": current["temperature"],
                    "wind speed": current["wind speed"],
                    "weather code": current["weather code"],
                    "condition": weather_codes.get(current["weather code"], "Unknown"),
                    "time": current["time"]
                },
                "hourly_forecast": []
            }

            hourly = data["hourly"]
            for i in range(len(hourly["time"])):
                city_data["hourly_forecast"].append({
                    "time": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "precipitation_probability": hourly["precipitation_probability"][i],
                    "weather code": hourly["weather code"][i]
                })

            all_weather[city] = city_data

        except KeyError as e:
            print(f"Missing data for {city}: {e}")

    with open("eu_weather_data.json", "w", encoding="utf-8") as f:
        json.dump(all_weather, f, indent=2, ensure_ascii=False)

    print("Finished. Data saved to eu_weather_data.json")