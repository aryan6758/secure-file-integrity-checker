import pytest
import os
from pathlib import Path
from src.secure_integrity.core.hasher import Hasher

def test_hasher_sha256(tmp_path):
    content = b"hello world"
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(content)

    hasher = Hasher("sha256")
    # Expected SHA256 for "hello world"
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert hasher.compute_hash(file_path) == expected

def test_hasher_blake3(tmp_path):
    content = b"hello world"
    file_path = tmp_path / "test.txt"
    file_path.write_bytes(content)

    hasher = Hasher("blake3")
    # Expected BLAKE3 for "hello world"
    expected = "d7497373573a6275940980f2b294e9404241c8f026669e3b65f76c6f31163785"
    assert hasher.compute_hash(file_path) == expected

def test_unsupported_algorithm():
    with pytest.raises(ValueError):
        Hasher("md5")
