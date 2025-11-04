import os
import logging
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from dotenv import load_dotenv

from . import crud, models, schemas
from .database import engine, get_db

load_dotenv()
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Izbranoe Pro API")

bot_token = os.getenv("BOT_TOKEN")
bot = Bot(token=bot_token) if bot_token else None

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.post("/users/", response_model=schemas.User)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id=user.telegram_id)
    if db_user: raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{telegram_id}", response_model=schemas.User)
def get_user_endpoint(telegram_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if not db_user: raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/resolve-username/{username}")
async def resolve_username_endpoint(username: str):
    if not bot: raise HTTPException(status_code=500, detail="Bot not configured")
    try:
        chat = await bot.get_chat(chat_id=f"@{username}")
        return {"telegram_id": chat.id}
    except TelegramBadRequest: raise HTTPException(status_code=404, detail="Username not found")
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{telegram_id}/boards/", response_model=List[schemas.Board])
def read_user_boards_endpoint(telegram_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None: raise HTTPException(status_code=404, detail="User not found")
    return crud.get_boards_by_user(db, user_id=user.id)

@app.post("/users/{telegram_id}/boards/", response_model=schemas.Board)
def create_board_for_user_endpoint(telegram_id: int, board: schemas.BoardCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None:
        user = crud.create_user(db, schemas.UserCreate(telegram_id=telegram_id))
    return crud.create_user_board(db=db, board=board, user_id=user.id)

@app.get("/boards/{board_id}", response_model=schemas.Board)
def read_board_endpoint(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_board_by_id(db, board_id=board_id)
    if db_board is None: raise HTTPException(status_code=404, detail="Board not found")
    return db_board

@app.delete("/boards/{board_id}")
def delete_board_endpoint(board_id: int, db: Session = Depends(get_db)):
    db_board = crud.get_board_by_id(db, board_id=board_id)
    if db_board is None: raise HTTPException(status_code=404, detail="Board not found")
    crud.delete_board(db=db, board=db_board)
    return {"ok": True}

@app.get("/users/{telegram_id}/search/", response_model=List[schemas.Item])
def search_items_endpoint(telegram_id: int, q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return crud.search_items_by_title(db, user_id=user.id, query=q)

@app.post("/users/{telegram_id}/items/", response_model=schemas.Item)
def create_item_for_user(telegram_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id=telegram_id)
    if user is None: raise HTTPException(status_code=404, detail="User not found")
    return crud.create_user_item(db=db, item=item, user_id=user.id)

@app.get("/boards/{board_id}/items/", response_model=List[schemas.Item])
def read_board_items(board_id: int, db: Session = Depends(get_db)):
    return crud.get_items_by_board(db, board_id=board_id)

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item_by_id(db, item_id=item_id)
    if db_item is None: raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}/move/{board_id}", response_model=schemas.Item)
def move_item(item_id: int, board_id: int, db: Session = Depends(get_db)):
    item = crud.get_item_by_id(db, item_id=item_id)
    if not item: raise HTTPException(status_code=404, detail="Item not found")
    return crud.move_item_to_board(db, item=item, board_id=board_id)
    
@app.delete("/items/{item_id}")
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_item_by_id(db, item_id=item_id)
    if not success: raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}

@app.get("/items/{item_id}/download_url")
async def get_item_download_url(item_id: int, db: Session = Depends(get_db)):
    if not bot: raise HTTPException(status_code=500, detail="Bot not configured")
    db_item = crud.get_item_by_id(db, item_id=item_id)
    if not db_item: raise HTTPException(status_code=404, detail="Item not found")
    if db_item.item_type == 'text' or db_item.item_type == 'location':
        return {"url": db_item.content, "is_media": False}
    try:
        file_info = await bot.get_file(db_item.content)
        return {"url": f"https://api.telegram.org/file/bot{bot_token}/{file_info.file_path}", "is_media": True}
    except Exception as e:
        logging.error(f"Failed to get file link: {e}")
        raise HTTPException(status_code=500, detail="Failed to get file link from Telegram.")