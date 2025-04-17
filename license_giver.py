import requests
import logging
from datetime import datetime
from tariff_finder import get_tariff_name
from sensitivity_data import license_url
from user_get_info import get_user_data, get_manager_token

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

now = datetime.now()
formated_time = datetime.strftime(now, "%Y-%m-%dT%H:%M:%S.%fZ")

headers = {
    "authorization": "Bearer " + get_manager_token(),
}

#Функция для выдачи тарифа
def license_giver(tariff_name, user_url):
    data = {
        "tariff": get_tariff_name(tariff_name),
        "context": 4,
        "activate_time": formated_time,
        "user": get_user_data(user_url)
    }
    requests.post(license_url, headers=headers, json=data)
    logger.info(f"Лицензия для {tariff_name} выдана")