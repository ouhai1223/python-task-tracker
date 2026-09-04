# Python Task Tracker 手工验收清单

## 使用方法与准备

本清单检查正常操作、错误输入和文件持久化。每次复验时，将结果列重置为“待执行”，执行后再填写结果；不要把历史通过记录当成本次执行结果。

先按 README 完成环境准备，在仓库根目录激活虚拟环境。下面的 PowerShell 命令会将源码复制到新建的临时目录，后续创建的 `tasks.json` 位于副本中，不影响原仓库数据：

```powershell
$taskRepoRoot = (Get-Location).Path
$taskCheckRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("task-tracker-manual-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $taskCheckRoot | Out-Null
Copy-Item -LiteralPath .\src -Destination $taskCheckRoot -Recurse
Set-Location -LiteralPath $taskCheckRoot
python .\src\main.py list
```

首次运行应显示“没有符合条件的任务”。本清单中的命令都在该临时目录执行，`python` 继续使用已激活的虚拟环境。

- `<ID>` 替换为本轮添加任务时输出的实际 ID，不要输入尖括号，也不要固定沿用上次的 ID。
- `<不存在的ID>` 替换为通过 `list` 确认不存在的整数。
- 每条命令都会启动新的 Python 进程，因此后续读取同时检查了持久化。
- 列表输出还可能包含其他任务，应核对目标任务，不能把“存在其他输出”误认为失败。

## 1. 正常操作流程

按顺序执行。在第 3 步标记完成之后、第 8 步删除之前，执行下一节的边界检查。

| 步骤 | 操作命令 | 预期结果 | 本轮复验 |
|---|---|---|---|
| 1 | `python .\src\main.py add "Day6 验收任务"` | 提示已添加，记录 `<ID>`；任务默认为 pending | 通过（隔离副本） |
| 2 | `python .\src\main.py list pending` | 包含新任务，显示 `[pending]` | 通过（隔离副本） |
| 3 | `python .\src\main.py complete <ID>` | 提示已标记完成 | 通过（隔离副本） |
| 4 | `python .\src\main.py update <ID> "Day6 验收任务已修改"` | 提示更新成功，ID 不变 | 通过（隔离副本） |
| 5 | `python .\src\main.py list completed` | 显示新标题，状态仍为 completed | 通过（隔离副本） |
| 6 | `python .\src\main.py list pending` | 不包含目标任务 | 通过（隔离副本） |
| 7 | `python .\src\main.py list` | 目标任务只出现一次，标题和状态正确 | 通过（隔离副本） |
| 8 | `python .\src\main.py delete <ID>` | 提示已删除该任务 | 通过（隔离副本） |
| 9 | `python .\src\main.py list` | 目标消失，其他任务保持不变；若没有其他任务则提示没有符合条件的任务 | 通过（隔离副本） |

用户已在原仓库手动跑通“添加 → pending → 完成 → 更新 → completed → pending → 删除 → 全部列表”的流程：验收任务 ID 为 2，结束后原任务 ID 1 仍保留。上表的本轮复验另行在隔离副本中执行。

## 2. 边界情况

在目标任务已完成但尚未删除时执行。对于拒绝的操作，应核对任务的标题、状态和列表内容保持不变；筛选和重复完成也不应保存数据。

| 场景 | 操作命令 | 预期结果 | 本轮复验 |
|---|---|---|---|
| complete 缺少 ID | `python .\src\main.py complete` | 提示 complete 命令需要任务 ID | 通过（隔离副本） |
| complete 使用非整数 ID | `python .\src\main.py complete abc` | 提示任务 ID 必须是整数 | 通过（隔离副本） |
| complete 使用不存在的 ID | `python .\src\main.py complete <不存在的ID>` | 提示未找到任务 | 通过（隔离副本） |
| update 缺少参数 | `python .\src\main.py update`，再执行 `python .\src\main.py update <ID>` | 两次均提示需要 ID 和新标题 | 通过（隔离副本） |
| update 使用非整数 ID | `python .\src\main.py update abc "新标题"` | 提示任务 ID 必须是整数 | 通过（隔离副本） |
| update 使用不存在的 ID | `python .\src\main.py update <不存在的ID> "新标题"` | 提示未找到任务 | 通过（隔离副本） |
| 更新为纯空白标题 | `python .\src\main.py update <ID> "   "` | 提示标题不能为空，原标题不变 | 通过（隔离副本） |
| 重复完成 | `python .\src\main.py complete <ID>` | 提示任务已完成，状态不变，不新增重复任务 | 通过（隔离副本） |
| 非法筛选条件 | `python .\src\main.py list abc` | 提示参数必须是 completed 或 pending | 通过（隔离副本） |
| 多余筛选参数 | `python .\src\main.py list pending extra` | 显示 list 的用法 | 通过（隔离副本） |
| 大写筛选条件 | `python .\src\main.py list COMPLETED` | 与小写 completed 的筛选结果一致 | 通过（隔离副本） |
| add 缺少标题 | `python .\src\main.py add` | 提示需要任务标题 | 通过（隔离副本） |
| add 使用纯空白标题 | `python .\src\main.py add "   "` | 提示标题不能为空，不新增任务 | 通过（隔离副本） |
| 未知命令 | `python .\src\main.py unknown` | 提示未知命令，可用命令包含 add、list、delete、complete、update | 通过（隔离副本） |

