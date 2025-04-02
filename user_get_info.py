import requests

from secrets import token_url, login, psw

url = "https://estimate-office-staging.smeta.ru/identity/internal/users/74632"
identity_url = "https://estimate-office-staging.smeta.ru/identity/token"

token_data = {
    "login": login,
    "pass": psw,}

identity_token_data = {
    "username": "so_manager",
    "password": "Oc03YGdcGCOu7Cdm",
    "grant_type": "password",
    "scope": "offline_access"
}


def get_manager_token():
    tokenResponse = requests.post(token_url, json=token_data)
    token = tokenResponse.json()['token']
    return token

def get_identity_token():
    identity_token_response = requests.post(identity_url, data=identity_token_data)
    identity_token = identity_token_response.json()['access_token']
    return identity_token


manager_headers = {
    "authorization": "Bearer " + get_identity_token(),
}

newTokenResponse = requests.get(url, headers=manager_headers)
print(newTokenResponse.json())


