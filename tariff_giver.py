from license_giver import license_giver
from sensitivity_data import users_url
from users_list import user_for_license_giving

tariffs = ("GESN2022", "Программа", "TSN_MGE", "SN2012")

print(f'обработка id {user_for_license_giving}')
for tariff in tariffs:
    user_url = f'{users_url}{user_for_license_giving}'
    license_giver(tariff, user_url)
