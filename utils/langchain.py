from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from aiogram.types import Message
from config import OPENAI_API_KEY

# Инициализация OpenAI
llm = OpenAI(api_key=OPENAI_API_KEY)

# Промпт для определения настроения
mood_prompt = PromptTemplate(
    input_variables=["text"],
    template="Определи настроение в тексте: {text}. Варианты: радость, грусть, тревога, злость, нейтральное."
)

# Промпт для генерации поддерживающего ответа
support_prompt = PromptTemplate(
    input_variables=["mood", "message"],
    template="Пользователь чувствует {mood}. Напиши поддерживающий ответ на его сообщение: {message}."
)

# Цепочки для обработки запросов
mood_chain = mood_prompt | llm
support_chain = support_prompt | llm


async def chat_with_gpt(message: str) -> str:
    response = await llm.ainvoke(message)
    return response


async def detect_mood(message: Message) -> str:
    try:
        result = await mood_chain.ainvoke({"text": message.text})
        return result
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


async def generate_support_response(mood: str, message: Message) -> str:
    try:
        result = await support_chain.ainvoke({"mood": mood, "message": message.text})
        return result
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
