from fastapi import APIRouter,Depends,Path,Query,HTTPException,status
from typing import Annotated
from sqlalchemy.orm import Session
from schemas.registration_schema import Message
from schemas.chat_schema import LatestMessagesResponse
from api.deps import get_db,getCurrentUser
from models.profile import Profile
from crud import crud_chat,crud_profile

router = APIRouter()
   
@router.post("/profile/{receiver_id}/chat",status_code=status.HTTP_201_CREATED,response_model= Message)
async def chatWithOtherProfile(
                               db: Annotated[Session, Depends(get_db)],
                               profile: Annotated[Profile, Depends(getCurrentUser)],
                               receiver_id: int ,
                               message: Annotated[str, Query(...)]
):
    """
    Here, the user provides the ID of the person they are going to send a message to.
    - **Receiver Id**: The ID of the person the user is sending the message to (Required)
    - **Message**: Required
    """
    if profile.id == receiver_id:
        raise HTTPException(
             status_code=status.HTTP_400_BAD_REQUEST,
             detail="You can't message your self"
         )
        
    db_profile = crud_profile.getProfileById(db=db,id=receiver_id)
    
    if not db_profile:
         raise HTTPException(
             status_code=status.HTTP_404_NOT_FOUND,
             detail="User Not Found"
         )
    delivered_or_not = crud_chat.createMessage(db=db,sender=profile,receiver_id=receiver_id,message=message)
    return Message(message=delivered_or_not)

@router.get("/profile/me/received_messages",response_model=LatestMessagesResponse)
async def receivedMessage(
                          db: Annotated[Session, Depends(get_db)],
                          profile: Annotated[Profile, Depends(getCurrentUser)]
):
    """
    Here, the user can view the latest received message.
    """
    latest_message = crud_chat.getLatestMessageReceived(db=db,profile=profile)

    if not latest_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No messages"
        )
    return {"messages": latest_message}

@router.delete("/profile/mychat/{message_id}/delete",response_model=Message)
async def deleteParticularChat(
                               db: Annotated[Session, Depends(get_db)],
                               profile: Annotated[Profile, Depends(getCurrentUser)],
                               message_id: int  
):
    """
    Here, the user can delete a specific message using the message ID
    """
    db_message = crud_chat.getMessage(db=db,profile=profile,message_id=message_id)
    
    response = crud_chat.changeMessageStatus(db=db,message=db_message)
    return Message(message=response)


    
