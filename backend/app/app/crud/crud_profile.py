from sqlalchemy.orm import Session
from models.registration import Registration
from models.profile import Profile
from fastapi import UploadFile
import os
import uuid

def createProfile(db: Session,profile_in: Registration):
    db_obj = Profile(
        registration_id = profile_in.id,
        username = profile_in.name
    )
    db.add(db_obj)
    db.commit()
    
def getProfileByRegistrationId(db: Session, id: int):
    db_obj = db.query(Profile).filter(
        Profile.registration_id == id
    ).first()
    return db_obj

"""
get profile's by username
"""
def getUsersByUsername(db: Session,name: str):
    db_profiles = db.query(Profile).filter(Profile.username == name).all()
    return db_profiles



"""
get profile by Id
"""
def getProfileById(db: Session,id: int):
    return db.query(Profile).filter(Profile.id == id).one_or_none()

"""
get All Profile
"""
def getAllProfile(db: Session):
    return db.query(Profile).all()

"""
update profile based on user choice
"""

def updateProfile(
    db: Session, 
    pro_in: Profile, 
    profile_name: str | None = None,
    image: str | None = None,
    username: str | None = None,
    bio: str | None = None,
    private_or_not: bool | None = None
):
    if username:
        pro_in.username = username
    if image:
        image_dir = "images"
        
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        #here create unique name to all image
        unique_filename = f"{uuid.uuid4()}.jpg"
        image_path = os.path.join(image_dir, unique_filename)
        with open(image_path, "wb") as buffer:
            buffer.write(image.file.read())  
        pro_in.profile_image = image_path
    if profile_name:
        pro_in.profile_name = profile_name
    if bio:
        pro_in.bio = bio
    if private_or_not is not None:
        pro_in.is_private = private_or_not
    
    db.commit()
    db.refresh(pro_in)
    return pro_in
"""
update profile bio
"""
def updateBio(db: Session, profile_in: Profile, bio: str):
    profile_in.bio = bio
    db.commit()
    return "Successfully Updated"

"""
update profile name
"""
def updateName(db: Session, profile_in: Profile, name: str):
    profile_in.username = name
    db.commit()
    return "Successfully Updated"
    
"""
update profile private_or_not
"""
def updatePrivateOrNot(db: Session, profile_in: Profile, value_in: bool):
    profile_in.is_private = value_in
    db.commit()
    return "Successfully Updated"

"""
update profile image
"""
def updateProfileImage(db: Session, profile_in: Profile, value_in: UploadFile):
    
    unique_filename = f"{uuid.uuid4()}.jpg"
    image_path = os.path.join("images", unique_filename)
    
    with open(image_path, "wb") as buffer:
        buffer.write(value_in.file.read())
    
    profile_in.profile_image = image_path
    db.commit()
    db.refresh(profile_in)
    
    return "Profile image successfully updated"

"""
check profile name is unique
"""
def checkUniqueProfileName(db:Session,name_in:str):
    return db.query(Profile).filter(Profile.profile_name == name_in).one_or_none()

"""
Delete user - By change the active status
"""
def changeActiveStatus(db: Session,profile: Profile):
    profile.is_active = True
    db.commit()
    return "Profile deleted"
    