from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from db.db import Base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Registration(Base):
    __tablename__ = "registration"
    
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(50),nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    password = Column(String(200),nullable=False)
    secret_key = Column(String(200),nullable=False,unique=True)
    registration_date = Column(DateTime,nullable=False,default=func.now())
    otp = Column(Integer)
    otp_expiry_date = Column(DateTime)
    is_otp_verified = Column(Boolean,default=False)
    
    #relationships
    profile = relationship("Profile",back_populates="registration")