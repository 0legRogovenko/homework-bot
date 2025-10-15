class HomeworkBotError(Exception):
    """Базовое исключение для бота."""

    pass


class SendMessageError(HomeworkBotError):
    """Ошибка отправки сообщения в Telegram."""

    pass


class APIRequestError(HomeworkBotError):
    """Ошибка при запросе к API."""

    pass


class EndpointError(HomeworkBotError):
    """Эндпоинт недоступен."""

    pass


class StatusError(HomeworkBotError):
    """Недокументированный статус домашней работы."""

    pass


class HomeworkNameError(HomeworkBotError):
    """Ошибка отсутствия ключа 'homework_name' в ответе API."""

    pass


class UnknownStatusError(HomeworkBotError):
    """Неизвестный статус домашней работы."""

    pass


class HomeworkError(HomeworkBotError):
    """Общая ошибка домашней работы."""

    pass
