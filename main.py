import requests
from datetime import datetime
from license_giver import license_giver
from url_manager import user_licenses_url, users_url, environment
from user_get_info import get_manager_token, get_user_id_by_email, get_active_users_rg
from users_list import users_emails
import logging

# Настройка логирования
logger = logging.getLogger()
now = datetime.now().date()
active_users = True

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
            "id_user": [{"value": user_id, "matchMode": "equals", "operator": "and"}],
        }
    }

    response = requests.post(user_licenses_url, headers=headers, json=data)
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

        try:
            type = response.json()["rows"][start]["type"]
        except:
            type = None

        license_pool.insert(start, [formatted_date, license_name, status, type])
        if start < finish - 1:
            start += 1
    return license_pool

#Смотрим сколько дней осталось до конца лицензии (при возможности)
def date_checker(elem_date, elem_name, user_url):
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
            logger.info(f'выдаем лицензию для {elem_name} потому что дней до окончания {days_until_license_over}')
            license_giver(elem_name,user_url)
        elif days_until_license_over > 2:
            logger.info(f'Дней до окончания лицензии {elem_name} {days_until_license_over}')
        elif days_until_license_over < 0:
            logger.warning(f'Лицензия на {elem_name} истекла')
            # license_giver(elem_name,user_url)
    except:
        logger.error("Ошибка функции проверки даты")

#Основная функция, которая ходит по лиценз пулу и при активном статусе лицензии вызывает
# проверку даты, либо игнорит лицензию при статусе 0 или 5
def license_puller(user_url, license_pool):
    license_available = []
    i = 0
    while i < len(license_pool):
        if license_pool[i][3] == "3":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "Админ")
            elif license_pool[i][2] in ("1","2") and "Админ" not in license_available:
                date_checker(license_pool[i][0], 'Администраторский тариф', user_url)
        elif license_pool[i][1] == "GESN2022":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "ГЭСН")
            elif license_pool[i][2] in ("1","2") and "ГЭСН" not in license_available:
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "SN2012":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "СН")
            elif license_pool[i][2] in ("1","2") and "СН" not in license_available:
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "TSN_MGE":
            if license_pool[i][2] in ("0","5"):
                license_available.insert(i, "ТСН")
            elif license_pool[i][2] in ("1","2") and "ТСН" not in license_available:
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        elif license_pool[i][1] == "Программа":
            if license_pool[i][2] in ("0","5"):
                    license_available.insert(i, "ПРОГРАММА")
            elif license_pool[i][2] in ("1","2") and "ПРОГРАММА" not in license_available:
                date_checker(license_pool[i][0], license_pool[i][1], user_url)
        i += 1
    if "Админ" in license_available:
        logger.info("Активна лицензия администратора")
    else:
        if "ПРОГРАММА" in license_available:
            logger.info("Лицензия для Программы не требуется")
        if "ГЭСН" in license_available:
            logger.info("Лицензия для ГЭСН не требуется")
        if "ТСН" in license_available:
            logger.info("Лицензия для ТСН не требуется")
        if "СН" in license_available:
            logger.info("Лицензия для СН не требуется")
        logger.info(f'Лицензии в статусе "новая" или "ждет оплаты" {license_available}')

if active_users:
    logger.info(f'Окружение {environment}')
    for user in get_active_users_rg(users_url):
        user_id = get_user_id_by_email(users_url, user)
        user_url = f'{users_url}{user_id}'
        logger.info(f'обработка пользователя {user} id {user_id}')
        license = license_pool_create(user_id)
        license_puller(user_url, license)
else:
    for user in users_emails:
        user_id = get_user_id_by_email(users_url, user)
        user_url = f'{users_url}{user_id}'
        logger.info(f'обработка пользователя {user} id {user_id}')
        license = license_pool_create(user_id)
        license_puller(user_url, license)

