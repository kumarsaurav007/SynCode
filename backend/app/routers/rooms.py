from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..database import get_db
from ..services.room_service import create_room as svc_create_room, get_room as svc_get_room
from ..schemas import RoomCreateResponse, RoomInfo

router = APIRouter()

@router.post("/rooms", response_model=RoomCreateResponse)
async def create_room(db: AsyncSession = Depends(get_db)):
    r = await svc_create_room(db)
    return {"roomId": r.id}

@router.get("/rooms/{room_id}", response_model=RoomInfo)
async def get_room(room_id: str, db: AsyncSession = Depends(get_db)):
    try:
        rid = UUID(room_id)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid room id")

    r = await svc_get_room(db, rid)
    if not r:
        raise HTTPException(status_code=404, detail="room not found")
    return {"roomId": r.id, "code": r.code or "", "language": r.language or "python"}