标题清理可在主流程第 4 步额外检查：将新标题两端加上空格，更新后再 `list completed`，标题两端应已清理，完成状态不变。随后恢复为第 4 步的标题再继续。

当前程序多数输入错误的退出码仍为 0；本节依据提示内容和数据是否改变判断结果，不以非零退出码作为所有失败场景的统一标准。

## 3. 文件与空结果检查

以下文件写入仅限准备步骤创建的临时副本。完成前两节并清理本轮验收任务后，再执行本节。不要将这些测试内容写入原仓库的任务文件。

| 场景 | 操作 | 预期结果 | 本轮复验 |
|---|---|---|---|
| 首次运行无数据文件 | 在全新副本执行 `python .\src\main.py list` | 空结果提示，不报错，也不生成数据文件 | 通过（隔离副本） |
| 删除最后一个任务 | 主流程结束后检查副本中的 `tasks.json`，再次执行 `list` | 文件内容为 `[]`，显示空结果提示 | 通过（隔离副本） |
| 有任务但无匹配项 | 只保留 pending 测试任务时执行 `list completed` | 空结果提示，原任务仍在 | 通过（隔离副本） |
| 旧任务缺少 completed | 使用下方旧数据夹具，执行 `list pending` | ID 7 的任务显示为 pending | 通过（隔离副本） |
| JSON 语法损坏 | 使用下方损坏夹具，执行 `list` 和 `add "不应写入"` | 两次均提示 JSON 文件已损坏，退出码 1；文件内容不变 | 通过（隔离副本） |

旧数据夹具（下面两行依次执行）：

```powershell
'[{"id":7,"title":"legacy task"}]' | Set-Content -LiteralPath .\tasks.json -Encoding ascii
python .\src\main.py list pending
```

这个夹具只有 ASCII 字符，因此指定 ASCII 编码，兼容 Windows PowerShell 5.1 和 PowerShell 7。也可执行 `list completed` 验证无匹配项的提示。

损坏数据夹具与验证：

```powershell
'{' | Set-Content -LiteralPath .\tasks.json -Encoding ascii
$taskBeforeHash = (Get-FileHash -LiteralPath .\tasks.json).Hash
python .\src\main.py list
$LASTEXITCODE
python .\src\main.py add "不应写入"
$LASTEXITCODE
(Get-FileHash -LiteralPath .\tasks.json).Hash -eq $taskBeforeHash
```

两次退出码应为 `1`，最后的文件哈希比较应为 `True`。这验证的是 JSON 语法损坏，不代表程序已经校验所有合法 JSON 的字段结构。

结束后返回原仓库：

```powershell
Set-Location -LiteralPath $taskRepoRoot
```

临时目录的路径保存在 `$taskCheckRoot` 中，不应提交到仓库。再次复验时重新执行准备步骤，创建新的空副本。

## 验收记录

- 用户手工验收：正常操作主流程已通过，验收任务已清理，原任务保持不变。
- 文档整理后的隔离复验：2026-09-04，助手使用当前源码副本、新建的 Python 3.13.5 虚拟环境逐条运行命令；正常流程、15 次 CLI 边界调用、标题清理、空结果、旧数据兼容和损坏 JSON 保护均通过。每条 CLI 命令使用独立进程，原仓库数据未修改。
- 格式检查：交付前执行 `git diff --check`；后续每次改动后重新检查。
- 本文件是手工验收清单，不是自动执行的 Python 测试文件。
