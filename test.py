import requests

url = "https://estimate-office-staging.smeta.ru/identity/token"



data = {
    "username": "so_manager",
    "password": "Oc03YGdcGCOu7Cdm",
    "grant_type": "password",
    "scope": "offline_access"
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())