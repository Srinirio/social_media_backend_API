from pydantic import BaseModel
from fastapi import UploadFile

class ProfileOut(BaseModel):
    name: str
    id: int
    profile_name: str | None
    bio: str | None
    image: str | None
    is_private: bool
    
    
class ListOfProfile(BaseModel):
    list_of_profile: list[ProfileOut]
    
class ProfileResponse(BaseModel):
    id: int
    username: str
    profile_name: str | None
    profile_image: str | None
    bio: str | None
    is_private: bool

    class Config:
        orm_mode = True