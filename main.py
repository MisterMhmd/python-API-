from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import models
from Database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def getDB():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Task(BaseModel):
    task: str

class UpdateTask(BaseModel):
    task: Optional[str] = None

@app.get("/tasks")
async def getTasks(db: Session = Depends(getDB)):
    return db.query(models.Tasks).all()

@app.get("/tasks/{TaskID}")
async def getTasks(TaskID: int, db: Session = Depends(getDB)):
    task_model = db.query(models.Tasks).filter(models.Tasks.id == TaskID).first()
    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f" task {TaskID} is not found!"
        )

    return task_model

@app.post("/tasks")
async def CreateTasks(task: Task, db: Session = Depends(getDB)):

    task_model = models.Tasks()
    task_model.task = task.task
    task_model.status = "pending"

    db.add(task_model)
    db.commit()
    return task


@app.put("/tasks/{TaskID}")
async def EditTasks(TaskID: int, task: UpdateTask, db: Session = Depends(getDB)):
    task_model = db.query(models.Tasks).filter(models.Tasks.id == TaskID).first()
    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f" task {TaskID} is not found!"
        )

    task_model.task = task.task

    db.add(task_model)
    db.commit()

    return task

@app.patch("/tasks/{TaskID}")
async def MarkAsCompleted(TaskID: int, db: Session = Depends(getDB)):
    task_model = db.query(models.Tasks).filter(models.Tasks.id == TaskID).first()

    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f" task {TaskID} is not found!"
        )

    task_model.status = "Completed"
    db.add(task_model)
    db.commit()
    return {"Task": "marked as completed!"}

@app.delete("/tasks/{TaskID}")
async def DeleteTask(TaskID: int, db: Session = Depends(getDB)):

    task_model = db.query(models.Tasks).filter(models.Tasks.id == TaskID).first()
    if task_model is None:
        raise HTTPException(
            status_code=404,
            detail=f" task {TaskID} is not found!"
        )

    db.delete(task_model)
    db.commit()


    return {"Deleted": "Successfully!"}

