from dotenv import load_dotenv

load_dotenv()

# Токены и идентификаторы
REQUIRED_TOKENS = ('PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID')

# Возможные вердикты проверки
HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

# Сообщения об ошибках и логах
API_REQUEST_ERROR = (
    'Ошибка при запросе к API: {error}. '
    'Эндпоинт {endpoint} недоступен. '
    'Код ответа API: {status_code}, '
    'Текст ответа: {text}, '
    'URL запроса: {url}, '
    'Params: {params}'
)

MESSAGE_SEND_ERROR = (
    'Не удалось отправить сообщение в чат {chat_id}: {error}. '
    'Текст сообщения: {message}'
)

MESSAGE_SENT_LOG = (
    'Сообщение отправлено в чат {chat_id}. '
    'Текст сообщения: {message}'
)

MISSING_ENV_VAR = (
    'Отсутствует обязательная переменная окружения: {name}'
)

UNKNOWN_STATUS = (
    'Неизвестный статус работы: {status}'
)

ENDPOINT_UNAVAILABLE_ERROR = (
    'Эндпоинт {endpoint} недоступен. '
    'Код ответа API: {status_code}, '
    'Текст ответа: {text}, '
    'URL запроса: {url}'
)

API_RESPONSE_ERROR = (
    'Ошибка в ответе API: {data}. '
    'Эндпоинт: {endpoint}, '
    'Params: {params}'
)

API_RESPONSE_NOT_DICT_ERROR = (
    'Ответ API не является словарем. '
    'Получено: {actual_type}'
)

API_MISSING_HOMEWORKS_KEY_ERROR = (
    'В ответе API отсутствует ключ "homeworks"'
)

API_HOMEWORKS_NOT_LIST_ERROR = (
    '"homeworks" не является списком. '
    'Получено: {actual_type}'
)

API_HOMEWORK_NAME_MISSING_ERROR = (
    'В словаре homework отсутствует ключ "homework_name"'
)


HOMEWORK_STATUS_CHANGED = (
    'Изменился статус проверки работы "{name}". {verdict}'
)


NO_NEW_HOMEWORK_STATUSES = (
    'Нет новых статусов домашних работ'
)

PROGRAM_FAILURE_ERROR = (
    'Сбой в работе программы: {error}'
)

ERROR_MESSAGE_SEND_FAILURE = (
    'Не удалось отправить сообщение об ошибке: {send_error}'
)
