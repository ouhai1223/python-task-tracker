"""任务持久化模块。"""

import json
from pathlib import Path

from task import Task


DATA_FILE = Path(__file__).resolve().parent.parent / "tasks.json"


def load_tasks():
    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    tasks = []

    for item in data:
        task = Task(item["id"], item["title"])
        tasks.append(task)

    return tasks


def save_tasks(tasks):
    data = [
        {"id": task.id, "title": task.title}
        for task in tasks
    ]

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
