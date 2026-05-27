# pkgq Functional Analysis

## Executive Summary

pkgq (Package Query) is a Python module, CLI, MCP server, and C3 plugin ecosystem for finding, creating, and updating Python package documentation optimized for AI agents. The project is at version 0.2.0, published to PyPI, and implements a cascade lookup strategy (cache → GitHub → PyPI) to retrieve package information.

The project successfully delivers its core promise but has several areas for enhancement in error handling, testing coverage, feature completeness, and user experience.

## Current Capabilities

### Core Find Functionality

**Implemented:**
- Cascade lookup: cache → GitHub PACKAGE.md → PyPI fallback
- Cache management with configurable directory
- Version checking via `from_version` parameter
- Auto-generation of basic documentation from PyPI when PACKAGE.md not found

**Gaps:**
- No retry logic for transient network failures
- Limited error messages for common failure scenarios
- No rate limiting awareness for GitHub API
- No parallel fetching for performance optimization

### CLI Interface

**Implemented:**
- `pkgq find <package>` - Find package documentation
- `pkgq cache --list/--clear/--dir` - Cache management
- JSON output format (`--json`)
- Save to cache option (`--save`)
- Verbose mode (`--verbose`)

**Gaps:**
- No batch processing for multiple packages
- No output format options (only JSON and Markdown)
- No search/filter capabilities
- No offline mode indicator

### MCP Server

**Implemented:**
- Single tool: `find_package`
- Auto-save to cache by default
- Version checking support

**Gaps:**
- Single tool limits discoverability
- No cache management tools exposed
- No batch operations
- No package search tool

**Security Principle:**
MCP tools should only expose lookup and creational operations. Destructive actions (cache clear, delete, etc.) must not be exposed through MCP to prevent accidental or malicious data loss. This ensures that agents using the MCP server cannot inadvertently destroy cached data that may be valuable for other users or processes.

### Skills Ecosystem

**Implemented:**
- `/pkgq:create` - Generate PACKAGE.md for Python projects (documented but not implemented as executable skill)
- `/pkgq:update` - Update documentation for new versions (documented but not implemented as executable skill)

**Critical Gap:**
- Skills are documented as specifications but lack executable implementation
- Update skill describes features like HISTORY.md generation that don't exist in the core module
- No integration between skills and core find functionality

### Caching System

**Implemented:**
- File-based cache at `~/.cache/pkgq/packages/`
- Package directory structure with PACKAGE.md and metadata.json
- Environment variable configuration (`PKGQ_CACHE`)

**Gaps:**
- No cache expiration or staleness detection
- No cache size management
- No cache validation or integrity checks
- No offline-first mode

## Architecture Analysis

### Code Structure

```
src/pkgq/
├── __init__.py    # Clean exports, version management
├── find.py        # Core find logic (351 lines)
├── cli.py         # CLI entry point (139 lines)
└── mcp.py         # MCP server (69 lines)
```

**Strengths:**
- Clean separation of concerns
- Well-documented functions with docstrings
- Type hints throughout
- Modern Python (3.10+) with union syntax

**Weaknesses:**
- `find.py` handles too many responsibilities (cache, PyPI, GitHub, generation)
- No dedicated error types
- Limited logging/observability
- No async support despite async-friendly dependencies

### Dependencies

| Package | Version | Purpose | Notes |
|---------|---------|---------|-------|
| httpx | >=0.27.0 | HTTP client | Good choice, async-capable but not used |
| pydantic | >=2.0.0 | Data validation | Listed but not actively used |
| rich | >=13.0.0 | Terminal output | Used for CLI formatting |
| fastmcp | >=3.0.0 | MCP server | Optional, well-integrated |

**Observation:** pydantic is listed as a core dependency but the codebase uses dataclasses instead. This could be an opportunity for improved validation or should be moved to optional dependencies.

### Testing

**Current Coverage:**
- 4 test functions in `test_find.py`
- Tests cache directory configuration and basic cache checking
- No tests for:
  - Network operations (PyPI, GitHub)
  - Error handling
  - CLI commands
  - MCP server
  - Find cascade logic

**Coverage Gap:** The test coverage is minimal and doesn't exercise the core functionality.

### Error Handling

**Current State:**
- Basic HTTP error handling via `raise_for_status()`
- Generic exception catching in CLI
- No custom error types
- No structured error messages

**Impact:** Users receive unhelpful error messages like "Error: Invalid GitHub URL" without context on how to resolve the issue.

## Requirements Analysis

### Functional Requirements

**FR1: Package Discovery**
- Find package documentation from multiple sources
- Current: Implemented via cascade lookup
- Gap: No fallback hierarchy beyond GitHub/PyPI

**FR2: Cache Management**
- Store and retrieve cached documentation
- Current: Implemented with basic structure
- Gap: No staleness detection, no cleanup mechanism

**FR3: CLI Interface**
- Command-line access to all core features
- Current: Basic commands implemented
- Gap: Limited output formats, no batch operations

**FR4: MCP Integration**
- Expose functionality to MCP-compatible agents
- Current: Single tool implemented
- Gap: Limited tool set, no cache management tools

