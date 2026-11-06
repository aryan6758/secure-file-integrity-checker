import pytest
from pathlib import Path
from src.secure_integrity.storage.database import Database

def test_database_save_and_load(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    test_data = [
        ("file1.txt", "hash1", "sha256", 12345.6),
        ("file2.txt", "hash2", "sha256", 67890.1),
    ]

    db.save_hashes(test_data)
    loaded = db.get_all_hashes()

    assert len(loaded) == 2
    assert loaded["file1.txt"] == ("hash1", "sha256", 12345.6)
    assert loaded["file2.txt"] == ("hash2", "sha256", 67890.1)

def test_database_update(tmp_path):
    db_path = tmp_path / "test.db"
    db = Database(db_path)

    db.save_hashes([("file1.txt", "hash1", "sha256", 100.0)])
    db.save_hashes([("file1.txt", "hash1_new", "sha256", 200.0)])

    loaded = db.get_all_hashes()
    assert loaded["file1.txt"][0] == "hash1_new"
    assert loaded["file1.txt"][2] == 200.0
