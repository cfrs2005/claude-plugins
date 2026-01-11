# -*- coding: utf-8 -*-
"""
SQLite database connection and schema management
"""

import sqlite3
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta

from .schema import SCHEMA
from .models import Session, Observation


def find_project_root() -> Path:
    """向上查找项目根目录（优先 .git）"""
    cwd = Path.cwd()

    # 优先找 .git
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".git").exists():
            return parent

    # 其次找 .claude-plugin
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".claude-plugin").exists():
            return parent

    return cwd


def get_default_db_path() -> Path:
    """获取项目级数据库路径"""
    root = find_project_root()
    return root / ".claude" / "memory.db"


class MemoryDB:
    """SQLite 数据库管理器"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or get_default_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            self._init_schema()
        return self._conn

    def _init_schema(self):
        """初始化数据库表结构"""
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    # ========================================
    # Session CRUD
    # ========================================

    def create_session(self, project: str, summary: str = "") -> int:
        cur = self.conn.execute(
            "INSERT INTO sessions (project, summary) VALUES (?, ?)",
            (project, summary)
        )
        self.conn.commit()
        return cur.lastrowid

    def get_current_session(self, project: str) -> Optional[int]:
        """获取当前项目最近的 session_id"""
        row = self.conn.execute(
            "SELECT id FROM sessions WHERE project = ? ORDER BY id DESC LIMIT 1",
            (project,)
        ).fetchone()
        return row["id"] if row else None

    # ========================================
    # Observation CRUD
    # ========================================

    def add_observation(self, obs: Observation) -> int:
        cur = self.conn.execute(
            """INSERT INTO observations
               (session_id, type, title, content, files, tokens)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (obs.session_id, obs.type, obs.title,
             obs.content, obs.files, obs.tokens)
        )
        self.conn.commit()
        return cur.lastrowid

    def get_recent(self, limit: int = 3, project: str = None) -> List[Observation]:
        """获取最近 N 条记录"""
        if project:
            rows = self.conn.execute(
                """SELECT o.* FROM observations o
                   JOIN sessions s ON o.session_id = s.id
                   WHERE s.project = ?
                   ORDER BY o.created_at DESC LIMIT ?""",
                (project, limit)
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM observations ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        return [self._row_to_obs(r) for r in rows]

    def search(self, query: str, limit: int = 10) -> List[Observation]:
        """FTS5 全文搜索，自动添加通配符支持中文"""
        # 为每个词添加通配符
        terms = query.strip().split()
        fts_query = " OR ".join(f'"{t}"*' for t in terms) if terms else query

        rows = self.conn.execute(
            """SELECT o.* FROM observations o
               JOIN observations_fts fts ON o.id = fts.rowid
               WHERE observations_fts MATCH ?
               ORDER BY rank LIMIT ?""",
            (fts_query, limit)
        ).fetchall()
        return [self._row_to_obs(r) for r in rows]

    def get_since(self, duration: str, project: str = None) -> List[Observation]:
        """获取指定时间范围内的记录，如 '7d', '24h'"""
        delta = self._parse_duration(duration)
        since = datetime.now() - delta

        if project:
            rows = self.conn.execute(
                """SELECT o.* FROM observations o
                   JOIN sessions s ON o.session_id = s.id
                   WHERE s.project = ? AND o.created_at >= ?
                   ORDER BY o.created_at DESC""",
                (project, since.isoformat())
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM observations WHERE created_at >= ? ORDER BY created_at DESC",
                (since.isoformat(),)
            ).fetchall()
        return [self._row_to_obs(r) for r in rows]

    # ========================================
    # Helper Methods
    # ========================================

    def _row_to_obs(self, row: sqlite3.Row) -> Observation:
        return Observation(
            id=row["id"],
            session_id=row["session_id"],
            type=row["type"],
            title=row["title"],
            content=row["content"],
            files=row["files"],
            created_at=datetime.fromisoformat(row["created_at"]),
            tokens=row["tokens"]
        )

    @staticmethod
    def _parse_duration(duration: str) -> timedelta:
        """解析时间字符串: 7d, 24h, 30m"""
        unit = duration[-1].lower()
        value = int(duration[:-1])
        if unit == "d":
            return timedelta(days=value)
        if unit == "h":
            return timedelta(hours=value)
        if unit == "m":
            return timedelta(minutes=value)
        raise ValueError(f"Unknown duration format: {duration}")
