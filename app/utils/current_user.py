from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer

from app import auth_settings
from app.model.auth import TokenData
from app.model.user import UserView, User

from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login", auto_error=False)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could nor validate credentials",
        headers={"Authentication": "Bearer"}
    )
    try:
        payload = jwt.decode(token, auth_settings.jwt_secret, algorithms=[auth_settings.jwt_algoritm])
        print(payload)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = await TokenData.find_one({TokenData.email:email})
        user = await User.find_one(User.email==token_data.email)
        
    except JWTError as e:
        raise credentials_exception
    return user  
    

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


async def get_current_superuser(current_user: User = Depends(get_current_active_user)):
    if current_user.is_superuser is False:
        print("====================== not superuser")
        raise HTTPException(status_code=400, detail="Not super user")
    return current_user