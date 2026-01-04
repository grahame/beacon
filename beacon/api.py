from fastapi import APIRouter, Depends

from .db import User
from .settings import settings
from .users import (
    auth_backend,
    current_active_user,
    fastapi_users,
    theolau_oauth_client,
)

api = APIRouter(prefix="/api/v1")

api.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
api.include_router(
    fastapi_users.get_oauth_router(
        theolau_oauth_client,
        auth_backend,
        settings.token_secret,
        redirect_url="https://{}/oauth-callback".format(settings.base_domain),
    ),
    prefix="/auth/theolau",
    tags=["auth"],
)


@api.get("/me")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
