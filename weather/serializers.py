from rest_framework.serializers import ModelSerializer

from weather.models import CityWeather


class CityWeatherSerializer(ModelSerializer):
    class Meta:
        model = CityWeather
        fields = "__all__"
