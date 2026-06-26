"""
Yoker plugin integration for pkgq.

This module provides the yoker plugin manifest and tool wrappers
for integrating pkgq with the yoker agent harness.
"""

from yoker.plugins import PluginManifest

from pkgq.find import find


def yoker_tool_find(
  package: str,
  version: str | None = None,
  from_version: str | None = None,
) -> str:
  """
  Find Python package documentation.

  Args:
    package: Package name to find
    version: Desired version (default: latest)
    from_version: Current cached version (for update check)

  Returns:
    Package documentation content as string
  """
  result = find(package, version, from_version)
  return result.content


yoker_tool_find.__yoker_name__ = "find"  # type: ignore[attr-defined]


__YOKER_MANIFEST__ = PluginManifest(
  tools=[yoker_tool_find],
  skills_dir="skills",
)

__all__ = ["__YOKER_MANIFEST__", "yoker_tool_find"]

