# Проектное задание
Бот создан для сихологической помощи людям в с импользованием ChatGPT. Проект выполнен в рамках научно-исследовательского семинара "Искусственный интеллект в инженерном образовании" МИЭМ НИУ ВШЭ.
Исполнители студенты группы БИВ234:
- Мирумян Артем
- Аброков Димир
- Куров Егор

# Блок-схема
[Посмотреть блок-схему](https://www.figma.com/board/d6VdhGlPXCT9jxdBODtsIE/doc?node-id=0-1&p=f&t=FgOdPUecHXOOEwgI-0)


# Как запустить
## Telegram bot
@AI_Psychologist78_bot

## Для разработчиков
Добавьте свою конфигурацию в .env файл
```
BOT_TOKEN=
OPENAI_API_KEY=
DATABASE_URL=postgresql+asyncpg://postgres:password@URL/db_name
```
password - пароль от баззы данных
URL - ссылка на баззу данных (например localhost:5432)
db_name - имя базы данных

