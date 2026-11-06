import pytest
from src.secure_integrity.core.checker import IntegrityChecker
from src.secure_integrity.core.hasher import Hasher

def test_checker_verify_no_changes():
    hasher = Hasher("sha256")
    checker = IntegrityChecker(hasher, [], [])

    baseline = {"f1.txt": ("hash1", "sha256", 10.0)}
    current = {"f1.txt": ("hash1", 10.0)}

    changes, mod, add, rem = checker.verify(baseline, current)
    assert len(changes) == 0
    assert mod == 0 and add == 0 and rem == 0

def test_checker_verify_modified():
    hasher = Hasher("sha256")
    checker = IntegrityChecker(hasher, [], [])

    baseline = {"f1.txt": ("hash1", "sha256", 10.0)}
    current = {"f1.txt": ("hash2", 11.0)}

    changes, mod, add, rem = checker.verify(baseline, current)
    assert len(changes) == 1
    assert changes[0]["status"] == "MODIFIED"
    assert mod == 1

def test_checker_verify_added():
    hasher = Hasher("sha256")
    checker = IntegrityChecker(hasher, [], [])

    baseline = {"f1.txt": ("hash1", "sha256", 10.0)}
    current = {"f1.txt": ("hash1", 10.0), "f2.txt": ("hash2", 12.0)}

    changes, mod, add, rem = checker.verify(baseline, current)
    assert len(changes) == 1
    assert changes[0]["status"] == "ADDED"
    assert add == 1

def test_checker_verify_removed():
    hasher = Hasher("sha256")
    checker = IntegrityChecker(hasher, [], [])

    baseline = {"f1.txt": ("hash1", "sha256", 10.0), "f2.txt": ("hash2", "sha256", 11.0)}
    current = {"f1.txt": ("hash1", 10.0)}

    changes, mod, add, rem = checker.verify(baseline, current)
    assert len(changes) == 1
    assert changes[0]["status"] == "REMOVED"
    assert rem == 1
