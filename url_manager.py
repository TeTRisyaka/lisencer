# Переменная окружения (staging или preview)
environment = "preview"

# URL-адреса для разных окружений
base_urls = {
    "staging": "https://estimate-office-staging.smeta.ru",
    "preview": "https://estimate-office-preview.smeta.ru"
}

# Получаем базовый URL для текущего окружения
base_url = base_urls[environment]

# Формируем URL-адреса для текущего окружения
def get_urls():
    return {
        "token_url": f"{base_url}/eo-admin/manager/admin-manager/login",
        "user_licenses_url": f"{base_url}/eo-admin/manager/invoice-manager/getUserLicenses",
        "license_url": f"{base_url}/eo-admin/manager/license-manager/createInvoice",
        "identity_url": f"{base_url}/identity/token",
        "users_url": f"{base_url}/identity/internal/users/",
        "tariff_url": f"{base_url}/eo-admin/manager/license-manager/tariff"
    }

# Экспортируем URL-адреса
urls = get_urls()
token_url = urls["token_url"]
user_licenses_url = urls["user_licenses_url"]
license_url = urls["license_url"]
identity_url = urls["identity_url"]
users_url = urls["users_url"]
tariff_url = urls["tariff_url"]