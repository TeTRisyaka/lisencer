from datetime import datetime
import requests
from secrets import login, psw, tokenUrl, url

now = datetime.now().date()
usrs = 74247, 74598

data = {
    "login": login,
    "pass": psw,}

tokenResponse = requests.post(tokenUrl, json=data)
responceJson = tokenResponse.json()
token = tokenResponse.json()["token"]

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer" + token,
    "cache-control": "no-cache",
    "content-type": "application/json",
    "dnt": "1",
    "origin": "https://estimate-office-staging.smeta.ru",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://estimate-office-staging.smeta.ru/eo-admin/user-licenses",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

data = {
    "first": 0,
    "rows": 15,
    "sortOrder": 1,
    "filters": {
        "id": [{"value": None, "matchMode": "equals", "operator": "and"}],
        "id_invoice": [{"value": None, "matchMode": "equals", "operator": "and"}],
        "id_user": [{"value": usrs[1], "matchMode": "equals", "operator": "and"}],
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
        licenseName = response.json()["rows"][start]["data"][0]["licenseData"][0]["type"]
       # print(formatted_date + " " + licenseName)
        licensePool.insert(start, [formatted_date, licenseName])
        if start < finish - 1:
            start += 1
    except:
      #  print(formatted_date + " Программа")
        licensePool.insert(start, [formatted_date, "Программа"])
        if start < finish - 1:
            start += 1

print(licensePool)
for elem in licensePool:
        try:
            license_date = datetime.strptime(elem[0], "%d-%m-%Y").date()
            #print(license_date)
        except:
            license_date = None

        try:
            days_until_license_over = (license_date - now).days
            if 100 > days_until_license_over > 0:
                print(f'Дней до окончания лицензии {elem[1]} {days_until_license_over}')
        except:
           None

