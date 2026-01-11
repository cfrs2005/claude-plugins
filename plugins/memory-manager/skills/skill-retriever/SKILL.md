---
name: "skill-retriever"
description: "Search and retrieve skills from marketplace based on task context"
allowed-tools: "Read, Grep, Glob, WebFetch"
---

# Skill Retriever

Intelligent skill discovery and retrieval system.

## Capabilities

1. **Local Search** - scan installed skills
2. **Marketplace Query** - fetch from remote sources
3. **Context Matching** - recommend based on task

## Search Strategy

- Keyword match in skill names/descriptions
- Semantic similarity to current task
- Usage frequency ranking

## Output

Return matched skills with:
- Name and description
- Installation status
- Relevance score
