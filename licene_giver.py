from datetime import datetime

import requests

from licenses import get_tariff_name
from secrets import license_url
from user_get_info import get_user_data, get_manager_token

now = datetime.now()
formated_time = datetime.strftime(now, "%Y-%m-%dT%H:%M:%S.%fZ")

headers = {
    "authorization": "Bearer " + get_manager_token(),
}


def license_giver(tariff_name):
    data = {
        "tariff": get_tariff_name(tariff_name),
        "context": 4,
        "activate_time": formated_time,
        "user": get_user_data()
    }
    response_for_license = requests.post(license_url, headers=headers, json=data)
    print(f"Лицензия для {tariff_name} выдана")