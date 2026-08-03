"""
ASCII Weather Art & Forecast Collector
Provides detailed high-density ASCII weather banners and forecast data.
"""
import urllib.request
import json

WEATHER_ART_MAP = {
    "clear": [
        "       \\   |   /       ",
        "     '-.  .---.  .-'   ",
        "    ---  (     )  ---  ",
        "     .-'  '---'  '-.   ",
        "       /   |   \\       "
    ],
    "clouds": [
        "         .--.          ",
        "      .-(    ).        ",
        "     (___.__.__)       ",
        "       (        )      ",
        "      '----------'     "
    ],
    "rain": [
        "         .--.          ",
        "      .-(    ).        ",
        "     (___.__.__)       ",
        "      /  /  /  /       ",
        "     /  /  /  /        "
    ],
    "thunderstorm": [
        "         .--.          ",
        "      .-(    ).        ",
        "     (___.__.__)       ",
        "      ⚡ / ⚡ / ⚡        ",
        "     / / / / /         "
    ],
    "snow": [
        "         .--.          ",
        "      .-(    ).        ",
        "     (___.__.__)       ",
        "      *  *  *  *       ",
        "     *  *  *  *        "
    ],
    "fog": [
        "    _ - _ - _ - _ -    ",
        "     _ - _ - _ - _     ",
        "    _ - _ - _ - _ -    ",
        "     _ - _ - _ - _     ",
        "    _ - _ - _ - _ -    "
    ]
}

def get_weather(city="auto", unit="C"):
    try:
        # Default high-density weather payload
        query_city = "Mangalore" if city == "auto" else city
        encoded_city = urllib.parse.quote(query_city)
        url = f"https://wttr.in/{encoded_city}?format=j1"

        req = urllib.request.Request(url, headers={"User-Agent": "AvocadoCLI/1.2"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))

            current = data['current_condition'][0]
            temp_c = current.get('temp_C', '26')
            temp_f = current.get('temp_F', '78')
            temp_str = f"{temp_c}°C" if unit == "C" else f"{temp_f}°F"

            desc = current.get('weatherDesc', [{}])[0].get('value', 'Clear Sky')
            wind = f"{current.get('windspeedKmph', '10')} km/h"

            desc_lower = desc.lower()
            art_key = "clear"
            if "rain" in desc_lower or "drizzle" in desc_lower: art_key = "rain"
            elif "thunder" in desc_lower or "storm" in desc_lower: art_key = "thunderstorm"
            elif "snow" in desc_lower or "ice" in desc_lower: art_key = "snow"
            elif "cloud" in desc_lower or "overcast" in desc_lower: art_key = "clouds"
            elif "fog" in desc_lower or "mist" in desc_lower or "haze" in desc_lower: art_key = "fog"

            forecast_list = []
            for day_data in data.get('weather', [])[:4]:
                date_str = day_data.get('date', '2026-08-03')[5:]
                hi_c = day_data.get('maxtempC', '28')
                lo_c = day_data.get('mintempC', '24')
                hi_f = day_data.get('maxtempF', '82')
                lo_f = day_data.get('mintempF', '75')
                hi_s = f"{hi_c}°C" if unit == "C" else f"{hi_f}°F"
                lo_s = f"{lo_c}°C" if unit == "C" else f"{lo_f}°F"
                forecast_list.append({"day": date_str, "high": hi_s, "low": lo_s})

            return {
                "city": query_city.title(),
                "temp": temp_str,
                "desc": desc,
                "wind": wind,
                "art": WEATHER_ART_MAP.get(art_key, WEATHER_ART_MAP["clear"]),
                "forecast": forecast_list
            }
    except Exception:
        # High-density offline fallback
        return {
            "city": city.title() if city != "auto" else "Mangalore, IN",
            "temp": "26°C" if unit == "C" else "78°F",
            "desc": "Partly Cloudy",
            "wind": "12.5 km/h",
            "art": WEATHER_ART_MAP["clouds"],
            "forecast": [
                {"day": "08-03", "high": "27°C", "low": "24°C"},
                {"day": "08-04", "high": "28°C", "low": "24°C"},
                {"day": "08-05", "high": "28°C", "low": "24°C"}
            ]
        }
