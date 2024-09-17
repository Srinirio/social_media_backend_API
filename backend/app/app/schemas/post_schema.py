from pydantic import BaseModel
from fastapi import UploadFile
from datetime import datetime


class PostImageSchema(BaseModel):
    image_path: str

    class Config:
        orm_mode = True

class LikeSchema(BaseModel):
    post_id: int
    profile_username: str  

    class Config:
        orm_mode = True

class CommentSchema(BaseModel):
    post_id: int
    profile_username: str  
    comment: str

    class Config:
        orm_mode = True

class ShowAllPostDetail(BaseModel):
    post_id: int
    description: str
    created_at: datetime
    profile_id: int
    profile_name: str
    profile_image: str
    images: list[PostImageSchema]
    like_count: int
    comment_count: int
    likes: list[LikeSchema]
    comments: list[CommentSchema]

    class Config:
        orm_mode = True


class PostDetail(BaseModel):
    post_id: int
    description: str
    images: list[str]
    created_at: datetime
    
class UpdatePostSchema(BaseModel):
    description: str | None = None
    images: list[str] | None = None

