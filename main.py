from pathlib import Path
from os.path import splitext
from urllib.parse import urlparse
import os

import requests
from dotenv import load_dotenv


def fetch_spacex_last_launch(url, dirname):
    response = requests.get(url)
    response.raise_for_status()

    all_info = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for i in reversed(all_info):
        pics_list = i['links']['flickr_images']

        if len(pics_list) > 0:
            break

    for i, n in enumerate(pics_list):
        response = requests.get(n)
        response.raise_for_status()

        with open(f'{dirname}/spacex{i}.jpg', 'wb') as file:
            file.write(response.content)


def take_nasa_photos(url, apikey, max_img_count, dirname):
    payload = {
        "count": max_img_count,
        "api_key": apikey
    }
    
    response = requests.get(url, params=payload)
    response.raise_for_status()

    all_info = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for i, n in enumerate(all_info):
        if "hdurl" not in n:
            continue

        response = requests.get(n["hdurl"])
        response.raise_for_status()

        pic_ext = splitext(urlparse(n["hdurl"]).path)[1]

        with open(f'{dirname}/nasa{i}{pic_ext}', 'wb') as file:
            file.write(response.content)


def take_nasa_epics(url, apikey, dirname):
    payload = {
        "api_key": apikey
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    all_info = response.json()

    for i in range(0, len(all_info)):
        date = all_info[i]['date']
        image = all_info[i]['image']

        link = f"https://api.nasa.gov/EPIC/archive/natural/{date[:4]}/{date[5:7]}/{date[8:10]}/png/{image}.png?api_key={apikey}"

        response = requests.get(link)
        response.raise_for_status()

        Path(dirname).mkdir(exist_ok=True)

        with open(f'{dirname}/nasa_epic{i}.png', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    load_dotenv()

    spacex_api = 'https://api.spacexdata.com/v3/launches'
    spacex_dir = 'images'

    nasa_api_key = os.getenv('NASA_API_KEY')

    nasa_photos_api = 'https://api.nasa.gov/planetary/apod'
    nasa_photos_max_count = 50
    dir_for_nasa_photos = 'nasa_images'

    nasa_epics_api = 'https://api.nasa.gov/EPIC/api/natural'
    dir_for_nasa_epics = 'nasa_epics'

    fetch_spacex_last_launch(spacex_api, spacex_dir)
    take_nasa_photos(nasa_photos_api, nasa_api_key, nasa_photos_max_count, dir_for_nasa_photos)
    take_nasa_epics(nasa_epics_api, nasa_api_key, dir_for_nasa_epics)