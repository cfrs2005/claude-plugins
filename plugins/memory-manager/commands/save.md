---
description: "Save current session to SQLite memory database"
allowed-tools: "Read, Bash, Grep, Glob"
---

# 立即执行以下步骤，不要询问用户

## Step 1: 分析当前会话

回顾本次对话中的关键内容：
- 做了什么决策？
- 修改了哪些文件？
- 发现了什么问题？
- 还有什么待办？

## Step 2: 获取项目名

```bash
basename $(git rev-parse --show-toplevel 2>/dev/null || pwd)
```

## Step 3: 写入数据库

找到插件目录，在**当前项目目录**执行（数据库会自动写入项目/.claude/memory.db）：

```bash
PLUGIN_DIR=$(find ~/.claude -name "memory-manager" -type d 2>/dev/null | grep plugins | head -1)
python3 "$PLUGIN_DIR/storage/cli.py" save \
  --project "<项目名>" \
  --type "<decision|change|discovery|task>" \
  --title "<简短标题>" \
  --content "<详细内容>"
```

## Step 4: 确认结果

检查返回的 JSON，向用户报告保存成功。
