from http import HTTPStatus

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import View

from .ip_location import get_location_by_ip
from .weather_api import WeatherAPI

LAST_LOCATION_COOKIE = "last_location"


class IndexView(View):
    template_name = "weather/weather.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weather_api = WeatherAPI(
            api_key=settings.WEATHER_API_KEY, base_url=settings.WEATHER_API_BASE_URL
        )

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        location = request.COOKIES.get(LAST_LOCATION_COOKIE)
        if (location_param := request.GET.get("l")) is not None:
            location = location_param
        if location is None:
            location = get_location_by_ip(self._get_client_ip_from_request(request))
        return self._fetch_weather(request, location)

    @staticmethod
    def _get_client_ip_from_request(request: HttpRequest) -> str:
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.headers.get("X-Remote-Addr")

    def _fetch_weather(self, request: HttpRequest, location: str):
        location_weather_forecast = self.weather_api.get_forecast_by_location(location)
        if location_weather_forecast is None:
            return render(request, "404.html", status=HTTPStatus.NOT_FOUND)
        location, weather, forecast = location_weather_forecast
        context = {
            "location": location,
            "weather": weather,
            "forecast": forecast,
            "title": location.name.title(),
        }
        response = render(request, self.template_name, context)
        response.set_cookie(
            LAST_LOCATION_COOKIE, location.url if location.url else location.name
        )
        return response


class SearchView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weather_api = WeatherAPI(
            api_key=settings.WEATHER_API_KEY, base_url=settings.WEATHER_API_BASE_URL
        )

    def get(self, request: HttpRequest, **kwargs):
        if (query := request.GET.get("q")) is not None:
            data = self.weather_api.get_locations(query)
            return JsonResponse(data)
        return JsonResponse([])
