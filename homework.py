import logging
import os
import time

import requests
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import (
    SendMessageError,
    APIRequestError,
    EndpointError,
    StatusError,
    HomeworkNameError,
    UnknownStatusError,
    HomeworkError,
    HomeworkBotError
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = (
    'https://practicum.yandex.ru/api/user_api/homework_statuses'
)
HEADERS = {
    'Authorization': f'OAuth {PRACTICUM_TOKEN}',
}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("program.log", mode="w"),
        logging.StreamHandler(),
    ]
)


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
    }
    for name, value in tokens.items():
        if not value:
            logging.critical(
                f'Отсутствует обязательная переменная окружения: '
                f'{name}'
            )
            return False
    return True


def send_message(bot, message):
    """Отправляет сообщение в Telegram-чат."""
    chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))
    if chat_id is None:
        logging.error('TELEGRAM_CHAT_ID не установлен')
        raise ValueError('TELEGRAM_CHAT_ID не установлен')
    if not isinstance(message, str):
        logging.error('Сообщение должно быть строкой')
        raise TypeError('Сообщение должно быть строкой')
    try:
        bot.send_message(chat_id, message)
        logging.debug(
            f'Сообщение отправлено в чат {chat_id}'
        )
    except Exception as error:
        logging.error(
            f'Не удалось отправить сообщение в чат {chat_id}: '
            f'{error}'
        )
        raise SendMessageError(
            f'Не удалось отправить сообщение в чат {chat_id}: '
            f'{error}'
        )


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    try:
        response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params={'from_date': timestamp}
        )
    except requests.RequestException as error:
        logging.error(
            f'Ошибка при запросе к API: {error}'
        )
        raise APIRequestError(f'Ошибка при запросе к API: {error}')

    if response.status_code != 200:
        logging.error(
            f'Эндпоинт {ENDPOINT} недоступен. '
            f'Код ответа API: {response.status_code}, '
            f'Текст ответа: {response.text}, '
            f'URL запроса: {response.url}'
        )
        raise EndpointError(
            f'Эндпоинт {ENDPOINT} недоступен. '
            f'Код ответа API: {response.status_code}'
        )
    return response.json()


def check_response(response):
    """Проверяет ответ API на соответствие документации.

    Документация: урок «API сервиса Практикум Домашка».
    """
    if not isinstance(response, dict):
        logging.error('Ответ API не является словарем')
        raise TypeError('Ответ API не является словарем')

    if not isinstance(response.get('homeworks'), list):
        logging.error(
            '"homeworks" отсутствует или не является списком'
        )
        raise TypeError(
            '"homeworks" отсутствует или не является списком'
        )

    if not isinstance(response.get('current_date'), int):
        logging.error(
            '"current_date" отсутствует или не является числом'
        )
        raise TypeError(
            '"current_date" отсутствует или не является числом'
        )

    for homework in response['homeworks']:
        if not isinstance(homework, dict):
            logging.error(
                'Элемент списка homeworks не является словарем'
            )
            raise HomeworkError(
                'Элемент списка homeworks не является словарем'
            )

        if not isinstance(homework.get('homework_name'), str):
            logging.error(
                'Отсутствует ключ homework_name или он не строка'
            )
            raise HomeworkNameError(
                'Отсутствует ключ homework_name или он не строка'
            )

        if not isinstance(homework.get('status'), str):
            logging.error(
                'Отсутствует ключ status или он не строка'
            )
            raise StatusError(
                'Отсутствует ключ status или он не строка'
            )

    return response['homeworks']


def parse_status(homework):
    """Извлекает статус конкретной домашней работы.

    Аргумент homework — словарь с информацией о работе.
    """
    if not isinstance(homework, dict):
        logging.error('Аргумент homework не является словарем')
        raise TypeError('Аргумент homework не является словарем')

    if 'homework_name' not in homework:
        logging.error(
            'В словаре homework отсутствует ключи "homework_name"'
        )
        raise HomeworkNameError(
            'В словаре homework отсутствует ключи "homework_name"'
        )

    if 'status' not in homework:
        logging.error(
            'В словаре homework отсутствует ключи "status"'
        )
        raise StatusError(
            'В словаре homework отсутствует ключи "status"'
        )

    homework_name = homework['homework_name']
    verdict = homework['status']

    if verdict not in HOMEWORK_VERDICTS:
        logging.error(
            f'Неизвестный статус работы: {verdict}'
        )
        raise UnknownStatusError(f'Неизвестный статус работы: {verdict}')

    return (
        f'Изменился статус проверки работы "{homework_name}". '
        f'{HOMEWORK_VERDICTS[verdict]}'
    )


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        raise SystemExit('Отсутствуют обязательные переменные окружения')
    else:
        logging.debug('Нет новых статусов домашних работ')

    bot = TeleBot(TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)

            if homeworks:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            else:
                logging.debug('Нет новых статусов домашних работ')

            timestamp = response.get('current_date', timestamp)

        except HomeworkBotError as error:
            logging.error(f'Сбой в работе программы: {error}')
            try:
                send_message(bot, f'Сбой в работе программы: {error}')
            except SendMessageError as send_error:
                logging.error(
                    f'Не удалось отправить сообщение об ошибке: {send_error}')

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
