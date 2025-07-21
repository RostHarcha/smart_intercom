from pydantic import AnyUrl, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int

    @computed_field
    def url(self) -> AnyUrl: ...


class PostgresSettings(DatabaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    @computed_field
    def url(self) -> AnyUrl:
        return AnyUrl.build(
            scheme='postgresql+asyncpg',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.db,
        )


class Settings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=PostgresSettings)  # type: ignore reportArgumentType
    root_path: str = ''


settings = Settings()  # type: ignore[reportCallIssue]
