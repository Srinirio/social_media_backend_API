from fastapi import APIRouter,Depends,Body, HTTPException,status,Path
from sqlalchemy.orm import Session
from typing import Annotated
from api.deps import get_db
from schemas.registration_schema import RegistrationCreate,RegistrationOut,ResetPasswordIn,Message
from crud import crud_registration,crud_profile
from api.deps import verifySentOtp
from pydantic import EmailStr

router = APIRouter()


@router.post("/registration",response_model=RegistrationOut,status_code=status.HTTP_201_CREATED)
async def registrationForm(db: Annotated[Session,Depends(get_db)],
                           obj_in: Annotated[RegistrationCreate, Body()]
):
    """
    Here we register a new user. Once they are registered, we send them an OTP and a secret key. After that, we create a profile for the user. They can access their profile after verifying the OTP.
    
    - **email**: Should be unique
    - **password**: required
    - **name**: required
    
    """
    db_obj = crud_registration.get_by_email(db=db,email=obj_in.email)
    if db_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )
    
    user = crud_registration.createRegistrationForm(db=db,obj_in=obj_in)
    
    #creating profile once register
    crud_profile.createProfile(db=db,profile_in=user)
    return RegistrationOut(otp=user.otp,secret_key=user.secret_key,message="Please verify the OTP")

@router.get("/verify_otp",response_model=Message)
async def verifyOtp(
                   db: Annotated[Session,Depends(get_db)],key: str,otp: int
):
    """
    Here we verify the OTP. Once it is successfully verified, we update the OTP status in the database. Otherwise, an error is raised.
    
    - **Secret Key**: required
    - **OTM**: required
    """
    db_obj = crud_registration.getBySecretKey(db=db,key=key)
    
    # db-otp , client-otp, db_expiry_date, 
    verifySentOtp(db_otp = db_obj.otp,client_sent_otp = otp,db_expiry_date = db_obj.otp_expiry_date)
    
        
    if(crud_registration.changeOptStatus(db=db,email=db_obj.email)):
        return Message(
            message= "Your OTP is verified ,you can login now"
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to verify OTP."
    )
"""
if user forgot password, here user can give their email and get secret-key and otm , then they can reset their password 
"""    
@router.get("/forgot_password/{email}", response_model=RegistrationOut)
async def forgotPassword(
    db: Annotated[Session,Depends(get_db)],
    email: Annotated[EmailStr , Path(...)]
):
    """
    Here , If the user forgets their password, they can provide their email to receive the secret key and OTP. After that, they can reset their password.
    
    - **Email**: Required
    """
    db_user = crud_registration.get_by_email(db=db,email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found"
        )
    new_otp = crud_registration.changeOtp(db=db,obj=db_user)
    
    return RegistrationOut(otp=new_otp,secret_key=db_user.secret_key,message="OTP is sent, please verify to reset your password")


@router.put("/reset_password",response_model=Message)
async def resetPassword(db: Annotated[Session, Depends(get_db)],
                        data_in: ResetPasswordIn):
    """
    If the user forgets their password, they can change it by providing their secret key and OTP.
    
    - **Secret key**: Required
    - **OTM** : Required
    - **New Password** : Required
    """
    db_obj = crud_registration.getBySecretKey(db=db,key=data_in.secret_key)
    
    verifySentOtp(db_otp = db_obj.otp,client_sent_otp = data_in.otp,db_expiry_date = db_obj.otp_expiry_date)
    
    crud_registration.changePassword(db=db,obj=db_obj,new_password=data_in.new_password)
    
    return Message(
        message="Successfully Updated !!!"
    )
 
@router.get("/resend_otp/{email}",response_model=RegistrationOut)
async def resendOtp(db: Annotated[Session, Depends(get_db)],
                    email: EmailStr
                    ):
    """
    Here, If the OTP has expired, the user can regenerate a new one here.
    
    - **Email**: Required
    """
    db_obj = crud_registration.get_by_email(db=db,email=email)
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found"
        )
        
    new_otp = crud_registration.changeOtp(db=db,obj=db_obj)
    return RegistrationOut(
        secret_key=db_obj.secret_key,
        otp=new_otp,
        message="OTP is sent please verify"
    )