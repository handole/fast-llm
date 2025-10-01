from datetime import timedelta
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from beanie import Document

class AccessToken(BaseModel):
    """Access token details"""

    access_token: str
    access_token_expires: timedelta = timedelta(minutes=15)


class RefreshToken(AccessToken):    
    """Access and refresh token details"""

    refresh_token: str
    refresh_token_expires: timedelta = timedelta(days=30)


class TokenData(Document):
    email: Optional[str] = None
    token: Optional[RefreshToken]
    created_on: Optional[datetime] = datetime.now()
    
    class Settings:
        name = "token_data"