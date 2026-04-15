class AppError(Exception):
    """Базовая доменная ошибка приложения."""


class ConflictError(AppError):
    """Конфликт состояния (например, email уже существует)."""


class UnauthorizedError(AppError):
    """Неавторизован (неверные учётные данные/токен)."""


class ForbiddenError(AppError):
    """Запрещено (нет прав)."""


class NotFoundError(AppError):
    """Не найдено (объект отсутствует)."""


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса (например, OpenRouter)."""
