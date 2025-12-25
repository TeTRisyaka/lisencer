import requests
import logging
from datetime import datetime, timedelta
from tariff_finder import get_tariff_name
from url_manager import license_url
from user_get_info import get_user_data, get_manager_token

# Настройка логирования
logger = logging.getLogger()

now = datetime.now()
curent_time = now - timedelta(hours=3)
formated_time = datetime.strftime(curent_time, "%Y-%m-%dT%H:%M:%S.%fZ")

headers = {
    "authorization": "Bearer " + get_manager_token(),
}


# Функция для выдачи тарифа
def license_giver(tariff_name, user_url):
    data = {
        "tariff": get_tariff_name(tariff_name),
        "context": 4,
        "activate_time": formated_time,
        "user": get_user_data(user_url)
    }
    give_license = requests.post(license_url, headers=headers, json=data)
    if give_license.status_code == 400:
        logger.warning(f"Лицензия для {tariff_name} не выдана")
    else:
        logger.info(f"Лицензия для {tariff_name} выдана")
