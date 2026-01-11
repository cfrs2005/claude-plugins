# -*- coding: utf-8 -*-
"""
Database schema definition
"""

SCHEMA = """
-- ============================================================
-- Sessions: 会话元数据
-- ============================================================
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project TEXT NOT NULL,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    summary TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project);

-- ============================================================
-- Observations: 原子化记忆单元
-- ============================================================
CREATE TABLE IF NOT EXISTS observations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    type TEXT NOT NULL DEFAULT 'discovery',
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    files TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tokens INTEGER DEFAULT 0,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE INDEX IF NOT EXISTS idx_obs_session ON observations(session_id);
CREATE INDEX IF NOT EXISTS idx_obs_type ON observations(type);
CREATE INDEX IF NOT EXISTS idx_obs_created ON observations(created_at DESC);

-- FTS5 全文搜索
CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    title, content, files,
    content='observations',
    content_rowid='id'
);

-- 触发器: 同步 FTS 索引
CREATE TRIGGER IF NOT EXISTS obs_ai AFTER INSERT ON observations BEGIN
    INSERT INTO observations_fts(rowid, title, content, files)
    VALUES (new.id, new.title, new.content, new.files);
END;

CREATE TRIGGER IF NOT EXISTS obs_ad AFTER DELETE ON observations BEGIN
    INSERT INTO observations_fts(observations_fts, rowid, title, content, files)
    VALUES ('delete', old.id, old.title, old.content, old.files);
END;

CREATE TRIGGER IF NOT EXISTS obs_au AFTER UPDATE ON observations BEGIN
    INSERT INTO observations_fts(observations_fts, rowid, title, content, files)
    VALUES ('delete', old.id, old.title, old.content, old.files);
    INSERT INTO observations_fts(rowid, title, content, files)
    VALUES (new.id, new.title, new.content, new.files);
END;
"""
