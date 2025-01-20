from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from aiogram.types import Message
from utils.handle_error import handle_openai_errors
from utils.database import get_user_context, async_session
from utils.actions_json import ActionsJSON
from config import OPENAI_API_KEY
from utils.database import get_user, async_session

# Инициализация OpenAI
llm = OpenAI(api_key=OPENAI_API_KEY, max_tokens=3000)

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


@handle_openai_errors
async def chat_with_gpt(message: Message) -> str:
    user_context_json = await get_user_context(async_session(), message)
    messages_array = ActionsJSON.from_json(user_context_json.context_data).get_messages()

    # Формируем контекст из истории сообщений
    context = "\n".join(messages_array[-5:])  # Используем последние 5 сообщений

     # Получаем данные пользователя
    user = await get_user(async_session(), message)

    # Проверяем, найден ли пользователь, и извлекаем имя
    user_name = user.name if user and user.name else "Пользователь"

    wrapped_message = (
        f"Ты — психолог. Тебя зовут Зигмунд Фрейд. Твой клиент по имени {user.name} написал тебе следующее сообщение: {message.text}.\n"
        "Ответь на него как психолог, исключительно с этой точки зрения. "
        f"до этого вопроса вы немного пообщались. "
        "Также не надо каждый раз представляться, попробуй следить за контекстом, если сможешь, и пиши как настоящий психолог, также ты можешь задавать вопросы."
    )

    # Передаем контекст в модель
    response = await llm.ainvoke(wrapped_message)
    return response


@handle_openai_errors
async def detect_mood(message: Message) -> str:
    result = await mood_chain.ainvoke({"text": message.text})
    return result


@handle_openai_errors
async def generate_support_response(mood: str, message: Message) -> str:
    result = await support_chain.ainvoke({"mood": mood, "message": message.text})
    return result
