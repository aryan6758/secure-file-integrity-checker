import hashlib
from pathlib import Path
from typing import Union
import blake3

class Hasher:
    """Handles cryptographic hashing of files."""

    SUPPORTED_ALGORITHMS = {
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "blake3": blake3.blake3
    }

    def __init__(self, algorithm: str = "sha256"):
        if algorithm not in self.SUPPORTED_ALGORITHMS:
            raise ValueError(f"Unsupported algorithm. Choose from: {list(self.SUPPORTED_ALGORITHMS.keys())}")
        self.algorithm_name = algorithm
        self.hash_func = self.SUPPORTED_ALGORITHMS[algorithm]

    def compute_hash(self, file_path: Union[str, Path]) -> str:
        """Computes the hash of a file in chunks to handle large files efficiently."""
        hasher = self.hash_func()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
