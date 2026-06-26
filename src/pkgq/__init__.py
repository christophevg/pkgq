"""
pkgq - Package Query

Find API information for Python packages.
"""

__version__ = "0.3.0"

from pkgq.find import FindResult, find
from pkgq.plugin import __YOKER_MANIFEST__

__all__ = ["find", "FindResult", "__YOKER_MANIFEST__"]
