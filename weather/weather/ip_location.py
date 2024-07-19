from urllib.parse import urljoin

import requests

BASE_URL = "https://ipapi.co/"


def get_location_by_ip(ip) -> str:
    req = requests.get(url=urljoin(BASE_URL, urljoin(str(ip), "json")))
    data = req.json()
    return data["city"]
