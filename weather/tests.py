import requests
from django.test import TestCase
from unittest.mock import patch, MagicMock

from requests import RequestException
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework import status

from .exceptions import WeatherServiceError
from .views import GetWeather, WeatherRequestsHistoryView
from .services import WeatherService, WeatherHistoryService
from .models import CityWeather, WeatherRequestsHistory


class GetWeatherTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GetWeather.as_view()

    @patch('weather.services.WeatherService.get_weather')
    def test_get_weather_success(self, mock_get_weather):
        mock_get_weather.return_value = {'temperature': 20, 'atmospheric_pressure': 1012, 'wind_speed': 5}

        request = self.factory.get('/weather', {'city': 'Москва'})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'temperature': 20, 'atmospheric_pressure': 1012, 'wind_speed': 5})


class WeatherServiceTestCase(TestCase):
    def setUp(self):
        self.service = WeatherService()
        self.city = "Москва"

    @patch('weather.services.WeatherService.get_city_coordinates')
    @patch('weather.services.requests.get')
    def test_get_weather_from_api(self, mock_requests_get, mock_get_city_coordinates):
        mock_get_city_coordinates.return_value = {'latitude': '55.7558', 'longitude': '37.6173'}

        mock_weather_data = {
            "fact": {
                "temp": 20,
                "pressure_mm": 1012,
                "wind_speed": 5
            }
        }
        mock_requests_get.return_value = MagicMock(status_code=200, json=lambda: mock_weather_data)

        weather_data = self.service.get_weather(city=self.city)

        self.assertEqual(weather_data['temperature'], 20)
        self.assertEqual(weather_data['atmospheric_pressure'], 1012)
        self.assertEqual(weather_data['wind_speed'], 5)

        city_weather_obj = CityWeather.objects.get(city_name=self.city)
        self.assertEqual(city_weather_obj.temperature, 20)


class WeatherHistoryServiceTestCase(TestCase):
    def setUp(self):
        self.service = WeatherHistoryService()
        self.city_weather = CityWeather.objects.create(city_name="Москва", temperature=20, atmospheric_pressure=1012,
                                                       wind_speed=5)
        self.history1 = WeatherRequestsHistory.objects.create(city=self.city_weather, request_type="web")
        self.history2 = WeatherRequestsHistory.objects.create(city=self.city_weather, request_type="mobile")

    def test_get_weather_history_with_filters(self):
        queryset = WeatherRequestsHistory.objects.all()
        filters = {'request_type': 'web'}

        filtered_queryset = self.service.get_weather_history(queryset, filters)

        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first().request_type, 'web')

    def test_get_weather_history_without_filters(self):
        queryset = WeatherRequestsHistory.objects.all()
        filtered_queryset = self.service.get_weather_history(queryset, filters=None)

        self.assertEqual(filtered_queryset.count(), 2)


class WeatherRequestsHistoryViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = WeatherRequestsHistoryView.as_view()
        self.city_weather = CityWeather.objects.create(city_name="Москва", temperature=20, atmospheric_pressure=1012,
                                                       wind_speed=5)
        WeatherRequestsHistory.objects.create(city=self.city_weather, request_type="web")
        WeatherRequestsHistory.objects.create(city=self.city_weather, request_type="mobile")

    def test_get_weather_requests_history(self):
        request = self.factory.get('/weather-requests-history')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_weather_requests_history_with_ordering(self):
        request = self.factory.get('/weather-requests-history', {'ordering': 'city__city_name'})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
