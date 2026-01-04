from collections import defaultdict
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import JSON, ForeignKey, Index, String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from .settings import settings


class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    access_token: Mapped[str] = mapped_column(String(length=4096), nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    name: Mapped[str | None] = mapped_column(String(length=255), nullable=True)
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


class Parish(Base):
    __tablename__ = "parish"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    geojson: Mapped[dict] = mapped_column(JSON, nullable=False)


class ParishSubscription(Base):
    __tablename__ = "parish_subscription"
    __table__args__ = Index("ix_unique_mapping", "user_id", "parish_id", unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parish_id: Mapped[int] = mapped_column(
        ForeignKey("parish.id", ondelete="CASCADE"), nullable=False
    )


engine = settings.create_sync_engine()
async_engine = settings.create_async_engine()
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)


def get_parish_subscriptions():
    session = Session(engine)
    stmt = (
        select(Parish.name, User.email)
        .join(ParishSubscription, ParishSubscription.parish_id == Parish.id)
        .join(User, User.id == ParishSubscription.user_id)
    )
    subs = defaultdict(list)
    for parish, email in session.execute(stmt):
        subs[parish].append(email)
    return subs
