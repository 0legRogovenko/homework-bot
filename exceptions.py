class HomeworkBotError(Exception):
    """Базовое исключение для бота."""


class SendMessageError(HomeworkBotError):
    """Ошибка отправки сообщения в Telegram."""


class APIRequestError(HomeworkBotError):
    """Ошибка при запросе к API."""


class EndpointError(HomeworkBotError):
    """Эндпоинт недоступен."""
