from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
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

async def detect_mood(text: str) -> str:
    result = await mood_chain.ainvoke({"text": text})
    return result

async def generate_support_response(mood: str, message: str) -> str:
    result = await support_chain.ainvoke({"mood": mood, "message": message})
    return result