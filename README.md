# Claude Plugins Marketplace

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)

> Claude Code 的持久化记忆系统，基于 SQLite + FTS5 全文搜索

## 特性

- **SQLite 存储** - 本地持久化，零外部依赖
- **全文搜索** - FTS5 索引，支持中文检索
- **智能检索** - 按数量、时间范围、关键词查询
- **原子化记忆** - decision / change / discovery / task 四种类型

## Installation

```bash
/plugin marketplace add https://github.com/cfrs2005/claude-plugins
/plugin install memory-manager
```

## 快速开始

### /save - 保存记忆

```bash
/save
```

自动分析当前会话，写入 `项目/.claude/memory.db`

### /restore - 恢复记忆

```
/restore              # 最近 3 条
/restore 5            # 最近 5 条
/restore 认证         # 搜索关键词
/restore --since 7d   # 最近 7 天
```

## 数据存储

数据库自动存储在项目根目录：

```
项目/.claude/memory.db
```

**项目根目录检测**：优先找 `.git`，其次找 `.claude-plugin`

## 架构

```
项目/.claude/memory.db      # 项目级 SQLite 数据库
├── sessions                # 会话元数据
├── observations            # 原子化记忆
└── observations_fts        # FTS5 全文索引
```

## 记忆类型

| Type | 用途 |
|------|------|
| `decision` | 架构决策、技术选型 |
| `change` | 代码修改、文件变更 |
| `discovery` | 发现的问题、学到的知识 |
| `task` | 待办事项、未完成工作 |

## License

MIT
