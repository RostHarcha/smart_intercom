from db.models.users import User
from db.repositories.base import Repository


class UserRepository(Repository[User]):
    model_class = User
