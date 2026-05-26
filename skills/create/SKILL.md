---
name: create
description: |
  Generate a PACKAGE.md file for a Python project. Analyzes the project structure,
  extracts key components, patterns, and creates agent-ready documentation.
  Use when creating documentation for your own packages.
---

# Package Documentation Generator

Creates PACKAGE.md files for Python packages, following the PACKAGE.md specification.

## When to Use

- You've created a new Python package
- You want to document your package for AI agents
- You're preparing a release and documentation needs updating

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| path | No | Project path (defaults to current directory) |
| output | No | Output path (defaults to PACKAGE.md in project root) |

## Process

### 1. Gather Project Metadata

Read project configuration:

```
pyproject.toml
├── [project]
│   ├── name
│   ├── version
│   ├── description
│   ├── dependencies
│   └── urls
├── [project.optional-dependencies]
└── [project.readme]
```

If `pyproject.toml` missing, check:
- `setup.py` (legacy)
- `setup.cfg` (legacy)
- `requirements.txt` (minimal)

### 2. Analyze Source Structure

Scan the package source:

```
src/{package}/
├── __init__.py      # Exports, version
├── {module}.py      # Key functions, classes
└── {submodule}/     # Nested modules
```

Or:

```
{package}/
├── __init__.py
├── {module}.py
└── ...
```

**Extract:**
- Package name from `__init__.py` or `pyproject.toml`
- Key classes (look for `class` definitions)
- Key functions (look for `def` at module level)
- Entry points (`__all__`, `__main__.py`)

### 3. Extract Patterns from Tests

Scan test files for usage patterns:

```
tests/
├── test_{module}.py
└── ...
```

**Extract:**
- Import patterns
- Initialization patterns
- Common usage sequences
- Configuration examples

### 4. Read Existing Documentation

Read for context:

- `README.md` - Human documentation
- `AGENTS.md` / `CLAUDE.md` - Development instructions
- `docs/` - Full documentation (if exists)

**Extract:**
- Purpose statement
- Quick start example
- Configuration options
- Known issues/limitations

### 5. Check for Changelog

Look for version history:

- `CHANGELOG.md`
- `HISTORY.md`
- `NEWS.md`
- GitHub releases
- Git tags

### 6. Generate PACKAGE.md

Create the documentation file:

```markdown
# {Package Name}

> {One-line description from pyproject.toml or README}

## Overview

{Extended description from README}

## Installation

\`\`\`
pip install {package}
\`\`\`

## Quick Start

{Minimal example from tests or README}

## Key Components

{Extracted from source analysis}

### Classes

#### `{ClassName}`

{Purpose inferred from docstring or usage}

\`\`\`python
{Usage example from tests}
\`\`\`

## Common Patterns

{Extracted from tests}

## Dependencies

{From pyproject.toml}

## Version Notes

{Current version from pyproject.toml}

## References

{Links from pyproject.toml project.urls}
```

### 7. Generate HISTORY.md

If changelog information available:

```markdown
# {Package} Version History

## {Current Version} ({Date})

### New Features
- {From changelog}

### Breaking Changes
- {From changelog}

---

{Previous versions}
```

## Output

Creates two files:

1. **PACKAGE.md** - Agent-ready documentation
2. **HISTORY.md** - Version history (if version info available)

## Example Usage

```bash
# Generate for current project
/pkgq:create

# Generate for specific project
/pkgq:create path=~/projects/my-package

# Specify output location
/pkgq:create output=docs/PACKAGE.md
```

## Quality Checks

After generation, verify:

- [ ] Purpose statement is clear
- [ ] Quick Start example works
- [ ] Key components are documented
- [ ] Common patterns cover 80% use cases
- [ ] Dependencies are accurate
- [ ] References links are correct

## Customization

The generated PACKAGE.md may need manual refinement:

1. **Review purpose** - Is it accurate?
2. **Refine Quick Start** - Is it minimal and working?
3. **Add patterns** - Are common use cases covered?
4. **Update migration guides** - Are breaking changes documented?

## Notes

- Works best with well-structured Python packages
- Legacy packages (setup.py only) have limited metadata extraction
- Private packages (not on PyPI) should use this skill
- Always review generated documentation before publishing