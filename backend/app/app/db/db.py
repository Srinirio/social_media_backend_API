from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from core.config import settings
# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

