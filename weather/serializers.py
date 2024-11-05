from rest_framework.serializers import ModelSerializer, CharField

from weather.models import CityWeather, WeatherRequestsHistory


class CityWeatherSerializer(ModelSerializer):
    class Meta:
        model = CityWeather
        fields = "__all__"


class WeatherRequestHistorySerializer(ModelSerializer):
    city_name = CharField(source='city.city_name')

    class Meta:
        model = WeatherRequestsHistory
        fields = ['id', 'city_name', 'request_type', 'created_at']
