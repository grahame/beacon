import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pg_dsn: PostgresDsn = "postgres+psycopg2://user:pass@localhost:5432/beacon"
    pg_async_dsn: PostgresDsn = "postgres+asyncpg://user:pass@localhost:5432/beacon"
    token_secret: str
    redis_location: str = "redis://localhost:6379/2"
    base_url: str
    theolau_oauth_client_id: str
    theolau_oauth_client_secret: str

    def create_sync_engine(self, **kwargs):
        return sqlalchemy.create_engine(
            str(self.pg_dsn),
            future=True,
            **kwargs,
        )

    def create_async_engine(self, **kwargs):
        return create_async_engine(
            str(self.pg_async_dsn),
            future=True,
            **kwargs,
        )


settings = Settings()
