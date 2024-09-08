import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    username: str
    email: EmailStr
    created_at: datetime.datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostIn(Post):
    pass

class PostOut(Post):
    id: int
    created_at: datetime.datetime
    user_id: int

    user_details: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None