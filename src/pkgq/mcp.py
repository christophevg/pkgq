"""
pkgq MCP Server - Model Context Protocol server for package query.

Provides a simple tool to find package documentation.
"""

from typing import Annotated

from fastmcp import FastMCP

from pkgq import find

# Create MCP server
mcp = FastMCP(
    name="pkgq",
    version="0.1.0",
)


@mcp.tool()
def find_package(
    package: Annotated[str, "Package name to find"],
    version: Annotated[str | None, "Desired version (default: latest)"] = None,
    from_version: Annotated[str | None, "Current cached version (for update check)"] = None,
) -> str:
    """Find package documentation.

    Queries multiple sources in order:
    1. Local cache (if from_version is provided)
    2. GitHub repository (PACKAGE.md)
    3. Generate from PyPI docs

    Args:
        package: Package name (e.g., "yoker", "httpx")
        version: Desired version (default: latest)
        from_version: Current cached version (for update check)

    Returns:
        Package documentation in PACKAGE.md format
    """
    result = find(
        package=package,
        version=version,
        from_version=from_version,
        verbose=True,  # Include source information
    )

    # Return formatted result
    status = "cached" if result.cached else "fetched"
    header = f"# {result.package} (v{result.version}) [{status}]\n\n"
    header += f"Source: {result.source}\n\n---\n\n"

    return header + result.content


def run():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    run()
