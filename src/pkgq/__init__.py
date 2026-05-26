"""
pkgq - Package Query

Find API information for Python packages.
"""

__version__ = "0.1.1"

from pkgq.find import FindResult, find

__all__ = ["find", "FindResult"]
