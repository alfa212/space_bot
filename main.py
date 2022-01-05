from pathlib import Path
from os.path import splitext
from urllib.parse import urlparse
import os

import requests
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# def fetch_spacex_last_launch(url, dirname):
#     response = requests.get(url)
#     response.raise_for_status()
#
#     all_info = response.json()
#
#     Path(dirname).mkdir(exist_ok=True)
#
#     for i in reversed(all_info):
#         pics_list = i['links']['flickr_images']
#
#         if len(pics_list) > 0:
#             break
#
#     for i, n in enumerate(pics_list):
#         response = requests.get(n)
#         response.raise_for_status()
#
#         with open(f'{dirname}/spacex{i}.jpg', 'wb') as file:
#             file.write(response.content)
#
#
# def fetch_nasa_photos(url, apikey, max_img_count, dirname):
#     payload = {
#         "count": max_img_count,
#         "api_key": apikey
#     }
#
#     response = requests.get(url, params=payload)
#     response.raise_for_status()
#
#     all_info = response.json()
#
#     Path(dirname).mkdir(exist_ok=True)
#
#     for i, n in enumerate(all_info):
#         if "hdurl" not in n:
#             continue
#
#         response = requests.get(n["hdurl"])
#         response.raise_for_status()
#
#         pic_ext = splitext(urlparse(n["hdurl"]).path)[1]
#
#         with open(f'{dirname}/nasa{i}{pic_ext}', 'wb') as file:
#             file.write(response.content)
#
#
# def fetch_nasa_epics(url, apikey, dirname):
#     payload = {
#         "api_key": apikey
#     }
#
#     response = requests.get(url, params=payload)
#     response.raise_for_status()
#
#     all_info = response.json()
#
#     Path(dirname).mkdir(exist_ok=True)
#
#     for i in range(0, len(all_info)):
#         date = all_info[i]['date']
#         image = all_info[i]['image']
#
#         link = f"https://api.nasa.gov/EPIC/archive/natural/{date[:4]}/{date[5:7]}/{date[8:10]}/png/{image}.png?api_key={apikey}"
#
#         response = requests.get(link)
#         response.raise_for_status()
#
#         with open(f'{dirname}/nasa_epic{i}.png', 'wb') as file:
#             file.write(response.content)
#
#
# if __name__ == '__main__':
#     load_dotenv()
#
#     spacex_api = 'https://api.spacexdata.com/v3/launches'
#     spacex_dir = 'images'
#
#     nasa_api_key = os.getenv('NASA_API_KEY')
#
#     nasa_photos_api = 'https://api.nasa.gov/planetary/apod'
#     nasa_photos_max_count = 50
#     nasa_photos_dir = 'nasa_images'
#
#     nasa_epics_api = 'https://api.nasa.gov/EPIC/api/natural'
#     nasa_epics_dir = 'nasa_epics'
#
#     fetch_spacex_last_launch(spacex_api, spacex_dir)
#     fetch_nasa_photos(nasa_photos_api, nasa_api_key, nasa_photos_max_count, nasa_photos_dir)
#     fetch_nasa_epics(nasa_epics_api, nasa_api_key, nasa_epics_dir)

# def hello(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(f'Hello {update.effective_user.first_name}')

load_dotenv()

updater = Updater(os.getenv('TELEGRAM_BOT_TOKEN'))

bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

# bot.send_message(chat_id='@dvmntest', text="Привет")

bot.send_photo(chat_id='@dvmntest', photo=open('images/spacex0.jpg', 'rb'))

# updater.dispatcher.add_handler(CommandHandler('hello', hello))
#
# updater.start_polling()
# updater.idle()