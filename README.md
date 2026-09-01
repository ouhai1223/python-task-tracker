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

项目目前已经实现基于 JSON 文件持久化的三个基础命令：添加任务、列出任务和删除任务。

## 目录结构

```text
python-task-tracker/
├── .venv/           # 项目的本地 Python 虚拟环境，不提交到 Git
├── src/             # 存放正式源代码
│   ├── main.py      # CLI 入口与命令分发
│   ├── task.py      # Task 数据模型
│   └── storage.py   # JSON 文件读取与保存
├── tests/           # 存放自动化测试代码
├── tasks.json       # 运行时任务数据，不提交到 Git
├── .gitignore       # 声明 Git 不需要追踪的文件
└── README.md        # 项目说明文档
```

## 运行方式

首先激活项目的虚拟环境，然后在项目根目录运行：

```powershell
python .\src\main.py
```

可用命令：

```powershell
python .\src\main.py add "学习 Python 模块"
python .\src\main.py list
python .\src\main.py delete 1
```

## 手动验收记录

```text
> python .\src\main.py add "学习 Python 模块"
已添加任务: [1] 学习 Python 模块

> python .\src\main.py list
[1] 学习 Python 模块

> python .\src\main.py delete 1
已删除任务: [1] 学习 Python 模块
```

删除后，`tasks.json` 中保存的是空列表 `[]`。

## 开发方式

每次开始新任务前，先切换到主分支并同步远程更新：

```powershell
git switch main
git pull
```

为本次任务创建并切换到独立分支：

```powershell
git switch -c <branch-name>
```

修改文件后，检查仓库状态和具体差异：

```powershell
git status
git diff
```

选择要提交的文件，并检查暂存区中的内容：

```powershell
git add <file>
git diff --staged
```

确认改动无误后，创建含义清楚的本地提交：

```powershell
git commit -m "<type>: <description>"
```

第一次推送新分支时，设置它跟踪对应的远程分支：

```powershell
git push -u origin <branch-name>
```

后续可以使用 `git push` 推送新的本地提交，使用 `git pull` 获取并整合远程更新。
