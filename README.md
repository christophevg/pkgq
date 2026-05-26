# pkgq

**PacKaGe Query** - Find API information for Python packages.

A fast, agent-friendly tool for discovering Python package documentation, capabilities, and migration guides.

## Installation

```bash
# Install with uv
uv add pkgq

# Or with pip
pip install pkgq

# For MCP server support
uv add "pkgq[mcp]"
```

## Usage

### Python Module

```python
from pkgq import find

# Find package documentation
result = find("yoker")
print(result.content)

# Find specific version
result = find("yoker", version="2.1.0")

# Check for updates
result = find("yoker", from_version="1.5.0")
if result.version != "1.5.0":
    print(f"Update available: {result.version}")

# Save to cache
result.save_to_cache()
```

### Command Line

```bash
# Find package documentation
pkgq find yoker

# Find specific version
pkgq find yoker --version 2.1.0

# Check for updates
pkgq find yoker --from-version 1.5.0

# Save to cache
pkgq find yoker --save

# Output as JSON
pkgq find yoker --json

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
uvx --from pkgq pkgq-mcp-server
```

The MCP server provides a `find_package` tool for use with Claude Code and other MCP-compatible agents.

## Cache

Package documentation is cached locally:

- Default: `~/.cache/pkgq/packages/`
- Custom: Set `PKGQ_CACHE` environment variable

Cache structure:
```
~/.cache/pkgq/packages/
├── yoker/
│   ├── PACKAGE.md      # Package documentation
│   └── metadata.json   # Version and source info
└── roomz/
    ├── PACKAGE.md
    └── metadata.json
```

## Development

```bash
# Clone repository
git clone https://github.com/christophevg/pkgq.git
cd pkgq

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run linter
uv run ruff check src/

# Run MCP server
uv run pkgq-mcp-server
```

## License

MIT License - See [LICENSE](LICENSE) for details.