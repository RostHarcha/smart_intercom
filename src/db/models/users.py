from sqlalchemy import BigInteger
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int = Field(
        sa_type=BigInteger,
        primary_key=True,
        unique=True,
    )
    first_name: str
    username: str | None = Field(
        default=None,
        nullable=True,
    )
