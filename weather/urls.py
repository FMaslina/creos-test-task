from django.urls import path

from weather.views import GetWeather

urlpatterns = [
    path('weather', GetWeather.as_view())
]
