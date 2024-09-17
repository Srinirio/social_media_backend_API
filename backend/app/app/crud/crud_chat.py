from sqlalchemy.orm import Session
from models.profile import Profile
from models.chat import Chat
from fastapi import HTTPException,status
from sqlalchemy import and_, func
"""
Insert the message in DB
"""
def createMessage(db: Session, receiver_id: int, sender: Profile,message: str):
    created_message = Chat(
        message=message,
        sender_id=sender.id,
        receiver_id=receiver_id
    )
    db.add(created_message)
    db.commit()
    db.refresh(created_message)
    return "Successfully sent!!"

"""
get latest message received
"""
def getLatestMessageReceived(db: Session,profile: Profile):
     # Subquery to get the latest message timestamp for each sender
    subquery = db.query(
        Chat.sender_id,
        func.max(Chat.created_at).label("latest_message_time")
    ).filter(
        and_(Chat.receiver_id == profile.id, Chat.is_active == True)
    ).group_by(Chat.sender_id).subquery()

    # Main query to join the subquery and get the latest messages
    latest_messages = db.query(Chat).join(
        subquery, and_(
            Chat.sender_id == subquery.c.sender_id,
            Chat.created_at == subquery.c.latest_message_time,
            Chat.is_active == True
        )
    ).all()
    
    list_of_message = {}
    for message in latest_messages:
          name = message.sender.username
          list_of_message[name] = {
        "message": message.message,
        "date": message.created_at
         }
    return list_of_message

"""
here we get particular message if the message id is belongs to the same user
"""
def getMessage(db: Session,
               message_id: int,
               profile: Profile 
               ):
    db_message = db.query(Chat).filter(and_(Chat.id == message_id, Chat.sender_id == profile.id, Chat.is_active == True)).one_or_none()
    print(Chat.sender_id,Profile.id)
    
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "Invalid credentials"
        )
    
    return db_message

"""
Here we going to change the status of the message
"""
def changeMessageStatus(db: Session, message: Chat):
    message.is_active = False
    db.commit()
    db.refresh(message)
    return "Successfully Deleted !!"
    
    