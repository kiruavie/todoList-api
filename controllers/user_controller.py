from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from utils.auth import hash_password, verify_password, create_access_token

def create_user(db: Session, user: UserCreate):
  hashed_pw = hash_password(user.password)
  new_user = User(username=user.username, password=hashed_pw)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def authenticate_user(db: Session, username: str, password: str):
  user = db.query(User).filter(User.username == username).first()
  if not user or not verify_password(password, user.password):
    return None
  token = create_access_token({"sub": user.username})
  return {"access_token": token, "token_type":"bearer"}
  