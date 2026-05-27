# TODO

## Backlog

### Design Principles

**Architectural Decision**: LLM-Driven Documentation Generation

The `/pkgq:create` and `/pkgq:update` skills follow an **instructional approach** rather than a coded implementation. This reflects a core architectural principle:

- **Retrieval/Find Operations**: Implemented in code (deterministic, fast, structured data)
- **Generation/Create/Update Operations**: Implemented as LLM instructions (creative, flexible, context-aware)

This separation leverages the strengths of each approach:
- Code excels at API calls, caching, and data retrieval
- LLMs excel at understanding project context, extracting patterns, and generating documentation

Skills provide structured guidance (SKILL.md files) that LLMs follow, avoiding the complexity of parsing code, extracting metadata programmatically, and generating documentation templates. The LLM naturally understands project structure, can ask clarifying questions, and adapts to project-specific conventions.

---

### Iteration 1: Test Coverage Foundation

Goal: Establish comprehensive test coverage to enable safe refactoring and feature additions.

- [ ] **I1-001: Add test fixtures for network mocking**
  - Create fixtures for PyPI API responses
  - Create fixtures for GitHub API responses
  - Create fixtures for PACKAGE.md content
  - **Delivers**: Reliable test infrastructure
  - **Satisfies**: NFR22, NFR24
  - **Acceptance**: Tests run without network calls, repeatable results

- [ ] **I1-002: Implement unit tests for find.py**
  - Test cascade lookup logic
  - Test cache checking
  - Test GitHub URL parsing
  - Test PyPI info extraction
  - **Delivers**: Core functionality verified
  - **Satisfies**: NFR22
  - **Acceptance**: >80% coverage of find.py

- [ ] **I1-003: Implement CLI integration tests**
  - Test `pkgq find` command with various options
  - Test `pkgq cache` commands
  - Test error output formatting
  - **Delivers**: CLI functionality verified
  - **Satisfies**: NFR23
  - **Acceptance**: All CLI commands tested, errors captured

- [ ] **I1-004: Implement MCP server tests**
  - Test find_package tool
  - Test auto-save behavior
  - Test error responses
  - **Delivers**: MCP functionality verified
  - **Satisfies**: NFR23
  - **Acceptance**: MCP tool behavior validated

**Result**: Test suite with >80% coverage, safe to refactor and add features.

---

### Iteration 2: Error Handling Overhaul

Goal: Improve user experience with clear, actionable error messages and resilience.

**Design Principle: Graceful Degradation**

The cascade lookup (cache → GitHub → PyPI) should handle failures at each step gracefully:
- Cache failure → Log warning, proceed to GitHub
- GitHub failure → Log warning, proceed to PyPI
- PyPI failure → Return PackageNotFoundError with helpful context

Users should never see internal errors from individual cascade steps - only the final outcome. Implementation should use try/except at each step with logging, not let exceptions propagate.

---

- [ ] **I2-001: Create custom exception types**
  - PackageNotFoundError
  - NetworkError
  - CacheError
  - GitHubRateLimitError
  - **Design Principle**: Exceptions should capture context (package name, attempted source, underlying error) for actionable messages
  - **Delivers**: Structured error handling
  - **Satisfies**: NFR10
  - **Acceptance**: All errors use custom types with context

- [ ] **I2-002: Implement retry logic for network operations**
  - Retry on transient failures (timeouts, 5xx errors)
  - Exponential backoff
  - Configurable retry count
  - **Design Principle**: Wrap network calls at the cascade step level, not globally - allows different retry strategies per source
  - **Delivers**: Resilient network operations
  - **Satisfies**: FR5, NFR5, NFR6
  - **Acceptance**: Tests verify retry behavior at each cascade step

- [ ] **I2-003: Add context-aware error messages**
  - Include resolution hints
  - Link to documentation
  - Suggest alternatives when package not found
  - **Design Principle**: Errors should guide users to resolution, not just report problems. "Package 'yoker' not found. Tried: cache, GitHub, PyPI. Check spelling or run `pkgq create` if this is your package."
  - **Delivers**: Actionable error output
  - **Satisfies**: NFR10, NFR11
  - **Acceptance**: User testing shows clear resolution path

- [ ] **I2-004: Add GitHub rate limit handling**
  - Detect rate limit exceeded
  - Show time until reset
  - Suggest authentication option
  - **Design Principle**: Rate limits are expected, not exceptional - handle gracefully and inform user of options (wait or authenticate)
  - **Delivers**: Graceful handling of API limits
  - **Satisfies**: FR6
  - **Acceptance**: Clear message when rate limited with time and auth suggestion

**Result**: Users get helpful errors with clear resolution paths.

---

