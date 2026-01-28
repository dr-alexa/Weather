import telebot
import os
import sqlite3
from dotenv import load_dotenv
from urllib3.util.request import body_to_chunks
import requests
import json


load_dotenv()
token_tg = os.getenv('TOKEN_TG')
weather_api = os.getenv('WEATHER_API')
bot = telebot.TeleBot(token_tg)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Рада видеть. Чтобы узнать погоду, мне нужен твой... город :)')


@bot.message_handler(content_types=['text'])
def send_pogoda(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric') #url на сайт (openweather) с погодой для каждого города
    if res.status_code == 200:

        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Вот что передают: {data["main"]["temp"]}') #получить все данные с сайта, вывести их в формате json

        #изображение
        if temp < 5.0:
            image = 'istockphoto-1047001668-170667a.jpg'
            file = open('./' + image, 'rb')
            bot.send_photo(message.chat.id, file)
        else:
            image = 'OIP (4).webp' if temp > 5.0 else 'sun-cloud.webp'
            file = open('./' + image, 'rb') #обращение к текущей директории
            bot.send_photo(message.chat.id, file)

    else:
        bot.reply_to(message, 'Точно тот город?')


bot.polling(none_stop=True)