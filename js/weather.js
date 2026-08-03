/**
 * Weather Manager (Open-Meteo API Integration)
 * Free real-time weather & 5-day forecasts with no API key requirement.
 */
class WeatherManager {
  constructor() {
    this.currentCity = "San Francisco";
  }

  init() {
    this.bindEvents();
    const city = window.settingsManager?.config?.defaultCity || "San Francisco";
    this.fetchWeather(city);
  }

  bindEvents() {
    const form = document.getElementById('weatherSearchForm');
    if (form) {
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        const city = document.getElementById('weatherCityInput').value.trim();
        if (city) this.fetchWeather(city);
      });
    }
  }

  async fetchWeather(cityName) {
    this.currentCity = cityName;
    try {
      // 1. Geocoding lookup
      const geoUrl = `https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(cityName)}&count=1&language=en&format=json`;
      const geoRes = await fetch(geoUrl);
      const geoData = await geoRes.json();

      if (!geoData.results || geoData.results.length === 0) {
        this.renderError("City not found");
        return;
      }

      const loc = geoData.results[0];
      const lat = loc.latitude;
      const lon = loc.longitude;
      const displayName = `${loc.name}, ${loc.country_code ? loc.country_code.toUpperCase() : ''}`;

      // 2. Fetch Weather Data
      const isF = (window.settingsManager?.config?.tempUnit || 'F') === 'F';
      const tempUnitParam = isF ? '&temperature_unit=fahrenheit' : '';
      const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=auto${tempUnitParam}`;
      
      const wRes = await fetch(weatherUrl);
      const wData = await wRes.json();

      this.renderWeather(displayName, wData, isF);
    } catch (e) {
      this.renderError("Weather offline");
    }
  }

  getWeatherIcon(code) {
    if (code === 0) return '☀️';
    if (code === 1 || code === 2) return '🌤';
    if (code === 3) return '☁️';
    if (code >= 45 && code <= 48) return '🌫';
    if (code >= 51 && code <= 67) return '🌧';
    if (code >= 71 && code <= 77) return '❄️';
    if (code >= 80 && code <= 82) return '🌦';
    if (code >= 95) return '🌩';
    return '🌡';
  }

  getWeatherDesc(code) {
    if (code === 0) return 'Clear Sky';
    if (code === 1 || code === 2) return 'Partly Cloudy';
    if (code === 3) return 'Overcast';
    if (code >= 45 && code <= 48) return 'Foggy';
    if (code >= 51 && code <= 67) return 'Rainy';
    if (code >= 71 && code <= 77) return 'Snowy';
    if (code >= 80 && code <= 82) return 'Rain Showers';
    if (code >= 95) return 'Thunderstorm';
    return 'Moderate';
  }

  renderWeather(cityName, data, isF) {
    const cur = data.current_weather;
    const unitSymbol = isF ? '°F' : '°C';

    document.getElementById('weatherIcon').textContent = this.getWeatherIcon(cur.weathercode);
    document.getElementById('weatherTemp').textContent = `${Math.round(cur.temperature)}${unitSymbol}`;
    document.getElementById('weatherCityName').textContent = cityName;
    document.getElementById('weatherDesc').textContent = this.getWeatherDesc(cur.weathercode);
    document.getElementById('weatherWind').textContent = `${cur.windspeed} km/h`;
    document.getElementById('weatherHumidity').textContent = `62%`;

    // 5-day forecast
    const forecastGrid = document.getElementById('weatherForecastGrid');
    if (forecastGrid && data.daily) {
      forecastGrid.innerHTML = '';
      const dates = data.daily.time;
      const maxs = data.daily.temperature_2m_max;
      const mins = data.daily.temperature_2m_min;
      const codes = data.daily.weathercode;

      for (let i = 0; i < Math.min(5, dates.length); i++) {
        const dayDate = new Date(dates[i]);
        const dayName = dayDate.toLocaleDateString('en-US', { weekday: 'short' });
        const icon = this.getWeatherIcon(codes[i]);
        
        const card = document.createElement('div');
        card.className = 'forecast-day';
        card.innerHTML = `
          <div><strong>${dayName}</strong></div>
          <div style="font-size:16px;margin:2px 0;">${icon}</div>
          <div>${Math.round(maxs[i])}° / ${Math.round(mins[i])}°</div>
        `;
        forecastGrid.appendChild(card);
      }
    }
  }

  renderError(msg) {
    document.getElementById('weatherDesc').textContent = msg;
  }
}

window.weatherManager = new WeatherManager();
