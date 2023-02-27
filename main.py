from fastapi import FastAPI, Depends
from database import Base, SessionLocal, engine
from models import Tasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskSchema(BaseModel):
    task_no: int
    task: str
    class Config:
        orm_mode = True


class TaskCreateSchema(BaseModel):
    task: str
    class Config:
        orm_mode = True


#Read
@app.get("/tasks",response_model=list[TaskSchema])
def get_tasks(db:Session = Depends(get_db)):
    return db.query(Tasks).all()


#Create
@app.post("/tasks",response_model=TaskSchema)
def post_tasks(task:TaskCreateSchema ,db:Session = Depends(get_db)):
    obj = Tasks(task=task.task)
    db.add(obj)
    db.commit()
    return obj


#Update
@app.put("/tasks/{task_no}", response_model=TaskSchema)
def update_task(task_no:int,task:TaskCreateSchema, db:Session=Depends(get_db)):
    try:
        obj = db.query(Tasks).filter(Tasks.task_no == task_no).first()
        obj.task = task.task
        db.add(obj)
        db.commit()
    except:
        return HTTPException(status_code=404, detail="task not found")


#Delete
@app.delete("/tasks/{task_no}", response_class = JSONResponse)
def delete_task(task_no:int, db:Session=Depends(get_db)):
    try:
        obj = db.query(Tasks).filter(Tasks.task_no == task_no).first()
        db.delete(obj)
        db.commit()
        return {f"Task no. {task_no} has been deleted"}

    except:
        return HTTPException(status_code=404, detail="task not found")
