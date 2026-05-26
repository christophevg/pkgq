---
name: update
description: |
  Update existing package documentation for a new version.
  Fetches changelog, extracts changes, and updates PACKAGE.md and HISTORY.md.
  Use when planning upgrades or when new versions are released.
---

# Package Documentation Updater

Updates existing package documentation to reflect new versions, including migration guides.

## When to Use

- A new version of a dependency was released
- You're planning a dependency upgrade
- Documentation needs refreshing after changes
- Migration planning requires current version info

## Input

| Parameter | Required | Description |
|-----------|----------|-------------|
| package | Yes | Package name |
| version | No | Target version (defaults to latest) |
| from_version | No | Current version (for comparison) |

## Process

### 1. Check Local Cache

Verify existing documentation:

```
~/.cache/pkgq/packages/{package}/
├── PACKAGE.md        # Current docs
└── metadata.json     # Cache metadata
```

If missing, use `/pkgq:find` first to fetch documentation.

### 2. Fetch Latest Metadata

Query PyPI for latest version:

```python
import requests

# Get latest version
response = requests.get(f"https://pypi.org/pypi/{package}/json")
latest = response.json()["info"]["version"]

# Get specific version if requested
if version:
    response = requests.get(f"https://pypi.org/pypi/{package}/{version}/json")
```

### 3. Find Changelog

Check multiple sources:

**Priority order:**

1. **Changelog file in repository**
   - `CHANGELOG.md`
   - `HISTORY.md`
   - `CHANGES.md`
   - `NEWS.md`

2. **GitHub Releases**
   - API: `https://api.github.com/repos/{owner}/{repo}/releases`
   - Parse release notes

3. **PyPI description**
   - May contain version history

4. **Git tags**
   - `git log v1.0.0..v2.0.0 --oneline`
   - Extract commit messages

### 4. Parse Changelog

Extract structured information:

```markdown
## 2.1.0 (2026-05-15)

### New Features
- Dict-based configuration
- Tool registry system

### Breaking Changes
- Agent.run() now returns Response object

### Deprecations
- agent.stop_agent() → agent.stop()

### Bug Fixes
- Fixed async client timeout issue
```

**Extract:**
- New features
- Breaking changes
- Deprecations
- Bug fixes
- Migration notes

### 5. Update HISTORY.md

Prepend new version entry:

```markdown
# {Package} Version History

## 2.1.0 (2026-05-15)

### New Features
- **Dict-based configuration**: `Agent(config={...})` without file
- **Tool registry**: Register tools dynamically

### Breaking Changes
- `Agent.run()` returns `Response` object (was string)
  - Before: `result = agent.run(prompt)`
  - After: `response = agent.run(prompt); result = response.content`

### Deprecations
- `agent.stop_agent()` → `agent.stop()`

### Bug Fixes
- Fixed timeout issue in AsyncClient

---

## 2.0.0 (2026-04-01)
{Previous entry...}
```

### 6. Update PACKAGE.md

Update current documentation:

**Version Notes section:**
```markdown
## Version Notes

### 2.1.0

**New Features:**
- Dict-based configuration - Use `Agent(config={...})` without file
- Tool registry - Register tools with `agent.register_tool()`

**Improvements:**
- AsyncClient timeout handling improved

**Deprecations:**
- `stop_agent()` - Use `stop()` instead
```

**Migration Guides section:**
```markdown
## Migration Guides

### From 2.0.x to 2.1.x

No breaking changes. New features are opt-in.

### From 1.x to 2.x

**Breaking Changes:**
- `Agent.run()` returns `Response` object

```python
# Before (1.x)
result = agent.run(prompt)

# After (2.x)
response = agent.run(prompt)
result = response.content
```
```

**Common Patterns section:**
- Add new patterns for new features
- Update patterns for changed APIs

### 7. Update Metadata

Update cache metadata:

```json
{
  "package": "yoker",
  "version": "2.1.0",
  "cached": "2026-05-26T14:30:00Z",
  "source": "github:christophevg/yoker",
  "previous_version": "2.0.0"
}
```

## Version Comparison

When `from_version` is specified, provide comparison:

```markdown
## Upgrade Analysis: 2.0.0 → 2.1.0

### New Features Available
- Dict-based configuration (simplifies setup)
- Tool registry (dynamic registration)

### Breaking Changes
- None (backward compatible)

### Deprecations to Plan
- `stop_agent()` will be removed in 3.0

### Code Changes Needed
- None required for upgrade

### Recommended Actions
1. Update to 2.1.0 (no code changes needed)
2. Consider migrating to dict config for simpler setup
3. Replace `stop_agent()` with `stop()` before 3.0
```

## Output

Returns:

1. **Upgrade summary** - What changed
2. **Migration guide** - How to update code
3. **Recommendations** - What to do

## Example Usage

```bash
# Update to latest version
/pkgq:update package=yoker

# Update to specific version
/pkgq:update package=yoker version=2.1.0

# Compare versions for upgrade planning
/pkgq:update package=yoker from_version=1.5.0 version=2.1.0
```

## Integration with Agents

### project-manage

```python
# When planning dependency upgrade
# Use MCP tool: mcp__plugin_c3_pkgq__find_package
# with from_version parameter
```

### functional-analyst

```python
# When evaluating upgrade impact
# Use MCP tool: mcp__plugin_c3_pkgq__find_package
# with from_version and version parameters
```

### python-developer

```python
# Before implementing upgrade
# Use MCP tool: mcp__plugin_c3_pkgq__find_package
# Returns: version info, migration notes
```

## Changelog Sources

### GitHub Releases

```python
# Get releases from GitHub API
releases = requests.get(
    f"https://api.github.com/repos/{owner}/{repo}/releases"
)

for release in releases:
    version = release['tag_name']
    notes = release['body']
    # Parse notes for changes
```

### PyPI Description

```python
# Some packages include changelog in description
response = requests.get(f"https://pypi.org/pypi/{package}/json")
description = response.json()['info']['description']

# Parse description for version history
```

### Git History

```bash
# If repository available
git log v{old_version}..v{new_version} --oneline
git log v{old_version}..v{new_version} --format="%s"
```

## Handling Breaking Changes

For breaking changes, generate detailed migration guide:

```markdown
### Breaking: Agent.run() Return Type

**What changed:**
`Agent.run()` returns `Response` object instead of string.

**Before:**
```python
result = agent.run(prompt)
print(result)  # string
```

**After:**
```python
response = agent.run(prompt)
print(response.content)  # string
```

**Impact:**
- All calls to `agent.run()` need `.content` access
- Tests using `assert result == "expected"` need update

**Migration:**
```bash
# Find affected code
grep -r "\.run(" --include="*.py"

# Update pattern
s/(\w+)\.run\(([^)]+)\)/\1.run(\2).content/g
```
```

## Quality Checks

After update, verify:

- [ ] HISTORY.md has new entry
- [ ] PACKAGE.md reflects current version
- [ ] Migration guides are accurate
- [ ] Breaking changes clearly documented
- [ ] Code examples still work

## Notes

- Works for packages with proper changelogs
- Falls back to git commit history if no changelog
- May not find changes for poorly maintained packages
- Use `mcp__plugin_c3_pkgq__find_package` to get documentation