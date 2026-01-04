from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .db import Parish, ParishSubscription, User, get_async_session
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


@api.get("/users/me")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {
        "email": user.email,
        "name": user.name,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
    }


@api.get("/subscriptions")
async def get_subscriptions(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    # Get all parishes
    parishes_result = await session.execute(select(Parish).order_by(Parish.name))
    parishes = parishes_result.scalars().all()

    # Get user's subscribed parish IDs
    subs_result = await session.execute(
        select(ParishSubscription.parish_id).where(
            ParishSubscription.user_id == user.id
        )
    )
    subscribed_ids = {row[0] for row in subs_result}

    return [
        {"parish": parish.name, "subscribed": parish.id in subscribed_ids}
        for parish in parishes
    ]


class SetSubscriptionRequest(BaseModel):
    parish_id: int


@api.post("/subscription")
async def set_subscription(
    request: SetSubscriptionRequest,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    subscription = ParishSubscription(user_id=user.id, parish_id=request.parish_id)
    session.add(subscription)
    await session.commit()
    return {"status": "subscribed"}


@api.delete("/subscription")
async def delete_subscription(
    request: SetSubscriptionRequest,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
):
    await session.execute(
        delete(ParishSubscription).where(
            ParishSubscription.user_id == user.id,
            ParishSubscription.parish_id == request.parish_id,
        )
    )
    await session.commit()
    return {"status": "unsubscribed"}
