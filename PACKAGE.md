# pkgq

> Find, create, and update Python package documentation for AI agents.

## Overview

pkgq (Package Query) is a Python module + CLI + MCP server for finding, creating, and
updating Python package documentation optimized for AI agents. It implements a cascade
lookup strategy: cache → GitHub → PyPI.

## Installation

```
pip install pkgq

# For MCP server support
pip install "pkgq[mcp]"
```

## Quick Start

```python
from pkgq import find

# Find package documentation
result = find("yoker")
print(result.content)

# Check for updates
result = find("yoker", from_version="1.5.0")

# Save to cache
result.save_to_cache()
```

## Key Components

### Classes

#### `FindResult`

Dataclass containing the result of a package find operation.

```python
from pkgq import FindResult

result = FindResult(
    package="yoker",
    version="1.5.0",
    source="github:christophevg/yoker",
    content="# yoker\n...",
    cached=False,
)

# Access properties
print(result.package)   # "yoker"
print(result.version)   # "1.5.0"
print(result.source)    # "github:christophevg/yoker"
print(result.cached)    # False

# Convert to dict
data = result.to_dict()

# Save to cache
result.save_to_cache()
```

### Functions

#### `find()`

Find package documentation using cascade lookup.

```python
from pkgq import find

# Basic lookup
result = find("yoker")

# With version check (returns cached if version matches)
result = find("yoker", from_version="1.5.0")

# Specific version
result = find("yoker", version="1.4.0")

# Custom cache directory
result = find("yoker", cache_dir=Path("/custom/cache"))

# Verbose mode (prints source information)
result = find("yoker", verbose=True)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `package` | `str` | required | Package name to find |
| `version` | `str \| None` | `None` | Desired version (default: latest) |
| `from_version` | `str \| None` | `None` | Current cached version (for update check) |
| `cache_dir` | `Path \| None` | `None` | Cache directory (default: `~/.cache/pkgq/packages`) |
| `verbose` | `bool` | `False` | Print source information during lookup |

#### `get_cache_dir()`

Get the cache directory path.

```python
from pkgq.find import get_cache_dir

cache_dir = get_cache_dir()  # ~/.cache/pkgq/packages
# Or set via PKGQ_CACHE environment variable
```

#### `check_cached()`

Check if package is cached locally.

```python
from pkgq.find import check_cached

result = check_cached("yoker")
if result:
    print(f"Found cached: {result.version}")
```

## Common Patterns

### CLI Usage

```bash
# Find package documentation
pkgq find yoker

# Find with version check
pkgq find yoker --from-version 1.5.0

# Save to cache
pkgq find yoker --save

# Output as JSON
pkgq find yoker --json

# Verbose output
pkgq find yoker --verbose

# Manage cache
pkgq cache --list
pkgq cache --clear
pkgq cache --dir
```

### MCP Server

```bash
# Run MCP server
pkgq-mcp-server

# Or with uvx
uvx --from "pkgq[mcp]" pkgq-mcp-server
```

The MCP server provides the `find_package` tool for Claude Code and other MCP-compatible agents.

### Environment Configuration

```bash
# Custom cache directory
export PKGQ_CACHE=/path/to/cache
```

## Dependencies

| Package | Purpose |
|---------|---------|
| `httpx>=0.27.0` | HTTP client for API requests |
| `pydantic>=2.0.0` | Data validation (optional, for future use) |
| `rich>=13.0.0` | Terminal output formatting |
| `fastmcp>=3.0.0` | MCP server implementation (optional, `[mcp]` extra) |

## Version Notes

**Current Version:** 0.1.1

### Recent Features

- Added `save` parameter to MCP tool with auto-cache results
- Fixed license format and linter issues for PyPI compatibility
- Initial implementation with cascade lookup (cache → GitHub → PyPI)

## Architecture

```
pkgq/
├── __init__.py    # Exports: find, FindResult
├── find.py        # Core find logic
├── cli.py         # CLI entry point
└── mcp.py         # MCP server
```

## Cache Structure

```
~/.cache/pkgq/packages/
├── {package}/
│   ├── PACKAGE.md    # Package documentation
│   └── metadata.json # Version and source info
```

## References

- [Homepage](https://github.com/christophevg/pkgq)
- [Documentation](https://github.com/christophevg/pkgq#readme)
- [Repository](https://github.com/christophevg/pkgq)
- [Issues](https://github.com/christophevg/pkgq/issues)