from pydantic import BaseModel

class TaskCreate(BaseModel):
  title: str
  description: str | None = None
  
class TaskUpdate(BaseModel):
  title: str | None
  description: str | None
  
class TaskResponse(BaseModel):
  id: int
  title: str
  description: str | None
  owner_id: int
  
  class Config:
    orm_mode = True
    
    
