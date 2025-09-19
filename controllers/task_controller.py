from sqlalchemy.orm import Session
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from fastapi import HTTPException



# Créer une tâche
def create_task(db: Session, task: TaskCreate, user_id: int):
  new_task = Task(title=task.title, description=task.description, owner_id = user_id)
  db.add(new_task)
  db.commit()
  db.refresh(new_task)
  return new_task

# obtenir une tâche par son id
def get_task(db: Session, task_id:int, user_id:int):
  task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
  
  if not task:
    raise HTTPException(status_code=404, detail="Task not found")
  return task

# voir tous mes todos
def get_tasks(db: Session, user_id: int):
  tasks = db.query(Task).filter(Task.owner_id == user_id).all()
  return tasks



def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description

    db.commit()
    db.refresh(task)
    return task


# supprimer une todo
def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
