from django.urls import path

from weather.views import GetWeather, WeatherRequestsHistoryView

urlpatterns = [
    path('weather', GetWeather.as_view()),
    path('requests/', WeatherRequestsHistoryView.as_view())
]
