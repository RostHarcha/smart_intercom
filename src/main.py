import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

import bot.dispatcher
from config import settings

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    await bot.dispatcher.dp.start_polling(bot.dispatcher.bot)
    yield
    await bot.dispatcher.dp.stop_polling()


app = FastAPI(root_path=settings.root_path, lifespan=lifespan)
