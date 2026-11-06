import yaml
from pathlib import Path
from typing import Any, Dict

class ConfigManager:
    """Manages project configuration."""

    DEFAULT_CONFIG = {
        "algorithm": "sha256",
        "db_path": "integrity.db",
        "excluded_dirs": [".git", "__pycache__", "venv", ".venv"],
        "excluded_files": [".DS_Store", "thumbs.db"]
    }

    def __init__(self, config_path: Optional[Path] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        if config_path and config_path.exists():
            self.load_config(config_path)

    def load_config(self, path: Path):
        with open(path, "r") as f:
            user_config = yaml.safe_load(f) or {}
            self.config.update(user_config)

    def get(self, key: str) -> Any:
        return self.config.get(key)
