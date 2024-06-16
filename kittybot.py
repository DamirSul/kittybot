import os
import logging

import requests
from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv()

secret_token = os.getenv('TOKEN')

bot = TeleBot(token=secret_token)
URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())

@bot.message_handler(commands=['delete'])
def delete_keyboard(message):
    chat = message.chat
    bot.send_message(
        chat_id=chat.id,
        text=f'Удаляю клавиатуру! Чтобы она снова появилась, введите /start.',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    

@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_newcat = types.KeyboardButton('/newcat')
    keyboard.row(
        types.KeyboardButton('Который час?'),
        types.KeyboardButton('Определи мой ip'),
    )
    keyboard.row(
        types.KeyboardButton('/random_digit'),
        types.KeyboardButton('/delete')
    )
    keyboard.add(button_newcat)

    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        reply_markup=keyboard,
    )

    bot.send_photo(chat.id, get_new_image())

@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KityyBot!')



def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
