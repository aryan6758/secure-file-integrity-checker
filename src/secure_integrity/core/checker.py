from typing import List, Dict, Tuple
from pathlib import Path
from .hasher import Hasher

class IntegrityChecker:
    """Orchestrates the process of hashing and comparing files."""

    def __init__(self, hasher: Hasher, excluded_dirs: List[str], excluded_files: List[str]):
        self.hasher = hasher
        self.excluded_dirs = set(excluded_dirs)
        self.excluded_files = set(excluded_files)

    def scan_directory(self, root_path: Path) -> Dict[str, Tuple[str, float]]:
        """Scans a directory and computes hashes for all files."""
        results = {}
        for path in root_path.rglob("*"):
            if path.is_file():
                # Check if any parent directory is excluded
                if any(part in self.excluded_dirs for part in path.parts):
                    continue
                # Check if file name is excluded
                if path.name in self.excluded_files:
                    continue

                relative_path = str(path.relative_to(root_path))
                try:
                    file_hash = self.hasher.compute_hash(path)
                    mtime = path.stat().st_mtime
                    results[relative_path] = (file_hash, mtime)
                except (PermissionError, OSError) as e:
                    # We skip files we can't read but could log this in a real app
                    continue
        return results

    def verify(self, baseline: Dict[str, Tuple[str, str, float]], current: Dict[str, Tuple[str, float]]) -> Tuple[List[Dict], int, int, int]:
        """Compares current state against baseline."""
        changes = []
        modified = 0
        added = 0
        removed = 0

        # Check for modified and removed
        for path, (base_hash, alg, base_mtime) in baseline.items():
            if path not in current:
                changes.append({"path": path, "status": "REMOVED", "details": "File missing"})
                removed += 1
            else:
                curr_hash, curr_mtime = current[path]
                if curr_hash != base_hash:
                    changes.append({"path": path, "status": "MODIFIED", "details": f"Hash changed from {base_hash[:8]} to {curr_hash[:8]}"})
                    modified += 1

        # Check for added
        for path in current:
            if path not in baseline:
                changes.append({"path": path, "status": "ADDED", "details": "New file detected"})
                added += 1

        return changes, modified, added, removed
