# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.misc.paginator import StandardResultsSetPagination
from weather.filters import WeatherRequestsFilter
from weather.models import WeatherRequestsHistory
from weather.serializers import WeatherRequestHistorySerializer
from weather.services import WeatherService, WeatherHistoryService


class GetWeather(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = WeatherService()

    def get(self, request):
        city = request.query_params.get('city')
        return Response(status=status.HTTP_200_OK, data=self.service.get_weather(city=city))


class WeatherRequestsHistoryView(ListAPIView):
    serializer_class = WeatherRequestHistorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = WeatherRequestsFilter
    ordering_fields = ['city__city_name', 'created_at']
    ordering = ['-created_at']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = WeatherHistoryService()

    def get_queryset(self):
        filters = self.request.query_params.dict()
        base_queryset = WeatherRequestsHistory.objects.all()
        return self.service.get_weather_history(base_queryset, filters)
