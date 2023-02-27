from database import Base
from sqlalchemy import Column, Integer, String

class Tasks(Base):
    __tablename__ = "tasks"
    task_no = Column(Integer, primary_key = True, index = True)
    task = Column(String(200))
