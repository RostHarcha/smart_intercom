from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session

DBSessionDep = Annotated[AsyncSession, Depends(get_session)]
