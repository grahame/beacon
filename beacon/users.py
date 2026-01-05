import uuid
from typing import Optional

from .settings import settings
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from httpx_oauth.clients.openid import OpenID

from .db import User, get_user_db

theolau_oauth_client = OpenID(
    settings.theolau_oauth_client_id,
    settings.theolau_oauth_client_secret,
    "https://auth.theol.au/application/o/beacon/.well-known/openid-configuration",
    "theolau",
    base_scopes=["openid", "email", "profile"],
)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    # reset_password_token_secret = settings.token_secret
    verification_token_secret = settings.token_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def oauth_callback(
        self,
        oauth_name: str,
        access_token: str,
        account_id: str,
        account_email: str,
        expires_at: Optional[int] = None,
        refresh_token: Optional[str] = None,
        request: Optional[Request] = None,
        *,
        associate_by_email: bool = False,
        is_verified_by_default: bool = False,
    ) -> User:
        user = await super().oauth_callback(
            oauth_name,
            access_token,
            account_id,
            account_email,
            expires_at,
            refresh_token,
            request,
            associate_by_email=associate_by_email,
            is_verified_by_default=is_verified_by_default,
        )

        # Always update the user's name from OAuth provider
        info = await theolau_oauth_client.get_profile(access_token)
        if info:
            if "name" in info:
                user.name = info["name"]
            if "email_verified" in info:
                user.is_verified = info["email_verified"]
            await self.user_db.update(user, {"name": user.name})

        return user


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:
    return JWTStrategy(secret=settings.token_secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
