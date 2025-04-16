from license_giver import license_giver
from sensitivity_data import users_url
from user_get_info import get_user_id_by_email
from users_list import users_for_license_giving

tariffs = ("GESN2022", "Программа", "TSN_MGE", "SN2012")


for user in users_for_license_giving:
    print(f'обработка пользователя {user} id {get_user_id_by_email(users_url, user)}')
    for tariff in tariffs:
        user_url = f'{users_url}{get_user_id_by_email(users_url, user)}'
        license_giver(tariff, user_url)
