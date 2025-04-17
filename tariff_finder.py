import requests
import logging
from url_manager import tariff_url
from user_get_info import get_manager_token

# Настройка логирования
logger = logging.getLogger()


headers = {
    "authorization": "Bearer " + get_manager_token(),
}

#Функция достает данные о необходимых тарифах из общего списка
def get_tariff_name(tariff_name):
    all_tariffs_response = requests.get(tariff_url, headers=headers)
    tariff = None
    if tariff_name == 'GESN2022':
        tariff_name = "Только ФСНБ"
    elif tariff_name == 'Программа':
        tariff_name = "Только Программа"
    elif tariff_name == 'TSN_MGE':
        tariff_name = "Только ТСН"
    elif tariff_name == 'SN2012':
        tariff_name = "Только СН"
    for i in all_tariffs_response.json():
        if i["name"] == tariff_name:
            tariff = i
            logger.info(f"Тариф найден: {tariff_name}")
    if tariff is None:
        logger.warning(f"Тариф не найден: {tariff_name}")
    return tariff

