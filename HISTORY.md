# pkgq Version History

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