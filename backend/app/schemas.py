from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class RoomCreateResponse(BaseModel):
    roomId: UUID

class RoomInfo(BaseModel):
    roomId: UUID
    code: str
    language: str

class AutocompleteRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str

class AutocompleteResponse(BaseModel):
    suggestion: str

class CodeUpdate(BaseModel):
    code: str
    cursor: Optional[int] = None
    sender: Optional[str] = None
