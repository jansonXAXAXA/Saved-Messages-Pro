from pydantic import BaseModel
from typing import List, Optional

class ItemBase(BaseModel):
    item_type: str
    title: str
    content: str
class ItemCreate(ItemBase):
    pass
class Item(ItemBase):
    id: int
    owner_id: int
    board_id: Optional[int] = None
    class Config: from_attributes = True

class BoardBase(BaseModel):
    name: str
    emoji_icon: Optional[str] = None
class BoardCreate(BoardBase):
    pass
class Board(BoardBase):
    id: int
    owner_id: int
    class Config: from_attributes = True

class User(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    boards: List[Board] = []
    class Config: from_attributes = True
class UserCreate(BaseModel):
    telegram_id: int
    username: Optional[str] = None