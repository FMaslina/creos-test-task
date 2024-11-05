from weather.services import WeatherService


class TelegramBotService:
    def __init__(self):
        self._weather_service = WeatherService()

    def get_weather(self, city):
        weather = self._weather_service.get_weather(city=city, request_type="telegram")

        weather_formatted = f"""
            Погода в городе: {city}\n\n
            Температура: {weather["temperature"]}\n
            Атмосферное давление: {weather["atmospheric_pressure"]}\n
            Скорость ветра: {weather["wind_speed"]}
            """

        return weather_formatted
