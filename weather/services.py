import os
from datetime import timedelta

import requests
from django.utils import timezone
from dotenv import load_dotenv

from weather.exceptions import WeatherServiceError
from weather.models import CityWeather, WeatherRequestsHistory
from weather.serializers import CityWeatherSerializer

load_dotenv()


class WeatherService:
    def __init__(self):
        self.weather_api_key = os.getenv("YANDEX_WEATHER_API_KEY")
        self.geocode_api_key = os.getenv("YANDEX_GEOCODE_API_KEY")
        self.serializer = CityWeatherSerializer

    def get_city_coordinates(self, city: str) -> dict:
        geocode_url = f"https://geocode-maps.yandex.ru/1.x?apikey={self.geocode_api_key}&geocode={city}&format=json"
        response = requests.get(geocode_url).json()

        try:
            pos = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        except IndexError:
            raise WeatherServiceError("Не удалось получить данные о погоде в городе")

        longitude, latitude = pos.split(" ")

        coordinates = dict(longitude=longitude, latitude=latitude)

        return coordinates

    def get_weather(self, city: str, request_type: str = 'web') -> dict:
        city_weather_obj = CityWeather.objects.filter(city_name=city).first()
        time_threshold = timezone.now() - timedelta(minutes=30)

        if not city_weather_obj or city_weather_obj.updated_at < time_threshold:
            city_coordinates = self.get_city_coordinates(city)

            headers = {
                'X-Yandex-Weather-Key': self.weather_api_key
            }
            url = (f'https://api.weather.yandex.ru/v2/forecast?'
                   f'lat={city_coordinates["latitude"]}&'
                   f'lon={city_coordinates["longitude"]}')

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                weather_data = response.json()

                weather_params = {
                    'temperature': weather_data["fact"]["temp"],
                    'atmospheric_pressure': weather_data["fact"]["pressure_mm"],
                    'wind_speed': weather_data["fact"]["wind_speed"]
                }

                city_weather_obj, _ = CityWeather.objects.update_or_create(
                    city_name=city,
                    defaults=weather_params
                )

            except (KeyError, requests.RequestException):
                raise WeatherServiceError("Не удалось получить данные о погоде в городе")

        WeatherRequestsHistory.objects.create(
            city=city_weather_obj,
            request_type=request_type
        )

        return self.serializer(city_weather_obj).data


class WeatherHistoryService:
    def get_weather_history(self, queryset, filters=None):
        if filters:
            request_type = filters.get('request_type')
            if request_type:
                queryset = queryset.filter(request_type=request_type)

        return queryset.select_related('city')
