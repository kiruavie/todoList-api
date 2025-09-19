from fastapi import FastAPI
from database import Base, engine 
from routes.user_route import router as user_router
from routes.task_route import router as task_router

# créer la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API - FastAPI")



# inclures les routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(task_router, prefix="/tasks", tags=["Tasks"])

