from db.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Profile(Base):
    __tablename__ = "profile"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    profile_name = Column(String(50))
    bio = Column(String(200))
    profile_image = Column(String(500))
    is_private = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    
    #foreign key relationship with the Registration table
    registration_id = Column(Integer, ForeignKey('registration.id',ondelete="CASCADE",onupdate="CASCADE"), nullable=False)
    
    #relationship to the Registration model
    registration = relationship("Registration", back_populates="profile")
    posts = relationship("Post",back_populates="profile")
    likes = relationship("Like",back_populates="profile")
    comments = relationship("Comment",back_populates="profile")
    
    sent_messages = relationship("Chat", foreign_keys="[Chat.sender_id]", back_populates="sender")
    received_messages = relationship("Chat", foreign_keys="[Chat.receiver_id]", back_populates="receiver")