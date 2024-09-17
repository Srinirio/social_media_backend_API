from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from db.db import Base

class Like(Base):
    __tablename__ = "like"
    
    id = Column(Integer,primary_key=True,index=True)
    
    # ForeignKey
    post_id = Column(Integer,ForeignKey("post.id",onupdate="CASCADE",ondelete="CASCADE"))
    profile_id = Column(Integer,ForeignKey("profile.id",onupdate="CASCADE",ondelete="CASCADE"))
    
    # relationship
    post = relationship("Post",back_populates="likes")
    profile = relationship("Profile",back_populates="likes")