from pathlib import Path
from os.path import splitext
from urllib.parse import urlparse

import requests


def fetch_nasa_photos(url, apikey, max_img_count, dirname):
    payload = {
        "count": max_img_count,
        "api_key": apikey
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    all_photos_desc = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for photo_num, photo_arr in enumerate(all_photos_desc):
        if "hdurl" not in photo_arr:
            continue

        response = requests.get(photo_arr["hdurl"])
        response.raise_for_status()

        pic_ext = splitext(urlparse(photo_arr["hdurl"]).path)[1]

        with open(f'{dirname}/nasa{photo_num}{pic_ext}', 'wb') as file:
            file.write(response.content)


def fetch_nasa_epics(url, apikey, dirname):
    payload = {
        "api_key": apikey
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    all_photos_desc = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for photo_num in range(0, len(all_photos_desc)):
        date = all_photos_desc[photo_num]['date']
        image = all_photos_desc[photo_num]['image']

        link = f"https://api.nasa.gov/EPIC/archive/natural/{date[:4]}/{date[5:7]}/{date[8:10]}/png/{image}.png?api_key={apikey}"

        response = requests.get(link)
        response.raise_for_status()

        with open(f'{dirname}/nasa_epic{photo_num}.png', 'wb') as file:
            file.write(response.content)
