from db.db import SessionLocal
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from typing import Annotated
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from core.config import settings
import jwt
from schemas.token import TokenPayload
from crud import crud_profile

#oauth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def getCurrentUser(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str , Depends(oauth2_scheme)]
):
    
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud_profile.getProfileByRegistrationId(db, id=token_data.sub)
    if user.is_active:
        raise HTTPException(status_code=404, detail="User is inactivate")
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


"""
Here i'm checking valid otp or not
# db-otp , client-otp, db_expiry_date
"""
def verifySentOtp(db_otp: int, client_sent_otp: int, db_expiry_date: datetime) -> bool | str:
    #OTP check
    if db_otp != client_sent_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
    
    #Time check
    if datetime.now() > db_expiry_date + timedelta(minutes=2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OTP Expired"
        )
    
    return True
