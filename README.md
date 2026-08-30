# Python Task Tracker

## 项目目标

Python Task Tracker 是一个使用 Python 开发的命令行任务追踪器。

项目将从最小可运行程序开始，逐步实现添加任务、查看任务、标记任务完成和删除任务等功能。

通过这个项目，我希望练习：

- Python 的基础语法与程序设计
- Python 项目、模块和包的组织方式
- 虚拟环境与项目依赖管理
- 自动化测试
- Git 版本控制
- 将一个想法逐步实现为完整项目的工程过程

## 当前状态

项目目前已完成基础目录初始化，并能够运行最小 Python 入口。

## 目录结构

```text
python-task-tracker/
├── .venv/           # 项目的本地 Python 虚拟环境，不提交到 Git
├── src/             # 存放正式源代码
│   └── main.py      # 当前程序入口
├── tests/           # 存放自动化测试代码
├── .gitignore       # 声明 Git 不需要追踪的文件
└── README.md        # 项目说明文档
```

## 运行方式

首先激活项目的虚拟环境，然后在项目根目录运行：

```powershell
python .\src\main.py
```

当前程序会输出：

```text
任务追踪器已启动
```