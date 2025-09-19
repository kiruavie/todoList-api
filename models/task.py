from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Task(Base):
  __tablename__ = "tasks"
  
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  description = Column(String, nullable=True)
  owner_id = Column(Integer, ForeignKey("users.id"))
  
  owner = relationship("User")