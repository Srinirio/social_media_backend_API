from typing import Annotated
from sqlalchemy.orm import Session
from schemas.registration_schema import RegistrationCreate
from models import Registration
from core.security import get_password_hash, verify_password
from utils import generateSecretKey,generate_otp
from datetime import datetime
from fastapi import HTTPException,status

def get_by_email(db: Session, email: str):
    return db.query(Registration).filter(Registration.email == email).first()
    

def getBySecretKey(db: Session,key: str):
    db_obj = db.query(Registration).filter(Registration.secret_key == key).one_or_none()
    
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Secret key"
        )
    return db_obj

def createRegistrationForm(db: Session,obj_in: RegistrationCreate):
    db_obj = Registration(
        name=obj_in.name,
        email=obj_in.email,
        password=get_password_hash(obj_in.password),
        secret_key=generateSecretKey(),
        otp=generate_otp(),
        otp_expiry_date=datetime.now()
    )
    db.add(db_obj)
    db.commit()
    return db_obj

def changeOptStatus(db: Session,email: str):
    
    obj = db.query(Registration).filter(
        Registration.email == email
    ).one_or_none()
    if not obj:
        return None
    obj.is_otp_verified = True
    db.commit()
    return True

def changeOtp(db: Session,obj: Registration):
    obj.otp = generate_otp()
    obj.otp_expiry_date = datetime.now()
    db.commit()
    return obj.otp
    
def changePassword(db: Session,obj: Registration,new_password: str):
    obj.password = get_password_hash(new_password)
    db.commit()
    
    
def authenticate(db: Session,email: str,password: str):
    db_obj = get_by_email(db=db,email=email)
    
    if not db_obj:
        return None
    if not verify_password(plain_password=password,hashed_password=db_obj.password):
        return None
    return db_obj


    
    
    
    

