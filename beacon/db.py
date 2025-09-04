from collections import defaultdict
from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import ForeignKey, Index, String, create_engine, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from .settings import settings


class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    access_token: Mapped[str] = mapped_column(String(length=4096), nullable=False)


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )


class ParishSubscription(Base):
    __tablename__ = "parish_subscription"
    __table__args__ = Index("ix_unique_mapping", "user_id", "parish", unique=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    parish: Mapped[str] = mapped_column(String(length=4096), nullable=False)


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
    stmt = select(ParishSubscription.parish, User.email).join(User)
    subs = defaultdict(list)
    for parish, email in session.execute(stmt):
        subs[parish].append(email)
    return subs
