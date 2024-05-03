from aiogram.types import BotCommand
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    timezone: str = 'Asia/Yekaterinburg'

    db_dialect: str = 'postgresql+asyncpg'
    db_username: str = 'postgres'
    db_password: str = '123'
    db_host: str = 'localhost'
    db_port: str = '5432'
    db_database: str = 'TelegramBotCore'
    test_database: str = 'TestDatabase'

    bot_token: str = '6725907075:AAHslUsu8WEbr74XfCZaNpbSkaKhGco_is4'
    telegram_api_base: str = 'https://api.telegram.org/bot'
    telegram_api_url: str = f'{telegram_api_base}{bot_token}'

    bot_commands: list[BotCommand] = [
        BotCommand(command="start", description="Начало работы"),
        BotCommand(command="menu", description="Главное меню"),
    ]

    api_error_message: str = 'Произошла ошибка обработки запроса к API. Попробуйте повторить запрос позже.'
    need_authorize_message: str = 'Необходимо повторно авторизоваться в боте. Используйте команду /start'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
