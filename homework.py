import logging
import time

import requests
from dotenv import load_dotenv
from telebot import TeleBot

from exceptions import (
    SendMessageError,
    APIRequestError,
    EndpointError,
)

from constants import (
    PRACTICUM_TOKEN,
    TELEGRAM_TOKEN,
    TELEGRAM_CHAT_ID,
    REQUIRED_TOKENS,
    RETRY_PERIOD,
    ENDPOINT,
    HEADERS,
    HOMEWORK_VERDICTS,
    STATUS_OK,
    API_REQUEST_ERROR_MSG,
    MESSAGE_SEND_ERROR_MSG,
    MESSAGE_SENT_LOG_MSG,
    MISSING_ENV_VAR_MSG,
    UNKNOWN_STATUS_MSG,
    ENDPOINT_UNAVAILABLE_ERROR_MSG,
    API_RESPONSE_ERROR_MSG,
    API_RESPONSE_NOT_DICT_ERROR_MSG,
    API_MISSING_HOMEWORKS_KEY_ERROR_MSG,
    API_HOMEWORKS_NOT_LIST_ERROR_MSG,
    API_HOMEWORK_NAME_MISSING_ERROR_MSG,
    HOMEWORK_STATUS_CHANGED_MSG,
    MISSING_REQUIRED_ENV_VARS_ERROR_MSG,
    NO_NEW_HOMEWORK_STATUSES_MSG,
    PROGRAM_FAILURE_ERROR_MSG,
    ERROR_MESSAGE_SEND_FAILURE_MSG,
)


load_dotenv()


def check_tokens():
    """Проверяет доступность переменных окружения."""
    missing = []
    for name in REQUIRED_TOKENS:
        if not globals().get(name):
            logging.critical(MISSING_ENV_VAR_MSG.format(name=name))
            missing.append(name)
    return not missing


def send_message(bot, message):
    """Отправляет сообщение в Telegram-чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.debug(MESSAGE_SENT_LOG_MSG.format(
            chat_id=TELEGRAM_CHAT_ID,
            message=message
        ))
    except Exception as error:
        logging.error(
            MESSAGE_SEND_ERROR_MSG.format(
                chat_id=TELEGRAM_CHAT_ID,
                error=error,
                message=message
            )
        )
        raise SendMessageError(
            MESSAGE_SEND_ERROR_MSG.format(
                chat_id=TELEGRAM_CHAT_ID,
                error=error,
                message=message
            )
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
        error_response = error.response
        raise RuntimeError(
            API_REQUEST_ERROR_MSG.format(
                error=error_response
            )
        )

    if response.status_code != STATUS_OK:
        raise EndpointError(
            ENDPOINT_UNAVAILABLE_ERROR_MSG.format(
                endpoint=ENDPOINT,
                status_code=response.status_code,
                text=response.text,
                url=response.url,
            )
        )
    data = response.json()

    if 'code' in data or 'error' in data:
        raise APIRequestError(
            API_RESPONSE_ERROR_MSG
        )

    return data


def check_response(response):
    """Проверяет ответ API на соответствие документации.

    Документация: урок «API сервиса Практикум Домашка».
    """
    if not isinstance(response, dict):
        raise TypeError(
            API_RESPONSE_NOT_DICT_ERROR_MSG
        )

    if 'homeworks' not in response:
        raise KeyError(
            API_MISSING_HOMEWORKS_KEY_ERROR_MSG
        )

    if not isinstance(response.get('homeworks'), list):
        raise TypeError(
            API_HOMEWORKS_NOT_LIST_ERROR_MSG
        )

    return response['homeworks']


def parse_status(homework):
    """Извлекает статус конкретной домашней работы.

    Аргумент homework — словарь с информацией о работе.
    """
    if 'homework_name' not in homework:
        raise KeyError(
            API_HOMEWORK_NAME_MISSING_ERROR_MSG
        )

    name = homework['homework_name']
    status = homework['status']

    if status not in HOMEWORK_VERDICTS:
        raise ValueError(UNKNOWN_STATUS_MSG.format(status=status))

    return (
        HOMEWORK_STATUS_CHANGED_MSG.format(
            name=name,
            verdict=HOMEWORK_VERDICTS[status])
    )


def main():
    """Основная логика работы бота."""
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(lineno)d - '
               '%(funcName)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(__file__ + '.log', mode='w'),
        ]
    )

    if not check_tokens():
        logging.critical(MISSING_REQUIRED_ENV_VARS_ERROR_MSG)
        return

    logging.debug(NO_NEW_HOMEWORK_STATUSES_MSG)

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
                logging.debug(NO_NEW_HOMEWORK_STATUSES_MSG)

        except Exception as error:
            error_message = PROGRAM_FAILURE_ERROR_MSG.format(error=error)
            logging.error(error_message)

            if error_message != last_error_message:
                try:
                    send_message(bot, error_message)
                    last_error_message = error_message
                except SendMessageError as send_error:
                    logging.error(
                        ERROR_MESSAGE_SEND_FAILURE_MSG.format(
                            send_error=send_error)
                    )

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
