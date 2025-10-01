import logging
from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from app import app_settings
from app.model.user import UserCreate
from app.model.user import User
from app.model.auth import RefreshToken, TokenData
from app.utils.authentication import get_hashed_password
from app.utils.authentication import verify_password
from app.utils.authentication import create_access_token, create_refresh_token
from app.utils import query as query_message


router = APIRouter(prefix=f"{app_settings.api_prefix}/users", tags=["Users"])
logger = logging.getLogger("users")


@router.post("/register", response_model=User)
async def register(data: UserCreate, request: Request):
    user = await User.find_one({User.email: data.email})
    if user is not None:
        logger.error(f"{query_message.REGISTER_USER_ALREADY_EXISTS}")
        raise HTTPException(409, "User with that email already exists")
    hashed = get_hashed_password(data.hashed_password)
    usr = User(
        full_name=data.full_name,
        email=data.email,
        hashed_password=hashed,
        phone_number=data.phone_number
    )
    await usr.create()
    return usr



@router.post("/login")
async def login(
    resp: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    user = await User.find_one(User.email == credentials.username)
    if user is None or verify_password(credentials.password, user.hashed_password) is False:
        logger.error("User or email hash been failed")
        raise HTTPException(status_code=401, detail="Bad email or password")

    if not user.is_verified:
        logger.error("User not verified, please verify your account...")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not verified"
        )

    access_token = create_access_token(subject=credentials.username)
    refresh_token = create_refresh_token(subject=credentials.username)

    td = TokenData(
        email=credentials.username,
        token=RefreshToken(access_token=access_token, refresh_token=refresh_token)
    )
    await td.save()
    return td                          