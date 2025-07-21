from pydantic import AnyUrl, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    @computed_field
    @property
    def url(self) -> AnyUrl: ...


class PostgresSettings(DatabaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    @computed_field
    @property
    def url(self) -> AnyUrl:
        return AnyUrl.build(
            scheme='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )


class TelegramBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TELEGRAM_BOT_')

    token: str


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='REDIS_')

    ssl: bool = Field(default=False, exclude=True)
    host: str = Field(exclude=True, alias='REDIS_MASTER_HOST')
    port: int | None = Field(exclude=True)
    username: str | None = Field(default=None, exclude=True)
    password: str | None = Field(default=None, exclude=True)

    @computed_field
    @property
    def url(self) -> AnyUrl:
        return AnyUrl.build(
            scheme='rediss' if self.ssl else 'redis',
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            path='3',
        )


class Settings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=PostgresSettings)  # type: ignore reportArgumentType
    telegram_bot: TelegramBotSettings = Field(
        default_factory=TelegramBotSettings  # type: ignore reportArgumentType
    )
    redis: RedisSettings = Field(default_factory=RedisSettings)  # type: ignore reportArgumentType
    root_path: str = ''


settings = Settings()  # type: ignore[reportCallIssue]
