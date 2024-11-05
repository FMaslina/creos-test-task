import os

import django
import telebot
from dotenv import load_dotenv
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from tg_bot.service import TelegramBotService

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creos.settings')
django.setup()

bot_token = os.getenv("TG_BOT_TOKEN")

bot = telebot.TeleBot(bot_token, parse_mode=None)

service = TelegramBotService()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = """
    Это погодный бот,
    вы можете узнать
    погоду по названию
    города, или по геолокации!
    """

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button_city = KeyboardButton("Узнать погоду")
    markup.add(button_city)

    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: message.text == "Узнать по городу")
def request_city_name(message):
    bot.send_message(message.chat.id, "Введите название города:")


@bot.message_handler(func=lambda message: message.text is not None)
def get_weather_by_city(message):
    city = message.text
    weather_info = service.get_weather(city)
    bot.send_message(message.chat.id, weather_info)


bot.infinity_polling()
