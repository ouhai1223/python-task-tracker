# Python Task Tracker

一个使用 Python 标准库实现的命令行任务追踪器，支持任务增删改、完成状态和 JSON 文件持久化。这是 12 周计算机方向探索计划的第一个项目，用来练习 Python 工程基础与 Git 工作流。

## Features

- `add`：添加任务，自动生成 ID，默认状态为 `pending`。
- `list`：显示任务 ID、状态和标题；可按 `completed` / `pending` 筛选，筛选不会修改文件。
- `update`：修改任务标题，保留 ID 和完成状态。
- `complete`：标记任务完成；重复操作会提示任务已经完成。
- `delete`：根据 ID 删除任务。
- 使用项目根目录的 `tasks.json` 保存数据，重新启动程序后恢复任务。
- 兼容没有 `completed` 字段的旧任务，默认将其视为未完成。
- 对缺少必要参数、非整数 ID、空白标题、未知命令和非法筛选条件给出提示。
- JSON 语法损坏时停止操作并报告错误，避免把损坏数据当成空列表覆盖。

## Installation

准备 Python 3.12+ 和 Git。本次本地验收使用 Python 3.13.5；以下命令适用于 Windows PowerShell。

获取项目并进入目录；已经有本地仓库时，直接进入现有目录：

```powershell
git clone https://github.com/ouhai1223/python-task-tracker.git
Set-Location python-task-tracker
```

创建并激活虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python .\src\main.py
```

最后一条命令应显示用法。项目目前只使用 Python 标准库，无需安装第三方依赖。

也可以不激活环境，直接使用虚拟环境中的解释器：

```powershell
.\.venv\Scripts\python.exe .\src\main.py list
```

## Usage

以下命令在项目根目录、虚拟环境已激活时执行。`<ID>` 是占位符，需要替换为添加任务时输出的实际整数，不能连同尖括号直接输入。

| 操作 | 命令 |
|---|---|
| 添加任务 | `python .\src\main.py add "学习 Python"` |
| 查看全部任务 | `python .\src\main.py list` |
| 查看已完成任务 | `python .\src\main.py list completed` |
| 查看未完成任务 | `python .\src\main.py list pending` |
| 修改标题 | `python .\src\main.py update <ID> "复习 Python 文件操作"` |
| 标记完成 | `python .\src\main.py complete <ID>` |
| 删除任务 | `python .\src\main.py delete <ID>` |

包含空格的标题要放在引号中。添加和更新会清除标题两端空白，并拒绝纯空白标题。筛选条件不区分大小写，例如 `list COMPLETED` 也可以使用。

下面的例子会创建一条练习任务，然后修改、完成并删除它。输入 ID 时只填写刚才添加的练习任务 ID：

```powershell
python .\src\main.py add "练习 JSON 持久化"
$taskId = [int](Read-Host "请输入刚才输出的练习任务 ID")
python .\src\main.py list pending
python .\src\main.py complete $taskId
python .\src\main.py update $taskId "复习 JSON 持久化"
python .\src\main.py list completed
python .\src\main.py delete $taskId
python .\src\main.py list
```

列表输出示例：

```text
[1] [pending] 学习 Python
[3] [completed] 复习 JSON 持久化
```

`tasks.json` 不存在时，程序将其视为空任务列表；第一次成功保存时创建文件。没有符合条件的任务时显示“没有符合条件的任务”。数据路径根据源码位置确定，不会随着终端工作目录改变。

任务在文件中的结构示例：

```json
[
  {
    "id": 1,
    "title": "学习 Python",
    "completed": false
  }
]
```

## Project Structure

```text
python-task-tracker/
├── src/
│   ├── main.py          # CLI 参数解析、任务操作和结果显示
│   ├── task.py          # Task dataclass：id、title、completed
│   └── storage.py       # JSON 读取、对象转换、保存和 StorageError
├── tests/
│   ├── .gitkeep         # 原有目录占位文件
│   └── manual-test.md   # 可重复执行的手工验收流程和预期结果
├── .venv/              # 本地虚拟环境，不提交到 Git
├── tasks.json          # 运行时生成的任务数据，不提交到 Git
├── .gitignore
└── README.md
```

## Verification

按 [手工验收清单](tests/manual-test.md) 检查完整操作流程、错误输入和持久化边界。清单提供隔离副本的准备步骤，便于重复执行并保留原任务数据。

当前仓库采用手工验收清单，没有已落盘的自动化单元测试套件。清单中记录的助手隔离验证不等同于仓库已配置 pytest 或 CI。

## What I Learned

- 用模块分工组织程序：入口处理命令，数据模型描述任务，存储模块负责文件读写。
- `@dataclass` 可以生成初始化、对象显示和比较方法；类型标注表达设计，不会自动校验或转换输入。
- 程序内部使用 `Task` 对象；保存时转换成字典，读取 JSON 后再恢复对象。
- 修改内存中的属性不等于保存文件，持久化需要显式调用 `save_tasks()`。
- 用 `item.get("completed", False)` 为旧数据提供默认状态，同时保留已有的 `True` / `False`。
- 任务 ID 与列表下标不同；修改已有对象的属性可以保留其余字段。
- 筛选参数中，`None` 表示全部，`True` 表示已完成，`False` 表示未完成；需要用 `is None` 区分“全部”和“未完成”。
- CLI 检查参数数量和格式，业务函数处理查找与状态变化；`StorageError` 将 JSON 语法错误传递给入口统一提示。
- 用正常路径、失败路径和跨进程操作检查功能；用 README 说明安装、使用方法和项目限制。
- 使用功能分支、`git diff`、暂存区和有意义的提交记录组织修改。

## Current Limitations

- 这是单用户本地文件项目，没有并发写入保护，也不提供恢复为 pending 的命令。
- ID 根据当前任务列表的最大 ID 加一生成，删除最大 ID 的任务后，该 ID 可能被后续任务复用。
- 目前处理的是 JSON 语法损坏；合法 JSON 的字段结构、字段类型和文件权限错误尚未全面校验或统一处理。
- 多数输入错误只打印提示并返回，退出码尚未统一为非零；捕获到 `StorageError` 时退出码为 1。`list` 会拒绝多余参数，其他命令目前只检查必要参数是否齐全。

## Development Workflow

开始新工作前检查状态；当前工作提交或妥善保存后，再按需要切换主分支、同步远程并创建 `codex/` 前缀的功能分支。

```powershell
git status
git diff
git diff --check
```

只暂存本次修改的文件，再用 `git diff --cached` 检查准备提交的内容。Day 6 完成源码、文档和验收后，建议提交信息为：

```text
feat: complete task tracker v1
```

提交和推送是两个步骤；首次推送功能分支时设置对应的远程跟踪分支。`v1.0.0` tag 是验收后的可选版本标记。
