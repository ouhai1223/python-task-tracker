"""任务数据模型。"""
from dataclasses import dataclass


@dataclass
class Task:
    """表示任务追踪器中的一个任务。"""
    id: int
    title: str
