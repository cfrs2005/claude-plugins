---
name: "context-memory"
description: "Automatic session context persistence - saves project state, decisions, and pending work"
allowed-tools: "Read, Write, Bash, Grep, Glob"
---

# Context Memory Skill

Automatically manage session memory for seamless context restoration.

## When to Activate

- Session ending or user requests save
- Major milestone completed
- Before switching tasks

## Memory Structure

Store in `.context_memory.md`:

1. **Project snapshot** - key files and structure
2. **Change log** - what was modified
3. **Decision record** - architectural choices
4. **Task queue** - pending and blocked items
5. **Skill cache** - retrieved skills this session

## Persistence Strategy

- Overwrite on save (not append)
- Create backup before overwrite
- Validate file integrity after write
