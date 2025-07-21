from aiogram import Router
from aiogram.filters import CommandStart

from bot.handlers.commands.start import StartCommandHandler

router = Router()
router.message.register(StartCommandHandler, CommandStart())
