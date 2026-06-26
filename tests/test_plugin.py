"""
Tests for yoker plugin integration.
"""

import pytest

from pkgq.plugin import __YOKER_MANIFEST__, yoker_tool_find


class TestPluginManifest:
  """Test yoker plugin manifest."""

  def test_manifest_exists(self):
    """Plugin manifest is defined."""
    assert __YOKER_MANIFEST__ is not None

  def test_manifest_has_tools(self):
    """Plugin manifest includes tools."""
    assert len(__YOKER_MANIFEST__.tools) == 1
    assert __YOKER_MANIFEST__.tools[0] == yoker_tool_find

  def test_manifest_has_skills_dir(self):
    """Plugin manifest specifies skills directory."""
    assert __YOKER_MANIFEST__.skills_dir == "skills"


class TestYokerToolFind:
  """Test yoker_tool_find wrapper function."""

  def test_tool_name(self):
    """Tool has correct yoker name."""
    assert yoker_tool_find.__yoker_name__ == "find"

  def test_tool_docstring(self):
    """Tool has docstring."""
    assert yoker_tool_find.__doc__ is not None
    assert "package" in yoker_tool_find.__doc__.lower()

  @pytest.mark.integration
  def test_tool_returns_string(self):
    """Tool returns string content."""
    # This is an integration test that requires network access
    # Marked with @pytest.mark.integration
    result = yoker_tool_find("yoker")
    assert isinstance(result, str)
    assert len(result) > 0