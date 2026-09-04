# Python Task Tracker

一个基于 Python 标准库的命令行任务管理工具，支持任务增删改、完成状态管理、状态筛选和 JSON 文件持久化。

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

运行要求：Python 3.12+ 和 Git。已验证环境为 Python 3.13.5、Windows PowerShell。

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
| 添加任务 | `python .\src\main.py add "整理项目文档"` |
| 查看全部任务 | `python .\src\main.py list` |
| 查看已完成任务 | `python .\src\main.py list completed` |
| 查看未完成任务 | `python .\src\main.py list pending` |
| 修改标题 | `python .\src\main.py update <ID> "完善项目文档"` |
| 标记完成 | `python .\src\main.py complete <ID>` |
| 删除任务 | `python .\src\main.py delete <ID>` |

包含空格的标题要放在引号中。添加和更新会清除标题两端空白，并拒绝纯空白标题。筛选条件不区分大小写，例如 `list COMPLETED` 也可以使用。

以下示例依次创建、完成、更新并删除一条任务。后续操作使用该示例任务的 ID：

```powershell
python .\src\main.py add "整理发布说明"
$taskId = [int](Read-Host "请输入新增示例任务的 ID")
python .\src\main.py list pending
python .\src\main.py complete $taskId
python .\src\main.py update $taskId "完善发布说明"
python .\src\main.py list completed
python .\src\main.py delete $taskId
python .\src\main.py list
```

列表输出示例：

```text
[1] [pending] 整理项目文档
[3] [completed] 完善发布说明
```

`tasks.json` 不存在时，程序将其视为空任务列表；第一次成功保存时创建文件。没有符合条件的任务时显示“没有符合条件的任务”。数据路径根据源码位置确定，不会随着终端工作目录改变。

任务在文件中的结构示例：

```json
[
  {
    "id": 1,
    "title": "整理项目文档",
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
│   ├── .gitkeep         # 目录占位文件
│   └── manual-test.md   # 可重复执行的手工验收流程和预期结果
├── .venv/              # 本地虚拟环境，不提交到 Git
├── tasks.json          # 运行时生成的任务数据，不提交到 Git
├── .gitignore
└── README.md
```

## Verification

[手工验收清单](tests/manual-test.md) 覆盖完整操作流程、错误输入、状态筛选、旧数据兼容和 JSON 语法损坏处理。清单提供隔离副本的准备步骤，便于重复执行并保留现有任务数据。

当前未配置自动化单元测试或 CI。

## Implementation Notes

- **模块职责**：`main.py` 负责参数解析、任务操作和结果显示；`task.py` 定义数据模型；`storage.py` 负责文件读写。
- **数据模型**：`Task` 使用 dataclass 定义 `id`、`title` 和 `completed` 字段，新任务的完成状态默认为 `False`。类型标注不执行运行时校验。
- **持久化**：保存时将 `Task` 转换为字典列表，再通过 `json.dump()` 写入文件；加载时通过 `json.load()` 读取数据并恢复对象。
- **数据兼容**：加载旧任务时使用 `item.get("completed", False)`，缺失的状态字段默认为未完成，已有状态保持不变。
- **任务更新**：根据 ID 查找已有对象并修改目标属性；标题更新保留 ID 和完成状态，成功保存后输出操作结果。
- **状态筛选**：筛选参数 `None`、`True`、`False` 分别对应全部、已完成和未完成。筛选结果用于显示，不写回数据文件。
- **错误处理**：CLI 校验必要参数、ID 格式和标题内容，业务函数处理未找到任务与重复完成。JSON 语法错误转换为 `StorageError`，由入口捕获并输出错误提示。

## Current Limitations

- 面向单用户本地使用，没有并发写入保护，也不提供恢复为 pending 的命令。
- ID 根据当前任务列表的最大 ID 加一生成，删除最大 ID 的任务后，该 ID 可能被后续任务复用。
- 目前处理的是 JSON 语法损坏；合法 JSON 的字段结构、字段类型和文件权限错误尚未全面校验或统一处理。
- 多数输入错误只打印提示并返回，退出码尚未统一为非零；捕获到 `StorageError` 时退出码为 1。`list` 会拒绝多余参数，其他命令目前只检查必要参数是否齐全。

## Development Workflow

功能变更使用独立分支管理。提交前执行手工验收，并检查工作区、文件差异和格式：

```powershell
git status
git diff
git diff --check
```

暂存与本次变更相关的文件后，检查暂存区内容：

```powershell
git diff --cached
git diff --cached --check
```

提交信息使用 `feat:`、`fix:`、`docs:` 等前缀描述变更类型。功能分支完成验收后合并到 `main`；版本发布时可创建 tag 标记对应提交。
