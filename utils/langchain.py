from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from aiogram.types import Message
from utils.handle_error import handle_openai_errors
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


@handle_openai_errors
async def chat_with_gpt(message: Message) -> str:
    response = await llm.ainvoke(message.text)
    return response


@handle_openai_errors
async def detect_mood(message: Message) -> str:
    result = await mood_chain.ainvoke({"text": message.text})
    return result


@handle_openai_errors
async def generate_support_response(mood: str, message: Message) -> str:
    result = await support_chain.ainvoke({"mood": mood, "message": message.text})
    return result