### Iteration 3: Documentation Quality

Goal: Provide tools to validate and score package documentation quality for agent-readiness.

**Design Principle: Agent-Readiness Assessment**

The quality commands help maintainers ensure their PACKAGE.md is optimized for AI agent consumption:
- **lint**: Check structure, required sections, formatting issues
- **score**: Assess completeness, clarity, agent-usefulness
- **verify**: Validate examples, code snippets, links

These tools support the ecosystem goal of making packages agent-discoverable and agent-usable.

---

- [ ] **I3-001: Implement `pkgq lint <package>` command**
  - Check for required sections (Installation, Usage, API Reference)
  - Validate markdown structure and formatting
  - Detect missing or incomplete sections
  - Output linting errors with severity levels
  - **Design Principle**: Clear, actionable feedback - not just "missing section" but "Missing 'Usage' section. Add examples showing common use cases."
  - **Delivers**: Documentation quality validation
  - **Satisfies**: FR50
  - **Acceptance**: `pkgq lint yoker` reports issues with fix suggestions

- [ ] **I3-002: Implement `pkgq score <package>` command**
  - Score documentation on completeness (0-100)
  - Break down by category: structure, examples, API coverage
  - Compare against best practices from high-quality PACKAGE.md files
  - Output actionable improvement suggestions
  - **Design Principle**: Gamification drives improvement - show "Your score: 72/100. Add API examples to reach 85."
  - **Delivers**: Quality metrics for maintainers
  - **Satisfies**: FR51
  - **Acceptance**: `pkgq score yoker` shows score breakdown and suggestions

- [ ] **I3-003: Implement `pkgq verify <package>` command**
  - Validate code examples are syntactically correct
  - Check that imports resolve to existing modules
  - Verify links (URLs, relative paths)
  - Report broken or outdated references
  - **Design Principle**: Trust but verify - agents will try to use the examples, ensure they work
  - **Delivers**: Documentation correctness validation
  - **Satisfies**: FR52
  - **Acceptance**: `pkgq verify yoker` checks examples and links

- [ ] **I3-004: Add quality badges output option**
  - Generate markdown badges for documentation scores
  - Support embedding in README.md or PACKAGE.md
  - Show lint status, score, verification status
  - **Delivers**: Visibility for package quality
  - **Satisfies**: FR53
  - **Acceptance**: `pkgq score yoker --badge` outputs markdown badge

**Result**: Maintainable, high-quality documentation with measurable standards.

---

### Iteration 4: Batch Operations

Goal: Enable efficient multi-package operations for teams and CI/CD workflows.

**Design Principle: Dependency-Aware Operations**

Batch operations should understand project context:
- Read from requirements.txt, pyproject.toml, poetry.lock
- Respect dependency groups (dev, test, optional)
- Enable cache portability for air-gapped environments

---

- [ ] **I4-001: Implement `pkgq find --requirements <file>` command**
  - Parse requirements.txt, requirements-dev.txt
  - Find documentation for all packages
  - Support --save to populate cache
  - Report progress and summary
  - **Design Principle**: One command to warm cache for entire project
  - **Delivers**: Project-wide documentation retrieval
  - **Satisfies**: FR15, FR54
  - **Acceptance**: `pkgq find --requirements requirements.txt --save` caches all project deps

- [ ] **I4-002: Implement `pkgq find --pyproject <file>` command**
  - Parse pyproject.toml dependencies
  - Support dependency groups (project.dependencies, dev, optional)
  - Filter by group with `--group` flag
  - Handle Poetry and setuptools formats
  - **Design Principle**: Modern Python projects use pyproject.toml - support it natively
  - **Delivers**: pyproject-aware batch operations
  - **Satisfies**: FR55
  - **Acceptance**: `pkgq find --pyproject pyproject.toml --group dev` finds dev deps

- [ ] **I4-003: Implement `pkgq cache export` command**
  - Export cached packages to archive (tar.gz)
  - Include all PACKAGE.md and metadata.json files
  - Support selective export by package list
  - Generate manifest of exported packages
  - **Design Principle**: Enable cache portability for CI/CD and air-gapped environments
  - **Delivers**: Cache portability
  - **Satisfies**: FR56
  - **Acceptance**: `pkgq cache export packages.tar.gz` creates portable archive

- [ ] **I4-004: Implement `pkgq cache import` command**
  - Import cached packages from archive
  - Validate imported content
  - Merge with existing cache (skip or overwrite options)
  - Report import summary
  - **Design Principle**: Import should be safe-by-default, merge intelligently
  - **Delivers**: Cache restoration capability
  - **Satisfies**: FR57
  - **Acceptance**: `pkgq cache import packages.tar.gz` restores cached packages

