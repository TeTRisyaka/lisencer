import requests
from datetime import datetime
from license_giver import license_giver
from sensitivity_data import url, users_url
from user_get_info import get_manager_token
from users_list import usrs

now = datetime.now().date()

#Создает удобный пул лицензий для конкретного пользователя
def license_pool_create(user_id):

    headers = {
        "authorization": "Bearer " + get_manager_token(),
    }
    data = {
        "first": 0,
        "rows": 15,
        "sortOrder": 1,
        "filters": {
            "id": [{"value": None, "matchMode": "equals", "operator": "and"}],
            "id_invoice": [{"value": None, "matchMode": "equals", "operator": "and"}],
            "id_user": [{"value": user_id, "matchMode": "equals", "operator": "and"}],
            "type": [{"value": None, "matchMode": "in", "operator": "and"}],
            "access_type": [{"value": None, "matchMode": "in", "operator": "and"}],
            "duration": [{"value": None, "matchMode": "equals", "operator": "and"}],
            "create_time": [{"value": None, "matchMode": "dateIs", "operator": "and"}],
            "start_time": [{"value": None, "matchMode": "dateIs", "operator": "and"}],
            "end_time": [{"value": None, "matchMode": "dateIs", "operator": "and"}],
            "create_method": [{"value": None, "matchMode": "in", "operator": "and"}],
            "status": [{"value": None, "matchMode": "in", "operator": "and"}]
        },
        "globalFilter": None
    }

    response = requests.post(url, headers=headers, json=data)
    start = 0
    finish = len(response.json()["rows"])
    license_pool = []
    for item in response.json()["rows"]:
        try:
            date = response.json()["rows"][start]["end_time"]
            dt = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = dt.strftime("%d-%m-%Y")
        except:
            formatted_date = "Дата окончания отсутствует"

        try:
            status = response.json()["rows"][start]["status"]
        except:
            status = None

        try:
            license_name = response.json()["rows"][start]["data"][0]["licenseData"][0]["type"]
        except:
            license_name = "Программа"
        license_pool.insert(start, [formatted_date, license_name, status])
        if start < finish - 1:
            start += 1
    return license_pool

#Смотрим сколько дней осталось до конца лицензии (при возможности)
def date_checker(elem_date, elem_name, user_url):
    # i = 0
    try:
        license_date = datetime.strptime(elem_date, "%d-%m-%Y").date()
    except:
        license_date = None
    try:
        days_until_license_over = (license_date - now).days
    except:
        days_until_license_over = None
    try:
            if 0 <= days_until_license_over <= 2:
                print(f'выдаем лицензию для {elem_name} потому что дней до окончания {days_until_license_over}')
                license_giver(elem_name,user_url)
            elif 2 <= days_until_license_over <= 100:
                print(f'Дней до окончания лицензии {elem_name} {days_until_license_over}')
    except:
        print("Ошибка функции")

#Основная функция, которая ходит по лиценз пулу и при активном статусе лицензии вызывает
# проверку даты, либо игнорит лицензию при статусе 0 или 5
def license_puller(user_url, license_pool):
    license_available = []
    i = 0
    while i < len(license_pool):
        if license_pool[i][1] == "GESN2022":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "ГЭСН")
            elif license_pool[i][2] in ("1","2") and "ГЭСН" not in license_available:
                            #print("Проверяем даты для ГЭСН")
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "SN2012":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "СН")
            elif license_pool[i][2] in ("1","2") and "СН" not in license_available:
                            #print("Проверяем даты СН")
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "TSN_MGE":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "ТСН")
            elif license_pool[i][2] in ("1","2") and "ТСН" not in license_available:
                            #print("Проверяем даты ТСН")
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "Программа":
            if license_pool[i][2] in ("0","5"):
                    license_available.insert(i, "ПРОГРАММА")
            elif license_pool[i][2] in ("1","2") and "ПРОГРАММА" not in license_available:
                            #print("Проверяем даты программа")
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        i += 1
    if "ПРОГРАММА" in license_available:
        print("Лицензия для Программы не требуется")
    if "ГЭСН" in license_available:
        print("Лицензия для ГЭСН не требуется")
    if "ТСН" in license_available:
        print("Лицензия для ТСН не требуется")
    if "СН" in license_available:
        print("Лицензия для СН не требуется")
    print(f'Лицензии в статусе "новая" или "ждет оплаты" {license_available}')


for user in usrs:
    user_url = f'{users_url}{user}'
    print(f'обработка id {user}')
    license = license_pool_create(user)
    license_puller(user_url, license)

