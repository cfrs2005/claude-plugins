#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Manager CLI
Usage:
    python cli.py save --project <name> --type <type> --title <title> --content <content>
    python cli.py restore [args]
"""

import sys
import json
from pathlib import Path

# 确保能找到同级模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.db import MemoryDB
from storage.models import Observation


def cmd_save(args: dict):
    """保存观察记录"""
    db = MemoryDB()

    project = args.get("project", "unknown")
    session_id = db.get_current_session(project)
    if not session_id:
        session_id = db.create_session(project)

    obs = Observation(
        session_id=session_id,
        type=args.get("type", "discovery"),
        title=args.get("title", ""),
        content=args.get("content", ""),
        files=args.get("files", "")
    )

    obs_id = db.add_observation(obs)
    print(json.dumps({"status": "ok", "id": obs_id}))


def cmd_restore(args: str, project: str = None):
    """恢复记忆，支持多种模式"""
    db = MemoryDB()

    if not args:
        results = db.get_recent(3, project)
    elif args.isdigit():
        results = db.get_recent(int(args), project)
    elif args.startswith("--since"):
        duration = args.split()[1] if len(args.split()) > 1 else "7d"
        results = db.get_since(duration, project)
    else:
        results = db.search(args)

    output = [format_observation(obs) for obs in results]
    print(json.dumps({"status": "ok", "results": output}))


def format_observation(obs: Observation) -> dict:
    return {
        "id": obs.id,
        "type": obs.type,
        "title": obs.title,
        "content": obs.content,
        "files": obs.files,
        "created_at": obs.created_at.isoformat(),
        "tokens": obs.tokens
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: cli.py <save|restore> [args]"}))
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "save":
        args = parse_save_args(sys.argv[2:])
        cmd_save(args)
    elif cmd == "restore":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        project = None
        if "--project" in sys.argv:
            idx = sys.argv.index("--project")
            project = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None
            query = query.replace(f"--project {project}", "").strip()
        cmd_restore(query, project)
    else:
        print(json.dumps({"error": f"Unknown command: {cmd}"}))
        sys.exit(1)


def parse_save_args(argv: list) -> dict:
    """解析 save 命令参数"""
    args = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            i += 1
    return args


if __name__ == "__main__":
    main()
