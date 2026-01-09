import httpx
import os

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

async def fetch_weather(city_name: str):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
