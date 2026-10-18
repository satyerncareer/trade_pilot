from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

# Base schema shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

# Schema for incoming registration payload
class UserCreate(UserBase):
    password: str

# Schema for user API responses
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Token Response Schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    
class UserCreate(UserBase):
    email: EmailStr
    # Restrict input string length at API schema level
    password: str = Field(..., min_length=8)