# import uuid
# from abc import ABC, abstractmethod
# from typing import Any
#
# from src.data.model import Task
# from src.data.schema.task import TaskUpdateSchema
# from src.data.schema.task.crud import TaskCreateSchema, TaskOutSchema
#
#
# class TaskRepo(ABC):
#     @abstractmethod
#     async def create_task(self, data: TaskCreateSchema) -> TaskOutSchema:
#         pass
#
#     @abstractmethod
#     async def update_task(self, target: uuid.UUID | Task, data: TaskUpdateSchema) -> TaskOutSchema:
#         pass
#
#     @abstractmethod
#     async def get_task_by_input(self, key: str, value: Any) -> TaskOutSchema:
#         pass
