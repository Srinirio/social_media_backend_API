from sqlalchemy import Boolean, Column,Integer,String,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from db.db import Base
from datetime import datetime

class Chat(Base):
    __tablename__ = "chat"
    
    id = Column(Integer,primary_key=True,index=True)
    message = Column(String(500),nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean,default=True)
    # ForeignKey
    sender_id = Column(Integer, ForeignKey("profile.id",ondelete="CASCADE",onupdate="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("profile.id",ondelete="CASCADE",onupdate="CASCADE"))
    
    #relationship
    sender = relationship("Profile", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("Profile", foreign_keys=[receiver_id], back_populates="received_messages")
    
