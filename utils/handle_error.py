from functools import wraps
from typing import Callable, Coroutine, Any
from aiogram.types import Message


def handle_openai_errors(func: Callable[..., Coroutine[Any, Any, str]]) -> Callable[..., Coroutine[Any, Any, str]]:
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs) -> str:
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            print(f"Error occurred while detecting mood: {e}")

            if "unsupported_country_region_territory" in str(e):
                await message.answer("Доступ к OpenAI ограничен в вашем регионе. Попробуйте использовать VPN (Казахский).")
                raise PermissionError(
                    "Доступ к OpenAI ограничен в вашем регионе. Попробуйте использовать VPN (Казахский)."
                ) from e
            elif "invalid_request_error" in str(e):
                raise ValueError("Некорректный запрос к OpenAI API.") from e
            elif "rate_limit_exceeded" in str(e):
                raise RuntimeError("Превышен лимит запросов к OpenAI API. Попробуйте позже.") from e
            else:
                raise RuntimeError(f"Неизвестная ошибка: {str(e)}") from e

    return wrapper
