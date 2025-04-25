import requests
import logging
from datetime import datetime

# Настройка логирования
logger = logging.getLogger()

from sensitivity_data import login, psw, username, password, grant_type, scope
from url_manager import token_url, identity_url, users_url


now = datetime.now().date()
date_previous_month = now.replace(year=now.year - 1)
formated_time = datetime.strftime(date_previous_month, "%Y-%m-%dT%H:%M:%S.%fZ")

token_data = {
    "login": login,
    "pass": psw,}

identity_token_data = {
    "username": username,
    "password": password,
    "grant_type": grant_type,
    "scope": scope
}

usrs = []

#Функция для получения токена для менеджера
def get_manager_token():
    token_response = requests.post(token_url, json=token_data)
    token = token_response.json()['token']
    return token

#Функция для получения токена для идентити
def get_identity_token():
    identity_token_response = requests.post(identity_url, data=identity_token_data)
    identity_token = identity_token_response.json()['access_token']
    return identity_token

identity_header = {
    "authorization": "Bearer " + get_identity_token()
}

#Функция для получения данных пользователя из списка
def get_user_data(user_url):
    new_token_response = requests.get(user_url, headers=identity_header)
    user_data = {
        "id": new_token_response.json()['cloudId'],
        "login": new_token_response.json()['userName'],
        "name": new_token_response.json()['fullName'],
        "email": new_token_response.json()['email'],
        "phone": new_token_response.json()['userPhone'],
        "company": new_token_response.json()['userOrg']
    }
    return user_data


#Функция для получения id пользователя по email
def get_user_id_by_email(users_url, user_email):
    data = {
        "filters": {
            "email": [{"value": user_email, "matchMode": "startsWith", "operator": "and"}]
            }}
    try:
        new_token_response = requests.post(users_url, headers=identity_header, json=data)
        user_id = new_token_response.json()['items'][0]['cloudId']
    except:
        logger.error(f'Id пользователя {user_email} не найден')
    return user_id

def get_active_users_rg(users_url):
    data = {
        "filters": {
            "email": [{"value": "@smeta.ru", "matchMode": "endsWith", "operator": "and"}],
            "lastOnlineDateTime": [{"value": formated_time, "matchMode": "dateAfter", "operator": "and"}]
        },
        "rows":100
    }
    new_token_response = requests.post(users_url, headers=identity_header, json=data)
    user_list = new_token_response.json()
    emails = [user["email"] for user in user_list["items"] if "email" in user]
    print(emails)
    return emails
