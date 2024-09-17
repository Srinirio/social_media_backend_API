from pydantic import BaseModel, EmailStr,Field
from datetime import datetime



class RegistrationCreate(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    
 
class ResetPasswordIn(BaseModel):
    secret_key: str
    otp: int
    new_password: str
    
class Message(BaseModel):
    message: str

class RegistrationOut(Message):
    secret_key: str
    otp: int