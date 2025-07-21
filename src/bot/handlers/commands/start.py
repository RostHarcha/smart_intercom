from typing import override

from aiogram.handlers import MessageHandler, MessageHandlerCommandMixin

from db import get_session_cm
from db.models import User
from db.repositories import UserRepository


class StartCommandHandler(MessageHandlerCommandMixin, MessageHandler):
    @override
    async def handle(self):
        assert self.from_user
        async with get_session_cm() as session:
            users = UserRepository(session)
            user = await users.get_or_create(
                User(
                    id=self.from_user.id,
                    first_name=self.from_user.first_name,
                    username=self.from_user.username,
                )
            )
        await self.event.answer(f'Привет, {user.first_name}!')
