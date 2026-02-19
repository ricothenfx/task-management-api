from sqlalchemy.orm import Session
from app.models.task import Task


class TaskRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(self, title: str, user_id: int, description: str | None = None):
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all(self):
        return self.db.query(Task).all()
    
    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()

    def get_all_by_user(self, user_id: int):
        return self.db.query(Task).filter(Task.user_id == user_id).all()
    
    def get_by_id_and_user(self, task_id: int, user_id: int):
        return self.db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()