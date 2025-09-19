from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from controllers import user_controller


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
  return user_controller.create_user(db, user)


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
  token = user_controller.authenticate_user(db, user.username, user.password)
  if not token:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  return token
