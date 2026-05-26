# pkgq

[![PyPI](https://img.shields.io/pypi/v/pkgq.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/pkgq.svg)][pypi]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/christophevg/pkgq/test.yml.svg)][ci]
[![Coverage](https://img.shields.io/coveralls/github/christophevg/pkgq.svg)][coveralls]
[![License](https://img.shields.io/github/license/christophevg/pkgq.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
[![PACKAGE.md](https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet)](https://github.com/christophevg/pkgq#readme)
  
> Make your Python package discoverable for AI coding agents in 3 steps.

## What is PACKAGE.md?

**PACKAGE.md** is a informally proposed documentation standard for Python packages optimized for AI agents. Unlike README.md (written for humans), PACKAGE.md provides structured, scannable content that coding agents can quickly understand:

- **Purpose** - What the package does in one line
- **Key Components** - Classes, functions, and their signatures
- **Common Patterns** - Code examples for typical use cases
- **Migration Guides** - How to upgrade between versions

When you add PACKAGE.md to your repository root, coding agents using `pkgq` can instantly understand your package's capabilities.

## Quick Start for Package Authors

**3 steps to make your package discoverable:**

```bash
# 0. Add the marketplace (one-time setup)
claude plugin marketplace add christophevg/marketplace

# 1. Get the plugin
claude plugin install pkgq@christophe.vg

# 2. Generate documentation
/pkgq:create

# 3. Commit and push
git add PACKAGE.md && git commit -m "docs: add PACKAGE.md" && git push
```

Done! Your package is now discoverable by coding agents using the `pkgq` tool or MCP server.

**Add the badge to show your package supports AI agents:**

```markdown
[![PACKAGE.md](https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet)](https://github.com/christophevg/pkgq#readme)
```

## For Package Users

### Installation

```bash
pip install pkgq

# For MCP server support
pip install "pkgq[mcp]"
```

### Python Module

```python
from pkgq import find

# Find package documentation
result = find("yoker")
print(result.content)

# Check for updates
result = find("yoker", from_version="1.5.0")
```

### Command Line

```bash
% pkgq find yoker --save | head -15
Saved to: /Users/xtof/.cache/pkgq/packages/yoker
yoker 0.4.0 (cached)
Source: github:christophevg/yoker

                              Yoker

A Python agent harness with configurable tools and guardrails - one who yokes
agents together.

Overview

Yoker is a library-first, event-driven agent harness for Python that integrates
with Ollama. It provides a transparent, configurable runtime for AI agents with
structured tool execution, guardrails, and event emission. Unlike CLI-first
agent frameworks, Yoker is designed to be embedded in applications with full
visibility into agent operations.

% pkgq cache --list
Cached packages (3):
  pkgq 0.1.1 (pypi)
  roomz 0.2.0 (github:christophevg/roomz)
  yoker 0.4.0 (github:christophevg/yoker)
```

### MCP Server

```bash
pkgq-mcp-server
# Or: uvx --from "pkgq[mcp]" pkgq-mcp-server
```

## Features

| Feature | Description |
|---------|-------------|
| Cascade lookup | Cache → GitHub PACKAGE.md → PyPI |
| MCP server | Tool for Claude Code agents |
| Auto-caching | Results saved to `~/.cache/pkgq/packages/` |
| Plugin skills | `/pkgq:create` and `/pkgq:update` |

## Development

```bash
% git clone https://github.com/christophevg/pkgq.git
% cd pkgq
% uv sync --all-extras
% uv run pytest
```

## License

[MIT](LICENSE)

[pypi]: https://pypi.org/project/pkgq/
[uv]: https://docs.astral.sh/uv/
[ci]: https://github.com/christophevg/pkgq/actions
[coveralls]: https://coveralls.io/github/christophevg/pkgq
[license]: https://github.com/christophevg/pkgq/blob/main/LICENSE
