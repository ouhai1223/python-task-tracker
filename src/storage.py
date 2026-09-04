"""任务持久化模块。"""

import json
from pathlib import Path

from task import Task


class StorageError(Exception):
    pass


DATA_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def load_tasks() -> list[Task]:
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as error:
            raise StorageError("tasks.json 文件已损坏，无法读取") from error

    tasks = []

    for item in data:
        task = Task(item["id"], item["title"], item.get("completed", False))
        tasks.append(task)

    return tasks


def save_tasks(tasks: list[Task]) -> None:
    data: list[dict[str, int | str | bool]] = [
        {"id": task.id, "title": task.title, "completed": task.completed }
        for task in tasks
    ]

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
