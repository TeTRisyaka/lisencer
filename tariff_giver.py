import logging
from license_giver import license_giver
from main import user
from sensitivity_data import users_url
from user_get_info import get_user_id_by_email
from users_list import users_emails, users_for_license_giving

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

users_email = "tetriskamana@gmail.com"
tariffs = ("GESN2022", "Программа", "TSN_MGE", "SN2012")


logger.info(f'обработка пользователя {users_email} id {get_user_id_by_email(users_url, users_email)}')
for tariff in tariffs:
        user_url = f'{users_url}{get_user_id_by_email(users_url, users_email)}'
        license_giver(tariff, user_url)

# for user in users_for_license_giving:
#     logger.info(f'обработка пользователя {user} id {get_user_id_by_email(users_url, user)}')
#     for tariff in tariffs:
#         user_url = f'{users_url}{get_user_id_by_email(users_url, user)}'
#         license_giver(tariff, user_url)