**FR5: Documentation Generation**
- Create PACKAGE.md for Python projects
- Current: Skill documented but not implemented
- Gap: No executable implementation

**FR6: Documentation Updates**
- Update documentation when new versions released
- Current: Skill documented but not implemented
- Gap: Version comparison, HISTORY.md generation not implemented

### Non-Functional Requirements

**NFR1: Performance**
- Fast lookups with caching
- Current: Acceptable for single packages
- Gap: No parallel fetching, no connection pooling configuration

**NFR2: Reliability**
- Graceful handling of network failures
- Current: Basic HTTP error handling
- Gap: No retry logic, no fallback on partial failures

**NFR3: Usability**
- Clear error messages and guidance
- Current: Generic errors
- Gap: Context-aware error messages with resolution hints

**NFR4: Maintainability**
- Well-tested, documented codebase
- Current: Good documentation, limited tests
- Gap: Test coverage < 50%, no integration tests

**NFR5: Security**
- Safe handling of external data
- Current: No validation of downloaded content
- Gap: No sanitization of markdown content, no GitHub token support

## Gap Analysis

### High Priority Gaps

1. **Skill Implementation**
   - The `/pkgq:create` and `/pkgq:update` skills are documented but not implemented
   - Users following the README instructions will encounter confusion
   - Impact: Core value proposition not fully delivered

2. **Test Coverage**
   - Minimal test coverage leaves core functionality untested
   - No tests for network operations, CLI, or MCP
   - Impact: Risk of regressions, difficult refactoring

3. **Error Handling**
   - Generic errors provide poor user experience
   - No guidance on resolving common issues
   - Impact: User frustration, support burden

### Medium Priority Gaps

4. **Cache Management**
   - No expiration or staleness detection
   - Cache can grow indefinitely
   - No validation of cached content

5. **Documentation Completeness**
   - HISTORY.md generation not implemented
   - Migration guide creation not implemented
   - Version comparison not fully realized

6. **API Rate Limiting**
   - GitHub API has rate limits (60/hour unauthenticated)
   - No rate limit awareness or handling
   - Could cause failures for heavy users

### Low Priority Gaps

7. **Async Support**
   - httpx supports async but code uses sync
   - No performance benefit for single package lookups
   - Would enable batch operations

8. **Output Formats**
   - Only JSON and Markdown supported
   - No YAML, TOML, or structured formats
   - Limits integration possibilities

9. **Offline Mode**
   - No explicit offline support
   - Cache exists but no offline-first flag
   - Could improve reliability

## Feature Recommendations

### Phase 1: Foundation (Stability)

1. **Implement Test Suite**
   - Unit tests for all core functions
   - Integration tests for CLI and MCP
   - Mocked network tests for reliability

2. **Error Handling Overhaul**
   - Custom exception types
   - Context-aware error messages
   - Retry logic for transient failures

3. **Documentation Sync**
   - Update README to reflect actual capabilities
   - Document limitations clearly
   - Add troubleshooting guide

### Phase 2: Feature Completion

4. **Implement `/pkgq:create` Skill**
   - Parse project structure
   - Extract metadata from pyproject.toml
   - Generate PACKAGE.md with key components

5. **Implement `/pkgq:update` Skill**
   - Fetch changelog from multiple sources
   - Generate HISTORY.md
   - Create migration guides

6. **Enhanced Cache Management**
   - Staleness detection (age-based)
   - Cache validation
   - Size limits and cleanup

### Phase 3: Enhancement

7. **Batch Operations**
   - Multi-package lookups
   - Bulk cache operations
   - Progress reporting

8. **GitHub API Integration**
   - Rate limit awareness
   - Optional authentication
   - Better repository discovery

9. **Additional Output Formats**
   - YAML output
   - TOML output
   - Structured JSON schema

### Phase 4: Advanced

10. **Version Intelligence**
    - Semantic version comparison
    - Dependency impact analysis
    - Upgrade recommendations

11. **Offline Mode**
    - Offline-first flag
    - Cache warmup command
    - Staleness indicators

12. **Async Architecture**
    - Async find operations
    - Parallel package fetching
    - Connection pooling

## Technical Debt

1. **Unused Dependency**
   - pydantic is declared but not used
   - Either implement or remove from dependencies

2. **Plugin Version Mismatch**
   - plugin.json shows 0.1.1, current version is 0.2.0
   - Should be kept in sync

3. **FindResult Serialization**
   - `to_dict()` method exists but not used for JSON output
   - Inconsistent serialization approach

4. **MCP Tool Naming**
   - Tool exposed as `mcp__plugin_c3_pkgq__find_package`
   - Should align with pkgq naming convention

## Success Metrics

### Current State
- PyPI package published and installable
- MCP server functional
- Basic caching working

### Target State (v1.0.0)
- 90%+ test coverage
- All documented features implemented
- Comprehensive error handling
- Clear upgrade/migration documentation

### Measurement Criteria
- Test coverage percentage
- User-reported issues (bug vs. documentation)
- Skill execution success rate
- Cache hit rate for repeated lookups