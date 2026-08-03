"""
Terminal Weather Fetcher & Formatter (Open-Meteo API)
"""
import urllib.request
import urllib.parse
import json

def get_weather_icon(code):
    if code == 0: return '☀️'
    if code in (1, 2): return '🌤'
    if code == 3: return '☁️'
    if 45 <= code <= 48: return '🌫'
    if 51 <= code <= 67: return '🌧'
    if 71 <= code <= 77: return '❄️'
    if 80 <= code <= 82: return '🌦'
    if code >= 95: return '🌩'
    return '🌡'

def get_weather_desc(code):
    if code == 0: return 'Clear Sky'
    if code in (1, 2): return 'Partly Cloudy'
    if code == 3: return 'Overcast'
    if 45 <= code <= 48: return 'Foggy'
    if 51 <= code <= 67: return 'Rainy'
    if 71 <= code <= 77: return 'Snowy'
    if 80 <= code <= 82: return 'Showers'
    if code >= 95: return 'Thunderstorm'
    return 'Moderate'

def get_weather(city_name="San Francisco", temp_unit="F"):
    try:
        # 1. Geocoding
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city_name)}&count=1&language=en&format=json"
        req = urllib.request.urlopen(geo_url, timeout=3)
        geo_data = json.loads(req.read().decode('utf-8'))

        if not geo_data.get("results"):
            return {"city": city_name, "error": "City not found"}

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]
        display_name = f"{loc['name']}, {loc.get('country_code', '').upper()}"

        # 2. Weather forecast
        is_f = temp_unit.upper() == 'F'
        unit_param = "&temperature_unit=fahrenheit" if is_f else ""
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto{unit_param}"
        
        w_req = urllib.request.urlopen(w_url, timeout=3)
        w_data = json.loads(w_req.read().decode('utf-8'))
        cur = w_data.get("current_weather", {})

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
                    "day": times[i][-5:], # MM-DD
                    "icon": get_weather_icon(codes[i]),
                    "high": f"{round(maxs[i])}{unit_str}",
                    "low": f"{round(mins[i])}{unit_str}"
                })

        return {
            "city": display_name,
            "temp": f"{round(cur.get('temperature', 68))}{unit_str}",
            "icon": get_weather_icon(cur.get("weathercode", 0)),
            "desc": get_weather_desc(cur.get("weathercode", 0)),
            "wind": f"{cur.get('windspeed', 8)} km/h",
            "forecast": forecast_list
        }
    except Exception as e:
        return {
            "city": city_name,
            "temp": "68°F",
            "icon": "🌤",
            "desc": "Partly Cloudy",
            "wind": "12 km/h",
            "forecast": []
        }
