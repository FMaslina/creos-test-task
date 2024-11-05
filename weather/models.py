from django.db import models

from core.models.base import TimeStampModel


class CityWeather(TimeStampModel):
    city_name = models.CharField(max_length=64, verbose_name="Название города", unique=True)
    temperature = models.FloatField(verbose_name="Температура в городе")
    atmospheric_pressure = models.IntegerField(verbose_name="Атмосферное давление")
    wind_speed = models.FloatField(verbose_name="Скорость ветра")

    class Meta:
        verbose_name = "Погода по городу"
        verbose_name_plural = "Погода по городам"


class WeatherRequestsHistory(TimeStampModel):
    city = models.ForeignKey(CityWeather, on_delete=models.CASCADE)
    request_type = models.CharField(
        max_length=20,
        choices=[('web', 'Web'), ('telegram', 'Telegram')],
        default='web'
    )
