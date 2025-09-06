from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

Tasks = {
    1: {
        "task": "Learn API's",
        "status": "pending"
    },

    2: {
        "task": "Learn python",
        "status": "Completed"
    }
}


class Task(BaseModel):
    task: str
    status: str

class UpdateTask(BaseModel):
    task: Optional[str] = None
    status: Optional[str] = None

@app.get("/tasks")
async def getTasks():
    return Tasks


@app.post("/CreateTask/{TaskID}")
async def CreateTasks(TaskID: int, task: Task):
    if TaskID in Tasks:
        return {"Error": "Task already exists!"}

    Tasks[TaskID] = task
    return Tasks[TaskID]


@app.put("/EditTask/{TaskID}")
async def EditTasks(TaskID: int, task: UpdateTask):
    if TaskID not in Tasks:
        return {"Error": "Task not found"}

    if task.task != None:
        Tasks[TaskID]["task"] = task.task

    if task.status != None:
        Tasks[TaskID]["status"] = task.status

    return Tasks[TaskID]


@app.delete("/DeleteTask/{TaskID}")
async def DeleteTask(TaskID: int):

    if TaskID not in Tasks:
        return {"Error": "Task not found!"}

    del Tasks[TaskID]
    return {"Deleted": "Successfully!"}

