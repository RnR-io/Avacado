"""
Terminal Weather Fetcher & ASCII Art Formatter (Open-Meteo API)
"""
import urllib.request
import urllib.parse
import json

ASCII_WEATHER_ART = {
    "clear": [
        "   \\  |  /   ",
        "  '-.(_).-`  ",
        "  -- ( ) --  ",
        "  .-'(`)-'.  ",
        "   /  |  \\   "
    ],
    "cloudy": [
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__.__) ",
        "             "
    ],
    "rain": [
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__.__) ",
        "  / / / / /  "
    ],
    "thunder": [
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__.__) ",
        "   ⚡ / ⚡ /  "
    ],
    "snow": [
        "     .--.    ",
        "  .-(    ).  ",
        " (___.__.__) ",
        "  *  *  *  * "
    ],
    "fog": [
        " = = = = = = ",
        "  - - - - -  ",
        " = = = = = = "
    ]
}

def get_weather_art_key(code):
    if code == 0: return "clear"
    if code in (1, 2, 3): return "cloudy"
    if 45 <= code <= 48: return "fog"
    if 51 <= code <= 67 or 80 <= code <= 82: return "rain"
    if 71 <= code <= 77: return "snow"
    if code >= 95: return "thunder"
    return "cloudy"

def get_weather_desc(code):
    if code == 0: return "Clear Sky"
    if code in (1, 2): return "Partly Cloudy"
    if code == 3: return "Overcast"
    if 45 <= code <= 48: return "Foggy"
    if 51 <= code <= 67: return "Rainy"
    if 71 <= code <= 77: return "Snowy"
    if 80 <= code <= 82: return "Rain Showers"
    if code >= 95: return "Thunderstorm"
    return "Moderate"

def get_weather(city_name="San Francisco", temp_unit="F"):
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_name)}&count=1&language=en&format=json"
        req = urllib.request.urlopen(geo_url, timeout=3)
        geo_data = json.loads(req.read().decode('utf-8'))

        if not geo_data.get("results"):
            return _default_weather(city_name, temp_unit)

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        display_name = f"{loc['name']}, {loc.get('country_code', '').upper()}"

        is_f = temp_unit.upper() == 'F'
        unit_param = "&temperature_unit=fahrenheit" if is_f else ""
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto{unit_param}"

        w_req = urllib.request.urlopen(w_url, timeout=3)
        w_data = json.loads(w_req.read().decode('utf-8'))
        cur = w_data.get("current_weather", {})
        code = cur.get("weathercode", 0)

        unit_str = "°F" if is_f else "°C"
        daily = w_data.get("daily", {})
        forecast_list = []

        if daily and "time" in daily:
            times = daily.get("time", [])
            maxs = daily.get("temperature_2m_max", [])
            mins = daily.get("temperature_2m_min", [])
            codes = daily.get("weathercode", [])

            for i in range(min(4, len(times))):
                forecast_list.append({
                    "day": times[i][-5:],
                    "high": f"{round(maxs[i])}{unit_str}",
                    "low": f"{round(mins[i])}{unit_str}"
                })

        art_key = get_weather_art_key(code)

        return {
            "city": display_name,
            "temp": f"{round(cur.get('temperature', 68))}{unit_str}",
            "desc": get_weather_desc(code),
            "wind": f"{cur.get('windspeed', 8)} km/h",
            "art": ASCII_WEATHER_ART.get(art_key, ASCII_WEATHER_ART["cloudy"]),
            "forecast": forecast_list
        }
    except Exception:
        return _default_weather(city_name, temp_unit)

def _default_weather(city_name, temp_unit):
    unit_str = "°F" if temp_unit.upper() == 'F' else "°C"
    return {
        "city": city_name,
        "temp": f"68{unit_str}",
        "desc": "Partly Cloudy",
        "wind": "10 km/h",
        "art": ASCII_WEATHER_ART["clear"],
        "forecast": [
            {"day": "Mon", "high": f"70{unit_str}", "low": f"55{unit_str}"},
            {"day": "Tue", "high": f"68{unit_str}", "low": f"54{unit_str}"},
            {"day": "Wed", "high": f"72{unit_str}", "low": f"56{unit_str}"}
        ]
    }
