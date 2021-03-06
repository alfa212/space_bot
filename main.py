import os
from os import listdir
import time

from dotenv import load_dotenv
import telegram

import fetch_spacex
import fetch_nasa


def post_photo(token, pause, channel, remove, *dirs):
    bot = telegram.Bot(token=token)

    for dir in dirs:
        for photo in listdir(dir):
            with open(f'{dir}/{photo}', 'rb') as photo_file:
                bot.send_photo(chat_id=channel, photo=photo_file)
            if remove == 'Y':
                os.remove(f'{dir}/{photo}')
            time.sleep(pause)


if __name__ == '__main__':
    load_dotenv()

    spacex_api = 'https://api.spacexdata.com/v3/launches'
    spacex_dir = 'images'

    nasa_api_key = os.getenv('NASA_API_KEY')

    nasa_photos_api = 'https://api.nasa.gov/planetary/apod'
    nasa_photos_max_count = 50
    nasa_photos_dir = 'nasa_images'

    nasa_epics_api = 'https://api.nasa.gov/EPIC/api/natural'
    nasa_epics_dir = 'nasa_epics'

    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')

    target_channel = os.getenv('TARGET_CHANNEL')

    timeout = int(os.getenv('PHOTO_POST_TIMEOUT', 86400))

    remove_photo = os.getenv('REMOVE_PHOTO', 'Y')

    dirs_images = []

    while True:
        try:
            dirs_images = listdir(spacex_dir) + listdir(nasa_photos_dir) + listdir(nasa_epics_dir)
        except FileNotFoundError:
            pass

        if dirs_images:
            post_photo(tg_token, timeout, target_channel, remove_photo, spacex_dir, nasa_photos_dir, nasa_epics_dir)
        else:
            fetch_spacex.fetch_spacex_last_launch(spacex_api, spacex_dir)
            fetch_nasa.fetch_nasa_photos(nasa_photos_api, nasa_api_key, nasa_photos_max_count, nasa_photos_dir)
            fetch_nasa.fetch_nasa_epics(nasa_epics_api, nasa_api_key, nasa_epics_dir)
