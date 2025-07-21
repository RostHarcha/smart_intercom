from typing import Generic, TypeVar, cast

from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

Model = TypeVar('Model', bound=SQLModel)


class Repository(Generic[Model]):
    model_class: type[Model]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id) -> Model | None:
        return await self.session.get(self.model_class, id)

    async def create(self, instance: Model) -> Model:
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def all(self) -> list[Model]:
        result = await self.session.exec(select(self.model_class))
        return cast(list, result.all())

    async def delete(self, id: int) -> None:
        instance = await self.get_by_id(id)
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
