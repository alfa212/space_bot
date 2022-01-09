from pathlib import Path
from os.path import splitext
from urllib.parse import urlparse

import requests


def fetch_spacex_last_launch(url, dirname):
    response = requests.get(url)
    response.raise_for_status()

    all_launches = response.json()

    Path(dirname).mkdir(exist_ok=True)

    for launch in reversed(all_launches):
        launch_photos = launch['links']['flickr_images']

        if len(launch_photos) > 0:
            break

    for photo_num, photo_link in enumerate(launch_photos):
        response = requests.get(photo_link)
        response.raise_for_status()

        with open(f'{dirname}/spacex{photo_num}.jpg', 'wb') as file:
            file.write(response.content)
