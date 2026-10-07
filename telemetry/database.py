import sqlite3
from typing import List, Optional
from .models import ValidValue, InvalidValue, TrendValue

class Database:
    def __init__(self, path: str = ":memory:"):
        self.path = path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA journal_mode = DELETE")
        self._create_tables()

    def close(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                object_name TEXT NOT NULL,
                value TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                trend_name TEXT NOT NULL,
                value REAL NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS invalid_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                object_name TEXT NOT NULL,
                value TEXT NOT NULL,
                reason TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save_valid(self, values: List[ValidValue]):
        cur = self.conn.cursor()
        cur.executemany(
            "INSERT INTO raw_values (timestamp, object_name, value) VALUES (?, ?, ?)",
            [(v.timestamp, v.object_name, str(v.value)) for v in values],
        )
        self.conn.commit()

    def save_invalid(self, values: List[InvalidValue]):
        cur = self.conn.cursor()
        cur.executemany(
            "INSERT INTO invalid_values (timestamp, object_name, value, reason) VALUES (?, ?, ?, ?)",
            [(v.timestamp, v.object_name, str(v.value), v.reason) for v in values],
        )
        self.conn.commit()

    def save_trend(self, trend: TrendValue):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO trends (timestamp, trend_name, value) VALUES (?, ?, ?)",
            (trend.timestamp, trend.trend_name, trend.value),
        )
        self.conn.commit()

    def count_raw_values(self) -> int:
        cur = self.conn.cursor()
        return cur.execute("SELECT COUNT(*) FROM raw_values").fetchone()[0]

    def count_invalid_values(self) -> int:
        cur = self.conn.cursor()
        return cur.execute("SELECT COUNT(*) FROM invalid_values").fetchone()[0]

    def count_trends(self) -> int:
        cur = self.conn.cursor()
        return cur.execute("SELECT COUNT(*) FROM trends").fetchone()[0]