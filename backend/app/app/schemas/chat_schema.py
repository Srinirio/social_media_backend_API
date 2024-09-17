from pydantic import BaseModel
from datetime import datetime

class MessageDetails(BaseModel):
    message: str
    date: datetime

class LatestMessagesResponse(BaseModel):
    messages: dict[str, MessageDetails]
