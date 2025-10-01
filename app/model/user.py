from datetime import datetime
from typing import Optional

from beanie import Document
from beanie import PydanticObjectId
from beanie import Indexed
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pymongo import IndexModel
from pymongo.collation import Collation


class BaseUserCreate(BaseModel):
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    def create_update_dict(self):
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    def create_update_dict_superuser(self):
        return self.dict(exclude_unset=True, exclude={"id"})


class User(Document, BaseUserCreate):
    full_name: Optional[str]
    email: Optional[EmailStr]
    hashed_password: Optional[str]
    phone_number: Optional[str]
    created_on: Optional[datetime] = datetime.now()
    updated_on: Optional[datetime] = datetime.now()

    class Settings:
        name = "users"
        email_collation = Collation("en", strength=2)
        indexes = [
            IndexModel("email", unique=True),
            IndexModel(
                "email", name="case_insensitive_email_index", collation=email_collation
            )
        ]

    class Config:
        schema_extra = {
            "example": {
                "full_name": "test user full",
                "email": "testuser@mail.com",
                "hashed_password": "test123",
                "phone_number": "08111321"
            }
        }
        orm_mode = True


class UserCreate(BaseUserCreate):
    full_name: Optional[str]
    email: EmailStr
    hashed_password: str
    phone_number: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "full_name": "test user full",
                "email": "testuser@mail.com",
                "hashed_password": "test123",
                "phone_number": "08111321"
            }
        }


class UserView(BaseModel):
    full_name: Optional[str]
    email: EmailStr
    hashed_password: str
    phone_number: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str


class ForgotPassword(BaseModel):
    email: EmailStr = Field(...)
    

class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str

    class Config:
        schema_extra = {"example": {"new_password": "asd", "confirm_password": "asd"}}

    # @validator("confirm_passwowrd")
    # def passwords_matching(cls, v, values, **kwargs):
    #     if "new_password" in values and v != values["new_password"]:
    #         raise ValueError("passwords do not match!")
    #     return v


class ResetCodePassword(Document):
    user_id: Optional[Indexed(PydanticObjectId)]
    reset_code: str
    status: Optional[bool] = True
    expired_in: Optional[datetime]

    class Collection:
        name = "reset_code_password"