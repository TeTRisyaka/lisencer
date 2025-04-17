import logging
from license_giver import license_giver
from url_manager import users_url, environment
from user_get_info import get_user_id_by_email

# Настройка логирования
logger = logging.getLogger()
tariffs = ("GESN2022", "Программа", "TSN_MGE", "SN2012")

user_email = "dsadsacvfrte564"


logger.info(f'Окружение {environment} '
            f'обработка пользователя {user_email} id {get_user_id_by_email(users_url, user_email)}')
for tariff in tariffs:
        user_url = f'{users_url}{get_user_id_by_email(users_url, user_email)}'
        license_giver(tariff, user_url)
