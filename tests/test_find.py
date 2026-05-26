"""Tests for pkgq find module."""

import pytest

from pkgq.find import get_cache_dir, check_cached


def test_get_cache_dir_default():
    """Test default cache directory."""
    cache_dir = get_cache_dir()
    assert ".cache" in str(cache_dir)
    assert "pkgq" in str(cache_dir)


def test_get_cache_dir_env(monkeypatch, tmp_path):
    """Test custom cache directory from environment."""
    monkeypatch.setenv("PKGQ_CACHE", str(tmp_path))
    cache_dir = get_cache_dir()
    assert cache_dir == tmp_path


def test_check_cached_not_found(tmp_path):
    """Test check_cached when package is not cached."""
    result = check_cached("nonexistent", tmp_path)
    assert result is None


def test_check_cached_found(tmp_path):
    """Test check_cached when package is cached."""
    import json
    from pkgq.find import FindResult

    # Create cached package
    package_dir = tmp_path / "testpkg"
    package_dir.mkdir()

    package_file = package_dir / "PACKAGE.md"
    package_file.write_text("# testpkg\n\nTest package.")

    metadata_file = package_dir / "metadata.json"
    metadata_file.write_text(json.dumps({
        "package": "testpkg",
        "version": "1.0.0",
        "source": "test",
    }))

    # Check cache
    result = check_cached("testpkg", tmp_path)
    assert result is not None
    assert result.package == "testpkg"
    assert result.version == "1.0.0"
    assert result.cached is True