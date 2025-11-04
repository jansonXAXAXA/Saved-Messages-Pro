from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(telegram_id=user.telegram_id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_board_by_id(db: Session, board_id: int):
    return db.query(models.Board).filter(models.Board.id == board_id).first()
def get_boards_by_user(db: Session, user_id: int):
    return db.query(models.Board).filter(models.Board.owner_id == user_id).all()
def create_user_board(db: Session, board: schemas.BoardCreate, user_id: int):
    db_board = models.Board(**board.dict(), owner_id=user_id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board
def delete_board(db: Session, board: models.Board):
    for item in board.items:
        item.board_id = None
    db.delete(board)
    db.commit()

def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
def get_items_by_board(db: Session, board_id: int):
    return db.query(models.Item).filter(models.Item.board_id == board_id).all()
def move_item_to_board(db: Session, item: models.Item, board_id: int):
    item.board_id = board_id
    db.commit()
    db.refresh(item)
    return item
def search_items_by_title(db: Session, user_id: int, query: str):
    return db.query(models.Item).filter(models.Item.owner_id == user_id, models.Item.title.ilike(f"%{query}%")).all()
def delete_item_by_id(db: Session, item_id: int):
    db_item = get_item_by_id(db, item_id=item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False