import logging
import os
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import (
    APIRequestError,
    EndpointError,
    SendMessageError,
)

from constants import (
    API_HOMEWORK_NAME_MISSING_ERROR,
    API_HOMEWORKS_NOT_LIST_ERROR,
    API_MISSING_HOMEWORKS_KEY_ERROR,
    API_REQUEST_ERROR,
    API_RESPONSE_ERROR,
    API_RESPONSE_NOT_DICT_ERROR,
    ENDPOINT_UNAVAILABLE_ERROR,
    ERROR_MESSAGE_SEND_FAILURE,
    HOMEWORK_STATUS_CHANGED,
    HOMEWORK_VERDICTS,
    MESSAGE_SEND_ERROR,
    MESSAGE_SENT_LOG,
    MISSING_ENV_VAR,
    NO_NEW_HOMEWORK_STATUSES,
    PROGRAM_FAILURE_ERROR,
    REQUIRED_TOKENS,
    UNKNOWN_STATUS,
)


load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses'
HEADERS = {
    'Authorization': f'OAuth {PRACTICUM_TOKEN}',
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    missing = [name for name in REQUIRED_TOKENS if not globals().get(name)]
    if missing:
        logging.critical(
            MISSING_ENV_VAR + f'Отсутствуют: {", ".join(missing)}'
        )
        return False
    return True


def send_message(bot, message):
    """Отправляет сообщение в Telegram-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(MESSAGE_SENT_LOG.format(
            chat_id=TELEGRAM_CHAT_ID,
            message=message
        ))
    except Exception as error:
        logging.error(
            MESSAGE_SEND_ERROR.format(
                chat_id=TELEGRAM_CHAT_ID,
                error=error,
                message=message
            )
        )
        raise SendMessageError(
            MESSAGE_SEND_ERROR.format(
                chat_id=TELEGRAM_CHAT_ID,
                error=error,
                message=message
            )
        )


def get_api_answer(timestamp):
    """Делает запрос к эндпоинту API-сервиса."""
    rq_pars = dict(
        url=ENDPOINT,
        headers=HEADERS,
        params={'from_date': timestamp}
    )
    try:
        response = requests.get(
            **rq_pars
        )
    except requests.RequestException as error:
        raise ConnectionError(
            API_REQUEST_ERROR.format(
                error=error,
                **rq_pars
            )
        )

    if response.status_code != HTTPStatus.OK:
        raise EndpointError(
            ENDPOINT_UNAVAILABLE_ERROR.format(
                endpoint=ENDPOINT,
                status_code=response.status_code,
                **rq_pars
            )
        )
    data = response.json()

    for key in ('code', 'error'):
        if key in data:
            raise APIRequestError(
                API_RESPONSE_ERROR.format(
                    key=key,
                    value=data[key],
                    **rq_pars
                )
            )

    return data


def check_response(response):
    """Проверяет ответ API на соответствие документации.

    Документация: урок «API сервиса Практикум Домашка».
    """
    if not isinstance(response, dict):
        error_msg = (
            f'{API_RESPONSE_NOT_DICT_ERROR}'
            f'Получено: {type(response)} - {repr(response)}'
        )
        raise TypeError(error_msg)

    if 'homeworks' not in response:
        raise KeyError(API_MISSING_HOMEWORKS_KEY_ERROR)

    homeworks = response['homeworks']

    if not isinstance(homeworks, list):
        error_msg = (
            f'{API_HOMEWORKS_NOT_LIST_ERROR}'
            f'Получено: {type(homeworks)} - {repr(homeworks)}'
        )
        raise TypeError(error_msg)

    return homeworks


def parse_status(homework):
    """Извлекает статус конкретной домашней работы.

    Аргумент homework — словарь с информацией о работе.
    """
    if 'homework_name' not in homework:
        raise KeyError(
            API_HOMEWORK_NAME_MISSING_ERROR
        )

    status = homework['status']

    if status not in HOMEWORK_VERDICTS:
        raise ValueError(UNKNOWN_STATUS.format(status=status))

    return (
        HOMEWORK_STATUS_CHANGED.format(
            name=homework['homework_name'],
            verdict=HOMEWORK_VERDICTS[status])
    )


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        return

    logging.debug(NO_NEW_HOMEWORK_STATUSES)

    bot = TeleBot(TELEGRAM_TOKEN)
    timestamp = int(time.time())
    last_error_message = None

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)

            if homeworks:
                send_message(bot, parse_status(homeworks[0]))
                timestamp = response.get('current_date', timestamp)
            else:
                logging.debug(NO_NEW_HOMEWORK_STATUSES)

        except Exception as error:
            error_message = PROGRAM_FAILURE_ERROR.format(error=error)
            logging.error(error_message)

            if error_message != last_error_message:
                try:
                    send_message(bot, error_message)
                    last_error_message = error_message
                except SendMessageError as send_error:
                    logging.error(
                        ERROR_MESSAGE_SEND_FAILURE.format(
                            send_error=send_error)
                    )

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(lineno)d - '
               '%(funcName)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(f'{__file__}.log', mode='w'),
            logging.StreamHandler()
        ]
    )
    main()
