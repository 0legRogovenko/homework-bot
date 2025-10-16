import os

from dotenv import load_dotenv

load_dotenv()

# Токены и настройки окружения
PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
REQUIRED_TOKENS = ('PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID')

# Основные параметры
RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses'
HEADERS = {
    'Authorization': f'OAuth {PRACTICUM_TOKEN}',
}

# Возможные вердикты проверки
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

STATUS_OK = 200

# Сообщения об ошибках и логах
API_REQUEST_ERROR_MSG = (
    'Ошибка при запросе к API: {error}. '
    'Эндпоинт {endpoint} недоступен. '
    'Код ответа API: {status_code}, '
    'Текст ответа: {text}, '
    'URL запроса: {url}, '
    'Params: {params}'
)

MESSAGE_SEND_ERROR_MSG = (
    'Не удалось отправить сообщение в чат {chat_id}: {error}. '
    'Текст сообщения: {message}'
)

MESSAGE_SENT_LOG_MSG = (
    'Сообщение отправлено в чат {chat_id}. '
    'Текст сообщения: {message}'
)

MISSING_ENV_VAR_MSG = (
    'Отсутствует обязательная переменная окружения: {name}'
)

UNKNOWN_STATUS_MSG = (
    'Неизвестный статус работы: {status}'
)

ENDPOINT_UNAVAILABLE_ERROR_MSG = (
    'Эндпоинт {endpoint} недоступен. '
    'Код ответа API: {status_code}, '
    'Текст ответа: {text}, '
    'URL запроса: {url}'
)

API_RESPONSE_ERROR_MSG = (
    'Ошибка в ответе API: {data}. '
    'Эндпоинт: {endpoint}, '
    'Params: {params}'
)

API_RESPONSE_NOT_DICT_ERROR_MSG = (
    'Ответ API не является словарем: {response}'
)

API_MISSING_HOMEWORKS_KEY_ERROR_MSG = (
    'В ответе API отсутствует ключ "homeworks"'
)

API_HOMEWORKS_NOT_LIST_ERROR_MSG = (
    '"homeworks" не является списком. Тип: {type}'
)

API_HOMEWORK_NAME_MISSING_ERROR_MSG = (
    'В словаре homework отсутствует ключ "homework_name"'
)


HOMEWORK_STATUS_CHANGED_MSG = (
    'Изменился статус проверки работы "{name}". {verdict}'
)

MISSING_REQUIRED_ENV_VARS_ERROR_MSG = (
    'Отсутствуют обязательные переменные окружения'
)

NO_NEW_HOMEWORK_STATUSES_MSG = (
    'Нет новых статусов домашних работ'
)

PROGRAM_FAILURE_ERROR_MSG = (
    'Сбой в работе программы: {error}'
)

ERROR_MESSAGE_SEND_FAILURE_MSG = (
    'Не удалось отправить сообщение об ошибке: {send_error}'
)
