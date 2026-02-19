from sqlalchemy.orm import Session
from app.repositories.task_repository import TaskRepository


class TaskService:

    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def create_task(self, title: str, user_id: int, description: str | None = None):
        return self.repo.create(
            title=title,
            user_id=user_id,
            description=description
        )
    
    def get_tasks(self, user_id: int):
        return self.repo.get_all_by_user(user_id)
    
    def get_task(self, task_id: int, user_id: int):
        return self.repo.get_by_id_and_user(task_id, user_id)
    
    def delete_task(self, task_id: int, user_id: int):
        task = self.repo.get_by_id_and_user(task_id, user_id)
        if not task:
            return None
        self.repo.delete(task)
        return True