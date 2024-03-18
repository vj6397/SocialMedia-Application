from datetime import datetime
from pydantic import BaseModel,EmailStr, conint, validator
from typing import Optional



class user(BaseModel):
    email: EmailStr
    password: str

class user_out(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True


class login(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None


class Post(BaseModel):
    title:str
    content:str
    published:bool=True

class create_post(Post):
    pass

class post_response(Post):
    id: int
    created_at: datetime
    owner_id:int
    owner:user_out

    class Config:
        orm_mode = True

class post_out(BaseModel):
    Post:post_response
    votes:int

    class Config:
        orm_mode = True



class Vote(BaseModel):
    post_id:int
    dir: int



