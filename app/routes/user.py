import logging
from typing import List
from fastapi import APIRouter
from fastapi import Depends

from app import app_settings
from app.model.user import User
from app.model.user import UserView
from app.utils.current_user import get_current_superuser, get_current_active_user


router = APIRouter(prefix=f"{app_settings.api_prefix}/users", tags=["Users"])
logger = logging.getLogger("users")


@router.get("", response_model=List[UserView])
async def users(user: User = Depends(get_current_active_user)):
    return await User.find(fetch_links=True).to_list()


@router.get("/active")
async def active(user: User = Depends(get_current_active_user)):
    return user


@router.get("/admin")
async def active(user: User = Depends(get_current_superuser)):
    return user