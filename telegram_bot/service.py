from weather.services import WeatherService


class TelegramBotService:
    def __init__(self):
        self._weather_service = WeatherService()

    def get_weather(self, city):
        weather = self._weather_service.get_weather(city=city, request_type="telegram")

        weather_formatted = (f"Погода в городе {city}:\nТемпература: {weather["temperature"]}\n"
                             f"Атмосферное давление: {weather["atmospheric_pressure"]}\n"
                             f"Скорость ветра: {weather["wind_speed"]}")

        return weather_formatted
