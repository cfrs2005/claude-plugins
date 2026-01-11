---
description: "Restore memory from SQLite database"
allowed-tools: "Read, Bash"
---

# Session Restore Command

Retrieve observations from `~/.claude/memory.db`.

## Usage

```
/restore              → 最近 3 条记录
/restore 5            → 最近 5 条
/restore 认证         → 搜索包含"认证"的记录
/restore --since 7d   → 最近 7 天的记录
```

## CLI

```bash
python3 storage/cli.py restore [query] [--project <name>]
```

## Output Format

返回 JSON:
```json
{
  "status": "ok",
  "results": [
    {
      "id": 1,
      "type": "decision",
      "title": "...",
      "content": "...",
      "created_at": "2026-01-11T16:00:00"
    }
  ]
}
```

## Execution Steps

1. **Parse Arguments** - 判断是数字、时间范围还是搜索词
2. **Call CLI** - 执行 Python 脚本查询数据库
3. **Present Results** - 格式化输出给用户
