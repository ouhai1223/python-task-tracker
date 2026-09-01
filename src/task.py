"""任务数据模型。"""


class Task:
    """表示任务追踪器中的一个任务。"""

    def __init__(self, task_id: int, title: str):
        self.id = task_id
        self.title = title
