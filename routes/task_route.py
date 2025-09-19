from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.task import TaskCreate, TaskResponse, TaskUpdate
from controllers import task_controller
from utils.auth import decode_access_token
from fastapi.security import HTTPBearer
from models.user import User
from jwt import PyJWTError
from pydantic import BaseModel

router = APIRouter()
security = HTTPBearer()

def get_current_user(
    token: str = Depends(security), db: Session = Depends(get_db)
):
    try:
        payload = decode_access_token(token.credentials)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Vérifier que l’utilisateur existe en DB
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", response_model=TaskResponse)
def create(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_controller.create_task(db, task, user_id=current_user.id)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_controller.get_tasks(db, user_id=current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return task_controller.get_task(db, task_id=task_id, user_id=current_user.id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_controller.update_task(db, task_id=task_id, task_data=task_data, user_id=current_user.id)

class MessageResponse(BaseModel):
    detail: str

@router.delete("/{task_id}", response_model=MessageResponse)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return task_controller.delete_task(db, task_id=task_id, user_id=current_user.id)

