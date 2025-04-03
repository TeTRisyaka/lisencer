import requests

from secrets import token_url, login, psw, identity_url, user_url

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


identity_header = {
    "authorization": "Bearer " + get_identity_token()
}

def get_user_data():
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


