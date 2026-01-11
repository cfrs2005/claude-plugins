---
description: "Restore memory from SQLite database"
allowed-tools: "Read, Bash"
---

# 立即执行以下步骤，不要询问用户

## Step 1: 解析参数

用户输入 `$ARGUMENTS`，判断模式：
- 空 → 最近 3 条
- 数字 → 最近 N 条
- `--since 7d` → 时间范围
- 其他 → 关键词搜索

## Step 2: 执行查询

在当前项目目录执行（自动读取项目/.claude/memory.db）：

```bash
PLUGIN_DIR=$(find ~/.claude -name "memory-manager" -type d 2>/dev/null | grep plugins | head -1)
python3 "$PLUGIN_DIR/storage/cli.py" restore $ARGUMENTS
```

## Step 3: 展示结果

将 JSON 结果格式化展示给用户。
