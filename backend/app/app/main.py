from fastapi import FastAPI
from api.api import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=settings.DESCRIPTION
)

@app.get("/",tags=["Root"])
async def root():
    return{
        "Message":"Hello"
    }
    
app.include_router(api_router,prefix=settings.API_V1_STR)