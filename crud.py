from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas
from auth import get_password_hash


# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password) # password hashing
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Todo CRUD operations
def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Todo]:
    """Get all todos for a specific user."""
    return db.query(models.Todo).filter(
        models.Todo.user_id == user_id
    ).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int, user_id: int) -> Optional[models.Todo]:
    """Get a specific todo by ID for a specific user."""
    return db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == user_id
    ).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
    """Create a new todo for a user."""
    db_todo = models.Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(
    db: Session, 
    todo_id: int, 
    todo_update: schemas.TodoUpdate, 
    user_id: int
) -> Optional[models.Todo]:
    """Update a specific todo for a user."""
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == user_id
    ).first()
    
    if db_todo:
        update_data = todo_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        
        db.commit()
        db.refresh(db_todo)
    
    return db_todo

def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
    """Delete a specific todo for a user."""
    db_todo = db.query(models.Todo).filter(
        models.Todo.id == todo_id,
        models.Todo.user_id == user_id
    ).first()
    
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False