"""
pkgq CLI - Command line interface for package query.
"""

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown

from pkgq import find
from pkgq.find import get_cache_dir


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="pkgq",
        description="Package Query - Find API information for Python packages",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # find command
    find_parser = subparsers.add_parser("find", help="Find package documentation")
    find_parser.add_argument("package", help="Package name")
    find_parser.add_argument(
        "--version", "-v", help="Desired version (default: latest)"
    )
    find_parser.add_argument(
        "--from-version", "-f", help="Current cached version (for update check)"
    )
    find_parser.add_argument(
        "--cache-dir", "-c", type=Path, help="Cache directory"
    )
    find_parser.add_argument(
        "--save", "-s", action="store_true", help="Save to cache"
    )
    find_parser.add_argument(
        "--json", "-j", action="store_true", help="Output as JSON"
    )
    find_parser.add_argument(
        "--verbose", "-V", action="store_true", help="Verbose output"
    )

    # cache command
    cache_parser = subparsers.add_parser("cache", help="Manage cache")
    cache_parser.add_argument(
        "--clear", action="store_true", help="Clear cache"
    )
    cache_parser.add_argument(
        "--list", action="store_true", help="List cached packages"
    )
    cache_parser.add_argument(
        "--dir", action="store_true", help="Show cache directory"
    )

    args = parser.parse_args()

    if args.command == "find":
        cmd_find(args)
    elif args.command == "cache":
        cmd_cache(args)
    else:
        parser.print_help()
        sys.exit(1)


def cmd_find(args):
    """Handle find command."""
    console = Console()

    try:
        result = find(
            package=args.package,
            version=args.version,
            from_version=args.from_version,
            cache_dir=args.cache_dir,
            verbose=args.verbose,
        )

        if args.save:
            cache_path = result.save_to_cache(args.cache_dir)
            console.print(f"[green]Saved to:[/green] {cache_path}")

        if args.json:
            print(json.dumps(result.to_dict(), indent=2))
        else:
            # Print version info
            status = "[green]cached[/green]" if result.cached else "[blue]fetched[/blue]"
            console.print(f"[bold]{result.package}[/bold] {result.version} ({status})")
            console.print(f"[dim]Source: {result.source}[/dim]")
            console.print()

            # Print content as markdown
            md = Markdown(result.content)
            console.print(md)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


def cmd_cache(args):
    """Handle cache command."""
    console = Console()
    cache_dir = get_cache_dir()

    if args.dir:
        console.print(str(cache_dir))
        return

    if args.clear:
        import shutil
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
            console.print(f"[green]Cleared cache:[/green] {cache_dir}")
        else:
            console.print("[yellow]Cache is empty[/yellow]")
        return

    if args.list:
        if not cache_dir.exists():
            console.print("[yellow]Cache is empty[/yellow]")
            return

        packages = sorted(cache_dir.iterdir())
        if not packages:
            console.print("[yellow]Cache is empty[/yellow]")
            return

        console.print(f"[bold]Cached packages ({len(packages)}):[/bold]")
        for pkg_dir in packages:
            metadata_file = pkg_dir / "metadata.json"
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text())
                version = metadata.get("version", "?")
                source = metadata.get("source", "?")
                console.print(f"  {pkg_dir.name} {version} ({source})")
            else:
                console.print(f"  {pkg_dir.name} (no metadata)")
        return

    # Default: show cache info
    console.print(f"Cache directory: {cache_dir}")
    if cache_dir.exists():
        packages = list(cache_dir.iterdir())
        console.print(f"Cached packages: {len(packages)}")
    else:
        console.print("Cache is empty")


if __name__ == "__main__":
    main()