from django_filters import rest_framework as filters

from weather.models import WeatherRequestsHistory


class WeatherRequestsFilter(filters.FilterSet):
    class Meta:
        model = WeatherRequestsHistory
        fields = ['request_type']
