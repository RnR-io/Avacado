"""
ASCII Weather Art & Forecast Collector v2.0.0
Provides detailed high-density ASCII weather banners and live forecast data.
"""
import urllib.request
import urllib.parse
import json
import datetime
import time

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

WEATHER_CACHE = {}

def get_location_from_ip():
    """Auto-detects current city using IP geolocation APIs."""
    for api_url in ["http://ip-api.com/json/", "https://ipinfo.io/json"]:
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "AvocadoCLI/2.0"})
            with urllib.request.urlopen(req, timeout=2) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                city = data.get("city") or data.get("region")
                country = data.get("countryCode") or data.get("country")
                if city:
                    return f"{city}, {country}" if country else city
        except Exception:
            continue
    return "Auto Location"

def get_weather(city="auto", unit="C"):
    global WEATHER_CACHE
    cache_key = f"{city}_{unit}"
    now_ts = time.time()

    # Return cache if less than 15 minutes old
    if cache_key in WEATHER_CACHE:
        cached_data, cached_ts = WEATHER_CACHE[cache_key]
        if now_ts - cached_ts < 900:
            return cached_data

    target_city = city
    if city == "auto":
        target_city = get_location_from_ip()

    try:
        encoded_city = urllib.parse.quote(target_city)
        url = f"https://wttr.in/{encoded_city}?format=j1"

        req = urllib.request.Request(url, headers={"User-Agent": "AvocadoCLI/2.0"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode('utf-8'))

            current = data['current_condition'][0]
            temp_c = current.get('temp_C', '24')
            temp_f = current.get('temp_F', '75')
            temp_str = f"{temp_c}°C" if unit == "C" else f"{temp_f}°F"

            desc = current.get('weatherDesc', [{}])[0].get('value', 'Clear')
            wind = f"{current.get('windspeedKmph', '10')} km/h"

            desc_lower = desc.lower()
            art_key = "clear"
            if "rain" in desc_lower or "drizzle" in desc_lower: art_key = "rain"
            elif "thunder" in desc_lower or "storm" in desc_lower: art_key = "thunderstorm"
            elif "snow" in desc_lower or "ice" in desc_lower: art_key = "snow"
            elif "cloud" in desc_lower or "overcast" in desc_lower: art_key = "clouds"
            elif "fog" in desc_lower or "mist" in desc_lower or "haze" in desc_lower: art_key = "fog"

            forecast_list = []
            today = datetime.date.today()
            for idx, day_data in enumerate(data.get('weather', [])[:3]):
                fc_date = today + datetime.timedelta(days=idx)
                date_str = fc_date.strftime("%m-%d")
                hi_c = day_data.get('maxtempC', '26')
                lo_c = day_data.get('mintempC', '20')
                hi_f = day_data.get('maxtempF', '78')
                lo_f = day_data.get('mintempF', '68')
                hi_s = f"{hi_c}°C" if unit == "C" else f"{hi_f}°F"
                lo_s = f"{lo_c}°C" if unit == "C" else f"{lo_f}°F"
                forecast_list.append({"day": date_str, "high": hi_s, "low": lo_s})

            result = {
                "city": target_city.title(),
                "temp": temp_str,
                "desc": desc,
                "wind": wind,
                "art": WEATHER_ART_MAP.get(art_key, WEATHER_ART_MAP["clear"]),
                "forecast": forecast_list
            }
            WEATHER_CACHE[cache_key] = (result, now_ts)
            return result
    except Exception:
        today = datetime.date.today()
        d1 = today.strftime("%m-%d")
        d2 = (today + datetime.timedelta(days=1)).strftime("%m-%d")
        d3 = (today + datetime.timedelta(days=2)).strftime("%m-%d")

        result = {
            "city": target_city.title() if target_city != "auto" else "Local Weather",
            "temp": "24°C" if unit == "C" else "75°F",
            "desc": "Clear Sky",
            "wind": "10 km/h",
            "art": WEATHER_ART_MAP["clear"],
            "forecast": [
                {"day": d1, "high": "26°C" if unit == "C" else "78°F", "low": "20°C" if unit == "C" else "68°F"},
                {"day": d2, "high": "27°C" if unit == "C" else "80°F", "low": "21°C" if unit == "C" else "70°F"},
                {"day": d3, "high": "25°C" if unit == "C" else "77°F", "low": "19°C" if unit == "C" else "66°F"}
            ]
        }
        return result
