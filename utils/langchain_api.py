from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from aiogram.types import Message
from utils.handle_error import handle_openai_errors
from utils.database import async_session, get_user
from config import OPENAI_API_KEY

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


users_dialogs = dict()


# Функция для получения истории диалога пользователя
def get_session_history(user_id: str) -> ChatMessageHistory:
    if user_id not in users_dialogs:
        users_dialogs[user_id] = ChatMessageHistory()  # Создаем новую историю для пользователя
    return users_dialogs[user_id]


@handle_openai_errors
async def chat_with_gpt(message: Message) -> str:
    async with async_session() as session:
        user = await get_user(session, message)

        history = get_session_history(str(user.user_id))

        prompt_template = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="history"),
            ("user", "{input}"),
        ])

        # Создаем цепочку с шаблоном и моделью
        chain = prompt_template | llm

        conversation = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        wrapped_message = (
            f"Ты — профессиональный психолог. Твой клиент по имени {user.name} написал тебе следующее сообщение: {message.text}.\n"
            "Ответь на него как психолог, исключительно с этой точки зрения. "
            "Также не надо каждый раз представляться, следи за контекстом, если сможешь, и пиши как настоящий психолог, также ты можешь задавать вопросы."
        )

        # Передаем контекст в модель
        response = await conversation.ainvoke(
            {"input": wrapped_message, "history": history.messages},
            config={"configurable": {"session_id": str(user.user_id)}}
        )

        # Добавляем сообщение пользователя и ответ модели в историю
        history.add_user_message(message.text)
        history.add_ai_message(response)

        return response


@handle_openai_errors
async def detect_mood(message: Message) -> str:
    result = await mood_chain.ainvoke({"text": message.text})
    return result


@handle_openai_errors
async def generate_support_response(mood: str, message: Message) -> str:
    result = await support_chain.ainvoke({"mood": mood, "message": message.text})
    return result
