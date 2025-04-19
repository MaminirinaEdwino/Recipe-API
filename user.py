
from db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from typing import Optional

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)


# --- Data Models (Pydantic) ---
class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
	
