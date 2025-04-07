from license_giver import license_giver
from sensitivity_data import users_url
from users_list import users_for_license_giving

tariffs = ("GESN2022", "Программа", "TSN_MGE", "SN2012")


for user in users_for_license_giving:
    print(f'обработка id {user}')
    for tariff in tariffs:
        user_url = f'{users_url}{user}'
        license_giver(tariff, user_url)
