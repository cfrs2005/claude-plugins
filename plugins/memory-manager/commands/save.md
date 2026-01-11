---
description: "Save observation to SQLite memory database"
allowed-tools: "Read, Bash, Grep, Glob"
---

# Session Save Command

Persist observations to `~/.claude/memory.db` via SQLite.

## Usage

```bash
python3 storage/cli.py save \
  --project "<project-name>" \
  --type "<decision|change|discovery|task>" \
  --title "<short-title>" \
  --content "<detailed-content>" \
  --files "<comma-separated-paths>"
```

## Observation Types

| Type | When to Use |
|------|-------------|
| `decision` | 架构决策、技术选型 |
| `change` | 代码修改、文件变更 |
| `discovery` | 发现的问题、学到的知识 |
| `task` | 待办事项、未完成工作 |

## Execution Steps

1. **Identify Observation Type** - 根据当前工作判断类型
2. **Extract Key Info** - 提取标题和核心内容
3. **Call CLI** - 执行 Python 脚本写入数据库
4. **Confirm Result** - 检查返回的 JSON 状态
