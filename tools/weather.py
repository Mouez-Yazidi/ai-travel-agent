"""
OpenWeather API tool for fetching current weather by city.
"""
from datetime import datetime

import requests
from langchain_core.tools import tool

from config import OPENWEATHER_API_KEY


@tool
def get_weather(city: str) -> str:
    """Fetch the current weather for a city."""
    if not OPENWEATHER_API_KEY:
        return (
            "Weather unavailable: API key not set "
            "(OPEN_WEATHER_API_KEY or OPENWEATHER_API_KEY in .env)."
        )
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    )
    r = requests.get(url)
    data = r.json()
    if r.status_code != 200 or data.get("cod") != 200:
        return "Weather information not available for this city."

    city_name = data["name"]
    country = data["sys"]["country"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    clouds = data["clouds"]["all"]
    visibility = data["visibility"] / 1000  # km
    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    return f"""
Weather in {city_name}, {country}

Temperature: {temp}°C (feels like {feels_like}°C)
Condition: {description}
Cloud Coverage: {clouds}%

Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
Visibility: {visibility} km
Pressure: {pressure} hPa

Sunrise: {sunrise}
Sunset: {sunset}
"""
