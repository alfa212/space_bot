from pathlib import Path
from os.path import splitext
from urllib.parse import urlparse

import requests


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
