import logging
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


# Переменная окружения (staging или preview)
environment = "стейджинг"

# URL-адреса для разных окружений
base_urls = {
    "стейджинг": "https://estimate-office-staging.smeta.ru",
    "превью": "https://estimate-office-preview.smeta.ru"
}

# Получаем базовый URL для текущего окружения
try:
    base_url = base_urls[environment]
except:
    logger.error(f"Некорректное окружение: {environment}")

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