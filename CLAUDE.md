# CLAUDE.md

This file provides guidance to Claude Code when working with the pkgq project.

## Project Overview

pkgq (Package Query) is a Python module + CLI + MCP server + C3 plugin for finding, creating, and updating Python package documentation optimized for AI agents.

## Architecture

```
pkgq/
├── .claude-plugin/
│   └── plugin.json           # C3 plugin manifest
├── src/pkgq/
│   ├── __init__.py           # Package exports
│   ├── find.py               # Core find logic (cascade: cache → GitHub → PyPI)
│   ├── cli.py                # CLI entry point
│   └── mcp.py                # MCP server
├── skills/
│   ├── create/SKILL.md       # Generate PACKAGE.md for projects
│   └── update/SKILL.md       # Update package documentation
├── tests/
│   └── test_find.py          # Unit tests
├── PACKAGE.md                # This package's own docs
├── pyproject.toml            # Project configuration
└── Makefile                  # Build and install commands
```

## Components

### Python Module (`src/pkgq/`)

| Module | Purpose |
|--------|---------|
| `find.py` | Cascade lookup: cache → GitHub → PyPI |
| `cli.py` | CLI: `pkgq find <package>` |
| `mcp.py` | MCP server: `find_package` tool |

### Skills (`skills/`)

| Skill | Purpose |
|-------|---------|
| `create` | Generate PACKAGE.md for Python projects |
| `update` | Update documentation for new versions |

## Development Commands

```bash
# Install dependencies
make install

# Run tests
make test

# Run linter
make lint

# Build package
make build

# Publish to PyPI
make publish

# Install as C3 plugin
make plugin-install
```

## Usage

### CLI

```bash
# Find package documentation
pkgq find yoker

# Find with cache save
pkgq find yoker --save

# Find with version check
pkgq find yoker --from-version 0.3.0

# Verbose output
pkgq find yoker --verbose

# Manage cache
pkgq cache --list
pkgq cache --clear
```

### MCP Server

```bash
# Run MCP server
pkgq-mcp-server

# Or with uvx
uvx --from "pkgq[mcp]" pkgq-mcp-server
```

### Skills

```bash
# Generate PACKAGE.md for a project
/pkgq:create path=~/projects/my-package

# Update documentation for new version
/pkgq:update package=yoker from_version=0.3.0
```

## Cache Structure

```
~/.cache/pkgq/packages/
├── yoker/
│   ├── PACKAGE.md      # Package documentation
│   └── metadata.json   # Version and source info
└── roomz/
    ├── PACKAGE.md
    └── metadata.json
```

## MCP Configuration

In `.mcp.json`:

```json
{
  "mcpServers": {
    "pkgq": {
      "command": "uvx",
      "args": ["--from", "pkgq[mcp]", "pkgq-mcp-server"]
    }
  }
}
```

Tool name in agents: `mcp__plugin_c3_pkgq__find_package`

## Coding Standards

- Use two-space indentation
- Follow ruff linting rules
- Type hints with `X | None` syntax
- Run tests and lint before committing

## Publishing Checklist

1. Update version in `pyproject.toml` and `__init__.py`
2. Update `mcp.py` version
3. Run tests: `make test`
4. Run lint: `make lint`
5. Build: `make build`
6. Verify wheel: `unzip -l dist/*.whl`
7. Publish: `make publish`
8. Tag: `git tag v<version> && git push --tags`