- [ ] **I4-005: Add parallel fetching for batch operations**
  - Fetch multiple packages concurrently
  - Configurable concurrency limit (default: 5)
  - Progress reporting during batch operations
  - Handle individual failures gracefully
  - **Design Principle**: Fast but not overwhelming - respect rate limits
  - **Delivers**: Efficient batch processing
  - **Satisfies**: NFR3, FR58
  - **Acceptance**: Batch operations complete faster with parallel fetching

**Result**: Efficient project-wide documentation management.

---

### Iteration 5: Cache Enhancement

Goal: Improve cache reliability and management.

**Security Principle: Safe-by-Default MCP Tools**

MCP tools should follow the principle of least privilege:
- **Expose**: Lookup (find), creational (save), and informational (list, validate) operations
- **Never expose**: Destructive operations (delete, clear, purge) - these require explicit CLI commands

This prevents accidental data loss from automated agents and ensures destructive operations are intentional, user-initiated actions.

---

- [ ] **I5-001: Implement staleness indicator report**
  - Check cached packages for newer versions on PyPI/GitHub
  - Report which packages have updates available
  - Show current version vs latest version
  - **Security Principle**: Read-only operation - safe to expose via MCP
  - **Delivers**: Cache freshness visibility
  - **Acceptance**: `pkgq cache stale` lists packages with available updates

- [ ] **I5-002: Implement upgrade cached documentation**
  - Add `pkgq cache upgrade` command for bulk refresh
  - Support upgrading all packages or specified packages
  - Show progress during upgrades
  - **Security Principle**: Creational operation (overwrite) - acceptable for MCP as it's already exposed via save parameter
  - **Delivers**: Easy cache maintenance
  - **Acceptance**: `pkgq cache upgrade --all` refreshes all cached packages

- [ ] **I5-003: Implement cache validation**
  - Verify PACKAGE.md exists and is readable
  - Check metadata.json is valid JSON with required fields
  - Report corrupted entries with actionable guidance
  - **Security Principle**: Read-only diagnostic - safe to expose via MCP
  - **Delivers**: Reliable cache
  - **Acceptance**: `pkgq cache validate` detects and reports issues, MCP tool available

- [ ] **I5-004: Add cache source indicator**
  - Show where documentation came from (cache, GitHub, PyPI)
  - Display cache age for cached entries
  - Include source info in output metadata
  - **Security Principle**: Read-only metadata - safe to expose via MCP
  - **Delivers**: Transparency about data provenance
  - **Acceptance**: Output shows source and age for all packages

**Result**: Robust caching with visibility and management tools.

---

### Iteration 6: Advanced Features

Goal: Enhance capabilities for power users and integrations.

- [ ] **I6-001: Implement batch package lookup**
  - Accept multiple package names
  - Parallel fetching
  - Progress reporting
  - **Delivers**: Efficient multi-package operations
  - **Satisfies**: FR15, NFR3
  - **Acceptance**: Multiple packages fetched efficiently

- [ ] **I6-002: Add additional output formats**
  - YAML output format
  - TOML output format
  - Structured JSON schema
  - **Delivers**: Integration flexibility
  - **Satisfies**: FR16
  - **Acceptance**: All formats validated

- [ ] **I6-003: Implement GitHub token support**
  - Environment variable configuration
  - Authenticated API requests
  - Higher rate limits
  - **Delivers**: Reduced rate limiting issues
  - **Satisfies**: FR6, NFR31
  - **Acceptance**: Authenticated requests working

- [ ] **I6-004: Add MCP cache management tools**
  - Expose cache list tool (read-only)
  - Expose cache validate tool (read-only)
  - **Security Principle**: No destructive operations via MCP - only lookup and creational actions
  - **Delivers**: Safe MCP cache visibility
  - **Satisfies**: FR23
  - **Acceptance**: Cache list and validate available via MCP, no destructive operations exposed

- [ ] **I6-005: Implement `pkgq --version` command**
  - Display package version
  - Support both short (`-V`) and long (`--version`) flags
  - **Delivers**: Quick version check for users and scripts
  - **Acceptance**: `pkgq --version` outputs version number

- [ ] **I6-006: Implement `pkgq add <package>` shorthand**
  - Shorthand for `pkgq find <package> --save`
  - Save package documentation to cache
  - **Delivers**: Convenient cache population
  - **Acceptance**: `pkgq add yoker` finds and saves documentation

- [ ] **I6-007: Implement `pkgq remove <package>` command**
  - Remove package from cache
  - Confirm before deletion (optional `--force` to skip)
  - **Delivers**: Cache management convenience
  - **Acceptance**: `pkgq remove yoker` removes from cache with confirmation

