# -*- coding: utf-8 -*-
"""
Data models for memory storage
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Session:
    """会话记录"""
    id: Optional[int] = None
    project: str = ""
    started_at: datetime = None
    summary: str = ""

    def __post_init__(self):
        if self.started_at is None:
            self.started_at = datetime.now()


@dataclass
class Observation:
    """原子化观察记录"""
    id: Optional[int] = None
    session_id: Optional[int] = None
    type: str = "discovery"  # decision, change, discovery, task
    title: str = ""
    content: str = ""
    files: str = ""  # 逗号分隔的文件路径
    created_at: datetime = None
    tokens: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if not self.tokens and self.content:
            # 粗略估算: 1 token ≈ 4 字符
            self.tokens = len(self.content) // 4
