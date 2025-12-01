from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from ..models import Room
import uuid

async def create_room(db: AsyncSession):
    r = Room()
    db.add(r)
    await db.commit()
    await db.refresh(r)
    return r

async def get_room(db: AsyncSession, room_id: uuid.UUID):
    q = await db.execute(select(Room).where(Room.id == room_id))
    return q.scalars().first()

async def set_room_code(db: AsyncSession, room_id: uuid.UUID, code: str):
    await db.execute(update(Room).where(Room.id == room_id).values(code=code))
    await db.commit()
    return await get_room(db, room_id)
