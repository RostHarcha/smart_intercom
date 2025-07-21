from db.models.users import User
from db.repositories.base import Repository


class UserRepository(Repository[User]):
    model_class = User

    async def get_or_create(self, user: User) -> User:
        instance = await self.get_by_id(user.id)
        if instance is None:
            instance = await self.create(user)
        return instance
