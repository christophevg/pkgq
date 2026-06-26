# pkgq

[![PyPI](https://img.shields.io/pypi/v/pkgq.svg)][pypi]
[![Python](https://img.shields.io/pypi/pyversions/pkgq.svg)][pypi]
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)][uv]
[![CI](https://img.shields.io/github/actions/workflow/status/christophevg/pkgq/test.yml.svg)][ci]
[![Coverage](https://img.shields.io/coveralls/github/christophevg/pkgq.svg)][coveralls]
[![License](https://img.shields.io/github/license/christophevg/pkgq.svg)][license]
[![Agentic](https://img.shields.io/badge/workflow-agentic-blueviolet?style=flat-square)](https://christophe.vg/about/Agentic-Workflow)
[![PACKAGE.md](https://img.shields.io/badge/pkgq-PACKAGE.md-blueviolet)](https://github.com/christophevg/pkgq#readme)
[![yoker](https://img.shields.io/badge/yoker-plugin-blueviolet)](https://github.com/christophevg/yoker#readme)
  
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
  pkgq 0.3.2 (pypi)
  roomz 0.2.0 (github:christophevg/roomz)
  yoker 0.5.0 (github:christophevg/yoker)
```

### Yoker Tool

When you're using yoker as your agent harness, you can simply include the pkgq package in your environment and ask yoker to load it as a plugin...

```console
% uvx --with pkgq yoker --with pkgq

╭───────────────────────────────── Plugin: pkgq ──────────────────────────────────╮
│ Plugin: pkgq                                                                    │
│                                                                                 │
│ Tools:     pkgq:find                                                            │
│ Skills:    pkgq:create, pkgq:update                                             │
│ Agents:    (none)                                                               │
│                                                                                 │
│ Plugins can execute code on your system.                                        │
│ Only load plugins you trust.                                                    │
│                                                                                 │
│ Load this plugin? [y/N]:                                                        │
╰─────────────────────────────────────────────────────────────────────────────────╯

y

To trust this plugin permanently, add to your yoker.toml:

  [plugins.trusted]
  pkgq = true

╭───────────────────────────────── 👋 Welcome... ─────────────────────────────────╮
│ Yoker v0.4.0 - Using model: kimi-k2.7-code:cloud                                │
│ Harness: yoker v1.0                                                             │
│ Thinking mode: enabled (use /think on|off|silent to toggle)                     │
│ Agent: default - The default/minimal Yoker agent.                               │
│ Type /help for available commands.                                              │
│ Press Ctrl+D (or Ctrl+Z on Windows) to quit.                                    │
╰─────────────────────────────────────────────────────────────────────────────────╯

> use the pkgq find tool to get information on pkgq
  The user wants me to use the pkgq find tool to get information on pkgq. I should
  use the pkgq__find function with package="pkgq".

⏺ Pkgq:find tool: pkgq  ✓ Success
  I got the information from the pkgq find tool. Let me summarize this for the user
  in a helpful way.

  Here is the information for **pkgq** using the pkgq find tool:

  ## pkgq — Package Query

  - **Version:** 0.1.1
  - **Author:** None listed
  - **Description:** Package Query - Find API information for Python packages
  - **Install command:**
    pip install pkgq
```

### MCP Server

```bash
pkgq-mcp-server
# Or: uvx --from "pkgq[mcp]" pkgq-mcp-server
```

So If you want to load it into your project, create a `.mcp.json` file:

```json
{
  "mcpServers": {
    "pkgq": {
      "command": "uvx",
      "args": [
        "--from",
        "pkgq[mcp]",
        "pkgq-mcp-server"
      ]
    }
  }
}
```

When you start your MCP-based coding harness, e.g. Claude Code, you'll be prompted for confirmation to use the new MCP server:

```
────────────────────────────────────────────────────────────────────────────────────
  New MCP server found in this project: pkgq

  MCP servers may execute code or access system resources. All tool calls require
  approval. Learn more in the MCP documentation.

  ❯ 1. Use this MCP server
    2. Use this and all future MCP servers in this project
    3. Continue without using this MCP server

  Enter to confirm · Esc to cancel
  ```

And you can use it:

```
❯ use the find_pacakge tool to find information about pkgq

⏺ Thinking for 2s, calling plugin:c3:pkgq…

────────────────────────────────────────────────────────────────────────────────────
 Tool use

   plugin:c3:pkgq - find_package(package: "pkgq") (MCP)
   Find package documentation.

   Queries multiple sources in order:…

 Do you want to proceed?
 ❯ 1. Yes
   2. Yes, and don't ask again for plugin:c3:pkgq - find_package commands in /Users/xtof/Workspace/agentic/pkgq
   3. No

 Esc to cancel · Tab to amend


 pkgq Package Information
 
 Version: 0.1.1 (cached)
 Source: PyPI
 
 Overview
 
 pkgq (Package Query) is a tool for finding API information for Python packages.
 ...
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

