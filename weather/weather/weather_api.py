from typing import Optional
from urllib.parse import urljoin

import requests

from .models import Location, Weather, Forecast

FORECAST_WEATHER_PATH = "forecast.json"

SEARCH_PATH = "search.json"


class WeatherAPI:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_forecast_by_location(
        self, location_name: str
    ) -> Optional[tuple[Location, Weather, Forecast]]:
        url = urljoin(self.base_url, FORECAST_WEATHER_PATH)
        req = requests.get(
            url,
            params={
                "key": self.api_key,
                "q": location_name,
                "days": 2,
                "aqi": "no",
                "alerts": "no",
            },
        )
        data = req.json()
        weather_data = data.get("current")
        location_data = data.get("location")
        forecast_data = data.get("forecast")
        if weather_data is None or location_data is None:
            return None
        condition_data = weather_data.get("condition")
        if (
            condition_data is not None
            and (icon_url := condition_data.get("icon")) is not None
        ):
            weather_data["condition"]["icon"] = "https:" + icon_url
        return (
            Location.from_dict(location_data),
            Weather.from_dict(weather_data),
            Forecast.from_dict(forecast_data),
        )

    def get_locations(self, symbols) -> dict[str, list[Location]]:
        if len(symbols) < 3:
            return {"locations": []}
        url = urljoin(self.base_url, SEARCH_PATH)
        req = requests.get(url, params={"key": self.api_key, "q": symbols})
        data = req.json()
        return {
            "locations": [
                Location.from_dict(location_data).to_dict()
                for location_data in data
                if location_data
            ]
        }
