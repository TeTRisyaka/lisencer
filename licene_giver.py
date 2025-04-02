import requests

from main import headers
from secrets import license_url

data = {
    "tariff": {
        "badge": {
            "text": "new ",
            "textColor": "#ffffff",
            "bgColor": "#5654DB"
        },
        "id": "22",
        "name": "Программа с ФСНБ-2022",
        "type": "1",
        "amount": "1",
        "duration": "1",
        "icon": "https://staging-storage.smeta.ru/smetaru/estimate-office/tariffs/gesn_1.png",
        "status": "1",
        "custom_license_data": None,
        "sort": "1",
        "created_at": "2025-03-20T05:25:08.099Z",
        "updated_at": "2025-03-20T10:39:01.477Z",
        "deleted_at": None,
        "license_data": [
            {
                "id": "1",
                "type": "0",
                "base_type": None,
                "name": "Программа",
                "duration": "1",
                "cost": "500.00",
                "data": {
                    "licenseDuration": 1,
                    "licenseData": [
                        {
                            "applicationType": 0,
                            "licenseDataType": 0
                        }
                    ]
                },
                "AvailableLicenseTariff": {
                    "id": "164",
                    "id_available_license": "1",
                    "id_tariff": "22"
                }
            },
            {
                "id": "19",
                "type": "2",
                "base_type": "GESN2022",
                "name": "ФСНБ-2022",
                "duration": "1",
                "cost": "125.00",
                "data": {
                    "licenseDuration": 1,
                    "licenseData": [
                        {
                            "type": "GESN2022",
                            "baseInfo": [],
                            "licenseDataType": 1
                        },
                        {
                            "type": "GESN2022",
                            "baseInfo": [],
                            "regionCode": None,
                            "yearInfo": [],
                            "quarterInfo": [],
                            "priceZoneInfo": [],
                            "licenseDataType": 3
                        }
                    ]
                },
                "AvailableLicenseTariff": {
                    "id": "165",
                    "id_available_license": "19",
                    "id_tariff": "22"
                }
            }
        ]
    },
    "context": 4,
    "activate_time": "2025-03-29T12:43:30.935Z",
    "user": {
        "id": 74598,
        "login": "TeTRis21_Auto",
        "name": "1  2",
        "email": "tetriskamana@gmail.com",
        "phone": "79999999999",
        "company": None
    }
}


def license_giver():
    response_for_license = requests.post(license_url, headers=headers, json=data)