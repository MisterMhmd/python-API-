from sqlalchemy import Column, Integer, String
from Database import Base

class Tasks(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String)
    status = Column(String, default="pending")