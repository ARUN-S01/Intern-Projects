from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import warnings
import uuid


class Schema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field()
    email: EmailStr = Field()
    phone: str = Field(max_length=10, min_length=10)
    age: int = Field(ge=18, le=60)

class UpdateSchema(BaseModel):
    phone: str = Field(max_length=10, min_length=10)
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=18, le=60)

class DeleteSchema(BaseModel):
    warnings.filterwarnings('ignore')
    phone: str = Field(max_length=10, min_length=10)