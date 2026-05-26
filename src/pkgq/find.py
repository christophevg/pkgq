"""
Package Query - Find package documentation.

This module provides the find() function to query Python package information
from various sources (GitHub, PyPI, etc.).
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path

import httpx


@dataclass
class FindResult:
    """Result of a package find operation."""

    package: str
    version: str
    source: str
    content: str
    cached: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "package": self.package,
            "version": self.version,
            "source": self.source,
            "content": self.content,
            "cached": self.cached,
        }

    def save_to_cache(self, cache_dir: Path | None = None) -> Path:
        """Save result to cache directory."""
        if cache_dir is None:
            cache_dir = get_cache_dir()

        package_dir = cache_dir / self.package
        package_dir.mkdir(parents=True, exist_ok=True)

        # Save PACKAGE.md
        package_file = package_dir / "PACKAGE.md"
        package_file.write_text(self.content)

        # Save metadata
        metadata = {
            "package": self.package,
            "version": self.version,
            "source": self.source,
            "cached": True,
        }
        metadata_file = package_dir / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))

        return package_dir


def get_cache_dir() -> Path:
    """Get the cache directory for package information."""
    # Check environment variable first
    cache_env = os.environ.get("PKGQ_CACHE")
    if cache_env:
        return Path(cache_env)

    # Default to ~/.cache/pkgq/packages
    cache_dir = Path.home() / ".cache" / "pkgq" / "packages"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def check_cached(package: str, cache_dir: Path | None = None) -> FindResult | None:
    """Check if package is cached locally.

    Args:
        package: Package name
        cache_dir: Cache directory (default: ~/.cache/pkgq/packages)

    Returns:
        FindResult if cached, None if not
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    package_dir = cache_dir / package
    package_file = package_dir / "PACKAGE.md"
    metadata_file = package_dir / "metadata.json"

    if not package_file.exists():
        return None

    if not metadata_file.exists():
        return None

    try:
        metadata = json.loads(metadata_file.read_text())
        content = package_file.read_text()

        return FindResult(
            package=metadata["package"],
            version=metadata["version"],
            source=metadata["source"],
            content=content,
            cached=True,
        )
    except (json.JSONDecodeError, KeyError):
        return None


def get_pypi_info(package: str) -> dict:
    """Get package info from PyPI.

    Args:
        package: Package name

    Returns:
        Package metadata from PyPI
    """
    url = f"https://pypi.org/pypi/{package}/json"

    with httpx.Client() as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()


def extract_github_url(pypi_info: dict) -> str | None:
    """Extract GitHub URL from PyPI info.

    Args:
        pypi_info: PyPI package info

    Returns:
        GitHub URL or None
    """
    info = pypi_info.get("info", {})
    project_urls = info.get("project_urls") or {}

    # Check project_urls for GitHub
    for _key, url in project_urls.items():
        if "github.com" in url.lower():
            return url

    # Check home_page
    home_page = info.get("home_page", "")
    if "github.com" in home_page.lower():
        return home_page

    return None


def parse_github_url(url: str) -> tuple[str, str]:
    """Parse GitHub URL to owner and repo.

    Args:
        url: GitHub URL

    Returns:
        Tuple of (owner, repo)
    """
    # Handle various GitHub URL formats
    # https://github.com/owner/repo
    # https://github.com/owner/repo.git
    # https://github.com/owner/repo/
    # https://github.com/owner/repo#readme

    # Remove URL fragment (e.g., #readme)
    if "#" in url:
        url = url.split("#")[0]

    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]

    parts = url.split("/")
    if len(parts) >= 5 and "github.com" in parts[2]:
        return parts[3], parts[4]

    raise ValueError(f"Invalid GitHub URL: {url}")


def fetch_package_md_from_github(
    owner: str, repo: str, branch: str = "main"
) -> str | None:
    """Fetch PACKAGE.md from GitHub repository.

    Args:
        owner: Repository owner
        repo: Repository name
        branch: Branch name (default: main)

    Returns:
        PACKAGE.md content or None
    """
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/PACKAGE.md"

    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            return response.text
        return None


def get_default_branch(owner: str, repo: str) -> str:
    """Get default branch from GitHub API.

    Args:
        owner: Repository owner
        repo: Repository name

    Returns:
        Default branch name
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"

    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("default_branch", "main")
        return "main"


def find(
    package: str,
    version: str | None = None,
    from_version: str | None = None,
    cache_dir: Path | None = None,
    verbose: bool = False,
) -> FindResult:
    """Find package documentation.

    Queries multiple sources in order:
    1. Local cache (if from_version is provided)
    2. GitHub repository (PACKAGE.md)
    3. Generate from PyPI docs

    Args:
        package: Package name
        version: Desired version (default: latest)
        from_version: Current cached version (for update check)
        cache_dir: Cache directory (default: ~/.cache/pkgq/packages)
        verbose: Print source information during lookup

    Returns:
        FindResult with package information

    Raises:
        ValueError: If package not found
    """
    if cache_dir is None:
        cache_dir = get_cache_dir()

    # Step 1: Check local cache
    cached = check_cached(package, cache_dir)
    if cached and from_version:
        # Check if we need to update
        if cached.version == from_version:
            # Same version, return cached
            return cached
        # Different version, need to fetch
    elif cached and not from_version:
        # No version specified, use cached
        return cached

    # Step 2: Get PyPI info
    pypi_info = get_pypi_info(package)
    info = pypi_info.get("info", {})
    latest_version = info.get("version", "unknown")

    if version is None:
        version = latest_version

    # Step 3: Try GitHub
    github_url = extract_github_url(pypi_info)
    github_error = None
    if github_url:
        try:
            owner, repo = parse_github_url(github_url)
            default_branch = get_default_branch(owner, repo)

            # Try common branches
            branches_tried = []
            for branch in [default_branch, "main", "master"]:
                if branch in branches_tried:
                    continue
                branches_tried.append(branch)
                content = fetch_package_md_from_github(owner, repo, branch)
                if content:
                    if verbose:
                        print(f"Found PACKAGE.md on GitHub ({owner}/{repo}, branch: {branch})")
                    return FindResult(
                        package=package,
                        version=version,
                        source=f"github:{owner}/{repo}",
                        content=content,
                        cached=False,
                    )

            # GitHub URL found but no PACKAGE.md in any branch
            github_error = f"GitHub repo found ({owner}/{repo}) but no PACKAGE.md found in branches: {', '.join(branches_tried)}"
        except ValueError as e:
            github_error = f"Invalid GitHub URL: {e}"

    # Step 4: Generate basic info from PyPI
    if verbose and github_error:
        print(f"Warning: {github_error}")
        print("Falling back to PyPI-generated documentation")

    summary = info.get("summary", "No summary available")
    author = info.get("author", "Unknown")
    home_page = info.get("home_page", "")
    project_urls = info.get("project_urls") or {}

    content = f"""# {package}

> {summary}

## Overview

Package: **{package}**
Version: **{version}**
Author: **{author}**

## Installation

```
pip install {package}
```

## References

"""

    if home_page:
        content += f"- Homepage: {home_page}\n"

    for key, url in project_urls.items():
        content += f"- {key}: {url}\n"

    if github_error:
        content += f"\n---\n\n_Note: {github_error}_\n"

    return FindResult(
        package=package,
        version=version,
        source="pypi",
        content=content,
        cached=False,
    )
