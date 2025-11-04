from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, BigInteger
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    boards = relationship("Board", back_populates="owner")
    items = relationship("Item", back_populates="owner")

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    emoji_icon = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="boards")
    items = relationship("Item", back_populates="board")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(50), nullable=False, default='text')
    title = Column(String, index=True)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    board_id = Column(Integer, ForeignKey("boards.id"), nullable=True)
    owner = relationship("User", back_populates="items")
    board = relationship("Board", back_populates="items")