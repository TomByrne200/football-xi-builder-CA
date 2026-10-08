from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = {"*"},
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return{"message": "CRUD API is working!"}

@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title = task.title,
        description = task.description,
        completed = task.completed
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task

@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    return tasks

@app.get("/tasks/{task_id}",response_model = schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail = "Task not found")

    return task

@app.put("/tasks/{task_id}", response_model = schemas.Task)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.completed = updated_task.completed

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code = 404, detail = "Task not found")
        
    db.delete(task)
    db.commit()

    return {"message": "Task deleted sucessfully"}