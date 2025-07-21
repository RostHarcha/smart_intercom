from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage

from bot.handlers import router
from config import settings

bot = Bot(
    token=settings.telegram_bot.token,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML,
        link_preview_is_disabled=True,
    ),
)

dp = Dispatcher(
    storage=RedisStorage.from_url(
        url=str(settings.redis.url),
        key_builder=DefaultKeyBuilder(
            with_destiny=True,
        ),
    ),
)

dp.include_router(router)
