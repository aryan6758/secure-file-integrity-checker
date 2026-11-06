from rich.console import Console
from rich.table import Table
from typing import List, Dict

class Reporter:
    """Handles formatting and displaying verification results."""

    def __init__(self):
        self.console = Console()

    def report_summary(self, total: int, modified: int, added: int, removed: int):
        self.console.print("\n[bold]Verification Summary[/bold]")
        self.console.print(f"Total files scanned: {total}")
        self.console.print(f"[yellow]Modified:[/yellow] {modified}")
        self.console.print(f"[green]Added:[/green] {added}")
        self.console.print(f"[red]Removed:[/red] {removed}")

        if modified == 0 and added == 0 and removed == 0:
            self.console.print("\n[bold green]✓ All files intact. Integrity verified.[/bold green]")
        else:
            self.console.print("\n[bold red]⚠ Integrity violations detected![/bold red]")

    def report_details(self, changes: List[Dict]):
        if not changes:
            return

        table = Table(title="Integrity Change Details")
        table.add_column("File Path", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Details", style="white")

        for change in changes:
            table.add_row(
                change["path"],
                change["status"],
                change["details"]
            )

        self.console.print(table)