- [ ] **I6-008: Implement `pkgq show <package>` command**
  - Display package documentation with pager (less)
  - Fall back to stdout if pager unavailable
  - Support `--no-pager` flag for direct output
  - **Delivers**: Comfortable documentation reading
  - **Acceptance**: `pkgq show yoker` opens docs in pager

- [ ] **I6-009: Implement shell completion**
  - Generate completion scripts for bash, zsh, fish
  - Command: `pkgq completion <shell>`
  - Support `--install` flag for automatic installation
  - Complete package names from cache and PyPI
  - **Design Principle**: Smooth developer experience with tab completion
  - **Delivers**: CLI usability enhancement
  - **Satisfies**: FR59
  - **Acceptance**: `pkgq completion bash` outputs bash completion script

**Result**: Enhanced capabilities for advanced usage.

---

### Iteration 7: Documentation & Polish

Goal: Complete documentation and resolve technical debt.

- [ ] **I7-001: Update documentation to match implementation**
  - Update README with actual capabilities
  - Document limitations clearly
  - Add troubleshooting guide
  - **Delivers**: Accurate documentation
  - **Satisfies**: D4, D6
  - **Acceptance**: No gaps between docs and code

- [ ] **I7-002: Create contributing guide**
  - Development setup
  - Testing guidelines
  - PR requirements
  - **Delivers**: Clear contribution path
  - **Satisfies**: D5
  - **Acceptance**: New contributors can start easily

- [ ] **I7-003: Resolve technical debt**
  - Remove or use pydantic dependency
  - Sync plugin.json version
  - Standardize serialization
  - **Delivers**: Clean codebase
  - **Satisfies**: T5, T6
  - **Acceptance**: No unresolved debt items

**Result**: Production-ready project with complete documentation.

---

### Iteration 8: Documentation Sites

Goal: Publish documentation and promotional sites to increase visibility and adoption.

- [ ] **I8-001: Set up ReadTheDocs documentation site**
  - Configure ReadTheDocs project
  - Set up Sphinx or MkDocs documentation
  - Create API reference from docstrings
  - Write usage guides and tutorials
  - Configure auto-deploy on release
  - **Delivers**: Professional technical documentation site
  - **Satisfies**: D7
  - **Acceptance**: https://pkgq.readthedocs.io live with API docs and guides

- [ ] **I8-002: Create GitHub Pages promotional site**
  - Design landing page explaining PACKAGE.md concept
  - Create "Why make your package agent-discoverable?" section
  - Add testimonials/use cases from real packages
  - Include step-by-step guide for maintainers
  - Link to skills for easy adoption
  - Reference https://agents.md as inspiration
  - Configure GitHub Actions for deployment
  - **Delivers**: Promotional site driving adoption
  - **Satisfies**: D8
  - **Acceptance**: https://c3-ls.github.io/pkgq live with compelling content

- [ ] **I8-003: Document non-coding-agent entry point**
  - Create step-by-step tutorial for non-technical users
  - Document yoker + ollama workflow for free LLM usage
  - Show how to query package documentation without coding knowledge
  - Include screenshots or diagrams of the workflow
  - **Design Principle**: Accessible to non-developers - clear language, no jargon, practical examples
  - **Delivers**: Low-barrier entry for all users
  - **Acceptance**: Tutorial guides non-coding user from zero to querying packages with free tools

**Result**: Dual documentation presence - technical docs on ReadTheDocs, promotional site on GitHub Pages with package registry.

---

## Future Considerations

The following features have been identified as potentially valuable but are deferred for future evaluation. They may be added to a future iteration based on user feedback and ecosystem needs.

### Health & Monitoring Commands

**Principle**: These commands would provide proactive insights into package ecosystem health.

| Command | Purpose | Consideration |
|---------|---------|---------------|
| `pkgq health <package>` | Check package maintenance status, recent releases, issue activity | Requires additional API integration (GitHub Issues, release cadence analysis) |
| `pkgq outdated` | List cached packages with newer versions available | Iteration 5's staleness report covers similar ground; evaluate if separate command needed |
| `pkgq audit <package>` | Security vulnerability scan of dependencies | Scope creep into security tools; consider integration with `pip-audit` or similar instead |

**Decision Criteria for Inclusion**:
- Clear user demand demonstrated
- Fits within pkgq's core mission (documentation, not security or monitoring)
- Does not duplicate existing tools in the ecosystem

---

## Done

- [x] **v0.1.0: Initial implementation**
  - Core find functionality
  - CLI interface
  - MCP server
  - Basic caching
  - Documentation

- [x] **v0.2.0: Plugin and CI**
  - Plugin structure
  - GitHub Actions CI
  - Coverage reporting
  - Save parameter for MCP tool