from ..schemas.tasks import TaskModel

class TaskModel:
    tasks: list[TaskModel] = []

    def create_task(self, id: str, title: str, completed: bool = False) -> tasks:
        self.list.append(id, title, completed)

    def get_tasks(self) -> tasks:
        return self.tasks