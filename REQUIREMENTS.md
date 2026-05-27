# Requirements

## Functional Requirements

### Core Find Functionality
- [x] FR1: Cascade lookup - cache → GitHub → PyPI
- [x] FR2: Cache storage and retrieval
- [x] FR3: Version checking via from_version parameter
- [x] FR4: Auto-generation of basic documentation from PyPI
- [ ] FR5: Retry logic for transient network failures
- [ ] FR6: Rate limiting awareness for GitHub API
- [ ] FR7: Parallel fetching for performance optimization

### CLI Interface
- [x] FR10: pkgq find command
- [x] FR11: pkgq cache --list/--clear/--dir commands
- [x] FR12: JSON output format
- [x] FR13: Save to cache option
- [x] FR14: Verbose mode
- [ ] FR15: Batch processing for multiple packages
- [ ] FR16: Additional output formats (YAML, TOML)
- [ ] FR17: Offline mode indicator

### MCP Server
- [x] FR20: find_package tool exposed
- [x] FR21: Auto-save to cache
- [x] FR22: Version checking support
- [ ] FR23: Cache management tools exposed
- [ ] FR24: Batch operations via MCP
- [ ] FR25: Package search tool

### Skills Ecosystem
- [x] FR30: /pkgq:create skill implementation (instructional approach)
- [x] FR31: /pkgq:update skill implementation (instructional approach)
- [x] FR32: Project structure parsing (via LLM in skill instructions)
- [x] FR33: Metadata extraction from pyproject.toml (via LLM in skill instructions)
- [x] FR34: Changelog fetching from multiple sources (via LLM in skill instructions)
- [x] FR35: HISTORY.md generation (via LLM in skill instructions)
- [x] FR36: Migration guide creation (via LLM in skill instructions)

### Caching System
- [x] FR40: File-based cache storage
- [x] FR41: Package directory structure
- [x] FR42: Environment variable configuration (PKGQ_CACHE)
- [ ] FR43: Cache expiration/staleness detection
- [ ] FR44: Cache size management
- [ ] FR45: Cache validation/integrity checks
- [ ] FR46: Offline-first mode

### Documentation Quality
- [ ] FR50: pkgq lint command for documentation validation
- [ ] FR51: pkgq score command for quality assessment
- [ ] FR52: pkgq verify command for example/link validation
- [ ] FR53: Quality badges output for documentation

### Batch Operations
- [ ] FR54: pkgq find --requirements for requirements.txt parsing
- [ ] FR55: pkgq find --pyproject for pyproject.toml parsing
- [ ] FR56: pkgq cache export for cache portability
- [ ] FR57: pkgq cache import for cache restoration
- [ ] FR58: Parallel fetching for batch operations

### Configuration
- [ ] FR59: Shell completion generation (bash, zsh, fish)

## Non-Functional Requirements

### Performance
- [x] NFR1: Fast lookups with caching
- [ ] NFR2: Connection pooling configuration
- [ ] NFR3: Async operations support

### Reliability
- [x] NFR4: Basic HTTP error handling
- [ ] NFR5: Retry logic for transient failures
- [ ] NFR6: Fallback on partial failures
- [ ] NFR7: Graceful degradation

### Usability
- [ ] NFR10: Context-aware error messages
- [ ] NFR11: Resolution hints in error output
- [ ] NFR12: Progress reporting for long operations

### Maintainability
- [x] NFR20: Well-documented code with docstrings
- [x] NFR21: Type hints throughout
- [ ] NFR22: 90%+ test coverage
- [ ] NFR23: Integration tests for CLI and MCP
- [ ] NFR24: Mocked network tests

### Security
- [ ] NFR30: Markdown content sanitization
- [ ] NFR31: GitHub token support for authentication
- [ ] NFR32: Safe handling of external data

## Technical Requirements

### Code Quality
- [x] T1: Modern Python 3.10+ syntax
- [x] T2: Type hints with union syntax (X | None)
- [x] T3: Two-space indentation
- [x] T4: ruff linting compliance
- [ ] T5: Remove or use pydantic dependency
- [ ] T6: Sync plugin.json version with package version

### Documentation
- [x] D1: README.md with installation and usage
- [x] D2: PACKAGE.md with API documentation
- [x] D3: CLAUDE.md with development guidance
- [ ] D4: Troubleshooting guide
- [ ] D5: CONTRIBUTING.md
- [ ] D6: Update README to reflect actual capabilities
- [ ] D7: ReadTheDocs documentation site with API reference
- [ ] D8: GitHub Pages promotional site for PACKAGE.md concept
- [ ] D9: Package registry for discovering agent-ready packages

### Infrastructure
- [x] I1: PyPI package published
- [x] I2: GitHub Actions CI
- [x] I3: Test coverage reporting (Coveralls)
- [x] I4: Makefile for common tasks
- [ ] I5: GitHub API token configuration

## Completed

- [x] FR1-FR4: Core find functionality (v0.1.0)
- [x] FR10-FR14: CLI interface (v0.1.0)
- [x] FR20-FR22: MCP server basics (v0.1.0)
- [x] FR30-FR36: Skills ecosystem with instructional approach (v0.2.0)
  - Skills use SKILL.md instructions for LLM-driven generation
  - Retrieval operations in code, generation operations via LLM
- [x] FR40-FR42: Basic caching (v0.1.0)
- [x] NFR20-NFR21: Documentation and typing (v0.1.0)
- [x] T1-T4: Code quality standards (v0.1.0)
- [x] D1-D3: Core documentation (v0.1.0)
- [x] I1-I4: Basic infrastructure (v0.1.0)