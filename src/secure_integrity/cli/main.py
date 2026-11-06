import click
from pathlib import Path
from tqdm import tqdm
from rich.console import Console

from ..core.hasher import Hasher
from ..core.checker import IntegrityChecker
from ..storage.database import Database
from ..config.manager import ConfigManager
from ..reporting.reporter import Reporter

console = Console()

@click.group()
def cli():
    """Secure File Integrity Checker CLI"""
    pass

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--config', type=click.Path(exists=True), help="Path to YAML config file")
def baseline(path, config):
    """Create a hash baseline for the specified directory."""
    target_path = Path(path).resolve()
    config_mgr = ConfigManager(Path(config) if config else None)

    algorithm = config_mgr.get("algorithm")
    db_path = Path(config_mgr.get("db_path"))

    console.print(f"[bold blue]Creating baseline for:[/bold blue] {target_path}")
    console.print(f"[blue]Algorithm:[/blue] {algorithm}")

    hasher = Hasher(algorithm)
    checker = IntegrityChecker(hasher, config_mgr.get("excluded_dirs"), config_mgr.get("excluded_files"))
    db = Database(db_path)

    # Scan
    files = list(target_path.rglob("*"))
    results = {}
    for p in tqdm(files, desc="Hashing files", unit="file"):
        if p.is_file():
            # Use checker's internal logic for exclusions
            if any(part in checker.excluded_dirs for part in p.parts) or p.name in checker.excluded_files:
                continue

            rel_path = str(p.relative_to(target_path))
            try:
                file_hash = hasher.compute_hash(p)
                mtime = p.stat().st_mtime
                results[rel_path] = (file_hash, mtime)
            except (PermissionError, OSError):
                continue

    # Save to DB: (path, hash, algorithm, mtime)
    data_to_save = [
        (path, h[0], algorithm, h[1])
        for path, h in results.items()
    ]
    db.save_hashes(data_to_save)

    console.print(f"\n[bold green]✓ Baseline created successfully. Saved to {db_path}[/bold green]")
    console.print(f"Total files tracked: {len(results)}")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--config', type=click.Path(exists=True), help="Path to YAML config file")
def verify(path, config):
    """Verify the integrity of the specified directory against the baseline."""
    target_path = Path(path).resolve()
    config_mgr = ConfigManager(Path(config) if config else None)

    algorithm = config_mgr.get("algorithm")
    db_path = Path(config_mgr.get("db_path"))

    if not db_path.exists():
        console.print("[bold red]Error: Baseline database not found. Please run 'baseline' first.[/bold red]")
        return

    console.print(f"[bold blue]Verifying integrity for:[/bold blue] {target_path}")

    hasher = Hasher(algorithm)
    checker = IntegrityChecker(hasher, config_mgr.get("excluded_dirs"), config_mgr.get("excluded_files"))
    db = Database(db_path)
    reporter = Reporter()

    # Load baseline
    baseline_data = db.get_all_hashes()

    # Scan current
    files = list(target_path.rglob("*"))
    current_data = {}
    for p in tqdm(files, desc="Checking files", unit="file"):
        if p.is_file():
            if any(part in checker.excluded_dirs for part in p.parts) or p.name in checker.excluded_files:
                continue

            rel_path = str(p.relative_to(target_path))
            try:
                file_hash = hasher.compute_hash(p)
                mtime = p.stat().st_mtime
                current_data[rel_path] = (file_hash, mtime)
            except (PermissionError, OSError):
                continue

    # Compare
    changes, modified, added, removed = checker.verify(baseline_data, current_data)

    # Report
    reporter.report_summary(len(current_data), modified, added, removed)
    reporter.report_details(changes)

if __name__ == "__main__":
    cli()
