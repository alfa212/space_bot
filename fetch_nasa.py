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


def fetch_nasa_epics(url, apikey, dirname):
    payload = {
        "api_key": apikey
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    all_info = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for i in range(0, len(all_info)):
        date = all_info[i]['date']
        image = all_info[i]['image']

        link = f"https://api.nasa.gov/EPIC/archive/natural/{date[:4]}/{date[5:7]}/{date[8:10]}/png/{image}.png?api_key={apikey}"

        response = requests.get(link)
        response.raise_for_status()

        with open(f'{dirname}/nasa_epic{i}.png', 'wb') as file:
            file.write(response.content)
