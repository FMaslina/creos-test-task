# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.services import WeatherService


class GetWeather(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = WeatherService()

    def get(self, request):
        city = request.query_params.get('city')
        return Response(status=status.HTTP_200_OK, data=self.service.get_weather(city=city))
