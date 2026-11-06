import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class Database:
    """Handles storage of file hashes in a SQLite database."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS file_hashes (
                    path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL,
                    algorithm TEXT NOT NULL,
                    last_modified REAL NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def save_hashes(self, hashes: List[Tuple[str, str, str, float]]):
        """Saves a list of file hashes: (path, hash, algorithm, mtime)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executemany(
                "INSERT OR REPLACE INTO file_hashes (path, hash, algorithm, last_modified) VALUES (?, ?, ?, ?)",
                hashes
            )
            conn.commit()

    def get_all_hashes(self) -> Dict[str, Tuple[str, str, float]]:
        """Returns a dictionary of {path: (hash, algorithm, mtime)}."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT path, hash, algorithm, last_modified FROM file_hashes")
            return {row[0]: (row[1], row[2], row[3]) for row in cursor.fetchall()}

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM file_hashes")
            conn.commit()
