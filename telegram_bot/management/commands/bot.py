from django.core.management import BaseCommand
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from creos import settings
from telegram_bot.service import TelegramBotService

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN, threaded=False)


service = TelegramBotService()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Это погодный бот, вы можете узнать погоду по названию города"

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_city = KeyboardButton("Узнать погоду")
    markup.add(button_city)

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Узнать погоду")
def request_city_name(message):
    bot.send_message(message.chat.id, "Введите название города:")


@bot.message_handler(func=lambda message: message.text is not None)
def get_weather_by_city(message):
    city = message.text
    weather_info = service.get_weather(city)
    bot.send_message(message.chat.id, weather_info)


class Command(BaseCommand):
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        bot.infinity_polling()
