from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from db.db import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class PostImage(Base):
    __tablename__ = "post_image"
    
    id = Column(Integer,primary_key=True,index=True)
    image_path = Column(String(200))
    
    # ForeignKey
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    
    # relationship
    post = relationship("Post",back_populates="images")

class Post(Base):
    __tablename__ = "post"
    
    id = Column(Integer,primary_key=True,index=True)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)
    # ForeignKey
    profile_id = Column(Integer, ForeignKey("profile.id", ondelete="CASCADE",onupdate="CASCADE"),nullable=False)
    
    # relationship
    images = relationship("PostImage",back_populates="post")
    profile = relationship("Profile",back_populates="posts")
    likes = relationship("Like",back_populates="post")
    comments = relationship("Comment",back_populates="post")