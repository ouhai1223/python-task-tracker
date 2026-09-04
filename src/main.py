"""Python Task Tracker 的命令行入口。"""

import sys

from storage import StorageError, load_tasks, save_tasks
from task import Task


def get_next_task_id(tasks: list[Task]) -> int:
    next_id = 1

    for task in tasks:
        if task.id >= next_id:
            next_id = task.id + 1

    return next_id


def add_task(title: str) -> None:
    tasks = load_tasks()
    task_id = get_next_task_id(tasks)
    task = Task(task_id, title)

    tasks.append(task)
    save_tasks(tasks)

    print(f"已添加任务: [{task.id}] {task.title}")


def list_tasks(completed: bool | None = None) -> None:
    tasks = load_tasks()
    filtered_tasks: list[Task] = []

    for task in tasks:
        if completed is None or task.completed == completed:
            filtered_tasks.append(task)

    if not filtered_tasks:
        print("没有符合条件的任务")
        return

    for task in filtered_tasks:
        if task.completed:
            status = "completed"
        else:
            status = "pending"

        print(f"[{task.id}] [{status}] {task.title}")


def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    task_to_delete: Task | None = None

    for task in tasks:
        if task.id == task_id:
            task_to_delete = task
            break

    if task_to_delete is None:
        print(f"未找到任务: {task_id}")
        return

    tasks.remove(task_to_delete)
    save_tasks(tasks)

    print(f"已删除任务: [{task_to_delete.id}] {task_to_delete.title}")


def complete_task(task_id: int) -> None:
    tasks = load_tasks()
    task_to_complete: Task | None = None

    for task in tasks:
        if task.id == task_id:
            task_to_complete = task
            break

    if task_to_complete is None:
        print(f"未找到任务: {task_id}")
        return

    if task_to_complete.completed:
        print(f"任务已完成: [{task_to_complete.id}] {task_to_complete.title}")
        return

    task_to_complete.completed = True
    save_tasks(tasks)
    print(f"已标记完成: [{task_to_complete.id}] {task_to_complete.title}")


def update_task(task_id: int, title: str) -> None:
    tasks = load_tasks()
    task_to_update: Task | None = None

    for task in tasks:
        if task.id == task_id:
            task_to_update = task
            break

    if task_to_update is None:
        print(f"未找到任务: {task_id}")
        return

    task_to_update.title = title
    save_tasks(tasks)
    print(f"已更新任务: [{task_to_update.id}] {task_to_update.title}")


def main() -> None:
    if len(sys.argv) < 2:
        print("用法: python .\\src\\main.py <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("错误: add 命令需要任务标题")
            return

        title = sys.argv[2].strip()
        if not title:
            print("错误: 任务标题不能为空")
            return
        add_task(title)

    elif command == "list":
        if len(sys.argv) == 2:
            list_tasks()
        elif len(sys.argv) == 3:
            status = sys.argv[2].lower()
            if status == "completed":
                list_tasks(completed=True)
            elif status == "pending":
                list_tasks(completed=False)
            else:
                print("错误: list 命令的参数必须是 'completed' 或 'pending'")
        else:
            print("用法: python .\\src\\main.py list [completed|pending]")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("错误: delete 命令需要任务 ID")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("错误: 任务 ID 必须是整数")
            return

        delete_task(task_id)

    elif command == "complete":
        if len(sys.argv) < 3:
            print("错误: complete 命令需要任务 ID")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("错误: 任务 ID 必须是整数")
            return

        complete_task(task_id)

    elif command == "update":
        if len(sys.argv) < 4:
            print("错误: update 命令需要任务 ID 和新的任务标题")
            return

        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("错误: 任务 ID 必须是整数")
            return

        title = sys.argv[3].strip()
        if not title:
            print("错误: 任务标题不能为空")
            return

        update_task(task_id, title)

    else:
        print(f"错误: 未知命令 '{command}'")
        print("可用命令: add, list, delete, complete, update")


if __name__ == "__main__":
    try:
        main()
    except StorageError as error:
        print(f"错误: {error}")
        sys.exit(1)
