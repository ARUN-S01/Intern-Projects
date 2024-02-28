from pydantic import BaseModel, EmailStr, Field
from typing import List

class EmailModel(BaseModel):
    email: List[EmailStr] = Field()