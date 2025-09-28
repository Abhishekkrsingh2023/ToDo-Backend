from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated, List

import crud
import schemas
import models
from database import get_db
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    db_dependency
)

# Create routers
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
todo_router = APIRouter(prefix="/todos", tags=["todos"])

user_dependency = Annotated[models.User, Depends(get_current_user)]

# Authentication routes
@auth_router.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: db_dependency):
    """Register a new user."""
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    db_user_name = crud.get_user_by_username(db, username=user.username)

    if db_user_name or db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    return crud.create_user(db=db, user=user)


@auth_router.post("/login", response_model=schemas.Token)
async def login(db: db_dependency,
                form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Todo routes
@todo_router.get("/", response_model=List[schemas.TodoResponse])
async def get_todos(
    db: db_dependency,
    current_user: user_dependency, # user dependency injection
    skip: int = 0,
    limit: int = 100
):
    """Get all todos for the current user."""
    todos = crud.get_todos(db, user_id=current_user.id, skip=skip, limit=limit)
    return todos


@todo_router.post("/", response_model=schemas.TodoResponse)
async def create_todo(
    todo: schemas.TodoCreate,
    db: db_dependency,
    current_user: user_dependency # user dependency injection
):
    """Create a new todo for the current user."""
    return crud.create_todo(db=db, todo=todo, user_id=current_user.id)


@todo_router.get("/{todo_id}", response_model=schemas.TodoResponse)
async def get_todo(
    todo_id: int,
    db: db_dependency,
    current_user: user_dependency # user dependency injection
):
    """Get a specific todo for the current user."""
    db_todo = crud.get_todo(db, todo_id=todo_id, user_id=current_user.id)
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return db_todo


@todo_router.put("/{todo_id}", response_model=schemas.TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: schemas.TodoUpdate,
    db: db_dependency,
    current_user: user_dependency # user dependency injection
):
    """Update a specific todo for the current user."""
    db_todo = crud.update_todo(
        db, todo_id=todo_id, todo_update=todo_update, user_id=current_user.id
    )
    if db_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return db_todo


@todo_router.delete("/{todo_id}", response_model=schemas.Message)
async def delete_todo(
    todo_id: int,
    db: db_dependency,
    current_user: user_dependency # user dependency injection
):
    """Delete a specific todo for the current user."""
    success = crud.delete_todo(db, todo_id=todo_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return {"message": "Todo deleted successfully"}