from fastapi import APIRouter, Body,Depends,UploadFile,Form,File,HTTPException,status
from api.deps import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from api.deps import getCurrentUser
from schemas.profile_schema import ProfileOut,ListOfProfile,ProfileResponse
from schemas.registration_schema import Message
from models.profile import Profile
from crud import crud_profile

router = APIRouter()


@router.get("/profile/me",response_model=ProfileOut)
async def myProfile(db: Annotated[Session, Depends(get_db)],
                    user_profile: Annotated[Profile, Depends(getCurrentUser)]
                    ):
    """
    Once the user registers and verifies their OTP, they can access their profile. At this point, we decode the token to retrieve the current user's profile.
    
    - **Username**
    - **User Id**
    - **Profile name**
    - **Bio**
    - **Profile Image**
    - **Private or not**
    """
    return ProfileOut(
        name=user_profile.username,
        id=user_profile.id,
        profile_name=user_profile.profile_name,
        bio=user_profile.bio,
        image=user_profile.profile_image,
        is_private=user_profile.is_private
    )

@router.get("/profile/all",response_model=ListOfProfile)
async def getAllProfile(
    db: Annotated[Session, Depends(get_db)],
    # user_profile: Annotated[Profile, Depends(getCurrentUser)]
):
    """
    Here, the user can view all other profiles.
    - **Username**
    - **User Id**
    - **Profile name**
    - **Bio**
    - **Profile Image**
    - **Private or not**
    """
    list_of_pro = crud_profile.getAllProfile(db=db)
    # Convert each Profile model instance to a ProfileOut Pydantic model
    list_of_profile_out = []
    for data in list_of_pro:
        list_of_profile_out.append(ProfileOut(
            name=data.username,
            id=data.id,
            profile_name=data.profile_name,
            bio=data.bio,
            image=data.profile_image,
            is_private=data.is_private
        ))
    return ListOfProfile(list_of_profile=list_of_profile_out)

@router.get("/profile/{user_name}",response_model=ListOfProfile)
async def showProfileByName(
                            db: Annotated[Session, Depends(get_db)],
                            # profile: Annotated[Profile, Depends(getCurrentUser)],
                            username: str
):
    """
    Here, the user can search for other profiles by their name.
    
    - **List of**
    - **Username**
    - **User Id**
    - **Profile name**
    - **Bio**
    - **Profile Image**
    - **Private or not**
    """
    db_profiles = crud_profile.getUsersByUsername(db=db,name=username)
    if not db_profiles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No user found this name :{username}"
        )
    list_of_profile_out = []
    for data in db_profiles:
        list_of_profile_out.append(ProfileOut(
            name=data.username,
            id=data.id,
            profile_name=data.profile_name,
            bio=data.bio,
            image=data.profile_image,
            is_private=data.is_private
        ))
    return ListOfProfile(list_of_profile=list_of_profile_out)


@router.put("/profile/me/update",response_model=ProfileResponse)
async def updateMyProfile(*,
                   db: Annotated[Session, Depends(get_db)],
                   profile_in: Annotated[Profile, Depends(getCurrentUser)],
                   profile_name: Annotated[str | None, Form()] = None,
                   image: Annotated[UploadFile | None , File()] = None,
                   username: Annotated[str | None, Form()] = None,
                   bio: Annotated[str | None, Form()] = None,
                   private_or_not: Annotated[bool | None, Form()] = None
):
    """
    Here user can update their field's
    - **Username**(Optional)
    - **Profile name**(Optional)(Unique)
    - **Bio**
    - **Profile Image**
    - **Private or not**
    """
    #Check profile name is unique
    if crud_profile.checkUniqueProfileName(db=db,name_in=profile_name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User name is already taken"
        )
        
    return crud_profile.updateProfile(
        db=db,
        pro_in=profile_in,
        profile_name=profile_name,
        image=image,
        username=username,
        bio=bio,
        private_or_not=private_or_not
    )

@router.patch("/profile/me/update/bio", response_model=Message)
async def updateProfileBio(
    db: Annotated[Session, Depends(get_db)],
    profile_in: Annotated[Profile, Depends(getCurrentUser)],
    bio: Annotated[str, Form(...)]
):
    """
    Update Profile **DB**
    - **Bio**: Required
    """
    return Message(
        message=crud_profile.updateBio(db=db,profile_in=profile_in,bio=bio)
    )
   
@router.patch("/profile/me/update/name", response_model=Message)
async def updateProfileBio(
    db: Annotated[Session, Depends(get_db)],
    profile_in: Annotated[Profile, Depends(getCurrentUser)],
    name: Annotated[str, Form(...)]
):
    """
    Update Profile **DB**
    - **Name**: Required
    """
    return Message(
        message=crud_profile.updateName(db=db,profile_in=profile_in,name=name)
    )

@router.patch("/profile/me/update/is_private", response_model=Message)
async def updateProfileBio(
    db: Annotated[Session, Depends(get_db)],
    profile_in: Annotated[Profile, Depends(getCurrentUser)],
    private_or_not: Annotated[bool, Form(...)]
):
    """
    Update Profile **DB**
    - **Private status**: Required
    """
    return Message(
        message=crud_profile.updatePrivateOrNot(db=db,profile_in=profile_in,value_in=private_or_not)
    )
   
@router.patch("/profile/me/update/profile_image", response_model=Message)
async def updateProfileBio(
    db: Annotated[Session, Depends(get_db)],
    profile_in: Annotated[Profile, Depends(getCurrentUser)],
    image: Annotated[UploadFile, File()]
):
    """
    Update Profile **DB**
    - **Image**: Required
    """
    return Message(
        message=crud_profile.updateProfileImage(db=db,profile_in=profile_in,value_in=image)
    )

@router.delete("/profile/me/delete",response_model=Message)
async def deleteProfile(
    db: Annotated[Session, Depends(get_db)],
    profile_in: Annotated[Profile, Depends(getCurrentUser)],
):
    """
    To delete a user, change their active status.
    """
    obj = crud_profile.changeActiveStatus(db=db,profile=profile_in)
    
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Something went wrong"
        )
    return Message(message=obj)