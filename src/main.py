"""Python Task Tracker 的命令行入口。"""

import sys

from storage import StorageError, load_tasks, save_tasks
from task import Task


def get_next_task_id(tasks):
    next_id = 1

    for task in tasks:
        if task.id >= next_id:
            next_id = task.id + 1

    return next_id


def add_task(title):
    tasks = load_tasks()
    task_id = get_next_task_id(tasks)
    task = Task(task_id, title)

    tasks.append(task)
    save_tasks(tasks)

    print(f"已添加任务: [{task.id}] {task.title}")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("暂无任务")
        return

    for task in tasks:
        print(f"[{task.id}] {task.title}")


def delete_task(task_id):
    tasks = load_tasks()
    task_to_delete = None

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


def main():
    if len(sys.argv) < 2:
        print("用法: python .\\src\\main.py <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("错误: add 命令需要任务标题")
            return

        title = sys.argv[2]
        title = title.strip()
        if not title:
            print("错误: 任务标题不能为空")
            return
        add_task(title)

    elif command == "list":
        list_tasks()

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

    else:
        print(f"错误: 未知命令 '{command}'")
        print("可用命令: add, list, delete")


if __name__ == "__main__":
    try:
        main()
    except StorageError as error:
        print(f"错误: {error}")
        sys.exit(1)
