# pkgq Version History

## 0.3.1 (2026-06-26)

### Bug Fixes

- **Package structure**: Fixed skills directory location in package
  - Skills now correctly packaged as `pkgq/skills/` instead of root level
  - Skills directory now properly included in distribution
  - Removed symlink confusion that caused incorrect package structure

---

## 0.3.0 (2026-06-26)

### New Features

- **Yoker plugin support**: pkgq can now be loaded as a yoker plugin
  - Exposes `find` tool for package documentation queries
  - Includes `create` and `update` skills for PACKAGE.md generation
  - Plugin manifest auto-discovered by yoker
- **Skills integration**: Skills moved into package for plugin distribution
  - `create` skill: Generate PACKAGE.md for Python projects
  - `update` skill: Update documentation for new versions
- **Module restructuring**: Added `plugin.py` module for yoker integration
  - Clean separation between core API and plugin interface
  - Mirrors existing `mcp.py` architecture pattern

### Breaking Changes

- **Skills location**: Skills moved from `skills/` to `src/pkgq/skills/`
  - Root `skills/` now a symlink for local development
  - Skills distributed with package when installed as yoker plugin

### Dependencies

- Added `yoker>=0.5.0` as required dependency
- Existing dependencies: httpx>=0.27.0, pydantic>=2.0.0, rich>=13.0.0

---

## 0.2.0 (2026-05-26)

### New Features

- Added plugin structure for Claude Code integration
- Added CI/CD with GitHub Actions
- Added PACKAGE.md for agent-ready documentation
- Added `save` parameter to MCP tool with auto-cache results

---

## 0.1.1 (2026-05-26)

## 0.1.1 (2026-05-26)

### New Features
- Added `save` parameter to MCP tool with auto-cache results
- Cascade lookup: cache → GitHub → PyPI
- CLI with `find` and `cache` commands
- MCP server for Claude Code integration
- Local caching at `~/.cache/pkgq/packages/`

### Bug Fixes
- Fixed license format and linter issues for PyPI compatibility

---

## 0.1.0 (2026-05-26)

### New Features
- Initial implementation of pkgq (package query)
- `find()` function to query Python package information
- `FindResult` dataclass for package information
- GitHub PACKAGE.md fetching
- PyPI documentation generation fallback