from pydantic import BaseModel, EmailStr
from datetime import datetime

# Schema/pydantic model in totally differnt than the models as models is use to create the structure of our postgres table whereas Schema is used to define the structure of the request and response data.

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class CreatePost(PostBase):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True  # even without it things are working fine

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None
    email: EmailStr