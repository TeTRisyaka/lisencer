from datetime import datetime
import requests

from licene_giver import license_giver
from secrets import url, usrs
from user_get_info import get_manager_token

now = datetime.now().date()

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
        "id_user": [{"value": usrs[3], "matchMode": "equals", "operator": "and"}],
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
licensePool = []

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
        licenseName = response.json()["rows"][start]["data"][0]["licenseData"][0]["type"]
        #print(formatted_date + " " + licenseName)
    except:
        #  print(formatted_date + " Программа")
        licenseName = "Программа"
    licensePool.insert(start, [formatted_date, licenseName, status])
    if start < finish - 1:
        start += 1

license_give = []


# def license_cheker(licence_name):
#     i = 0
#     while i < len(licensePool):
#         if licensePool[i][1] == licence_name:
#             del licensePool[i]
#                 # print(f'удалены лицензии для {licence_name}')
#             i -= 1
#         i += 1


# def finish_license_remover(license_name):
#     i = 0
#     while i < len(licensePool):
#         if licensePool[i][1] == license_name and licensePool[i][2] == "2":
#             del licensePool[i]
#         # print(f'удалены лицензии для {licence_name}')
#             i -= 1
#         i += 1


def date_checker(elem_date, elem_name):
    i = 0
    try:
        license_date = datetime.strptime(elem_date, "%d-%m-%Y").date()
    except:
        license_date = None
    try:
        days_until_license_over = (license_date - now).days
    except:
        days_until_license_over = None
    try:
            if days_until_license_over <= 2:
                print(f'выдаем лицензию для {elem_name}')
                license_give.insert(i, [elem_date, elem_name])
                i += 1
                license_giver(elem_name)
            else:
                print(f'Дней до окончания лицензии {elem_name} {days_until_license_over}')
    except:
        print("Ошибка функции")


#print(licensePool)

i = 0
while i < len(licensePool):
        if licensePool[i][1] == "GESN2022":
            if licensePool[i][2] == "0":
                print("Лицензия для ГЭСН не требуется")
            #     license_cheker(licensePool[i][1])
            #     i -= 1
            elif licensePool[i][2] == "1" or "2":
                #print("Проверяем даты для ГЭСН")
                date_checker(licensePool[i][0], licensePool[i][1])
                # i -= 1
        elif licensePool[i][1] == "SN2012":
            if licensePool[i][2] == "0":
                print("Лицензия для СН не требуется")
            #     license_cheker(licensePool[i][1])
            #     i-=1
            elif licensePool[i][2] == "1" or "2":
                #print("Проверяем даты СН")
                date_checker(licensePool[i][0], licensePool[i][1])
                # i -= 1
        elif licensePool[i][1] == "TSN_MGE":
            if licensePool[i][2] == "0":
                 print("Лицензия для ТСН не требуется")
            #     license_cheker(licensePool[i][1])
            #     i-=1
            elif licensePool[i][2] == "1" or "2":
                #print("Проверяем даты ТСН")
                date_checker(licensePool[i][0], licensePool[i][1])
                # i -= 1
        elif licensePool[i][1] == "Программа":
            if licensePool[i][2] == "0":
                 print("Лицензия для Программы не требуется")
            #     license_cheker(licensePool[i][1])
            #     i-=1
            elif licensePool[i][2] == "1" or "2":
                #print("Проверяем даты программа")
                date_checker(licensePool[i][0], licensePool[i][1])
                # i -= 1
        i += 1

#print(license_give)



