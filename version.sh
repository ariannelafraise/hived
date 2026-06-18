#!/usr/bin/env bash

set -euo pipefail

# x.y.z format
VERSION="$1"

# __version__.py
sed -i -E 's/__version__ = "[^"]+"/__version__ = "'"$VERSION"'"/' __version__.py
# api/pyproject.toml
sed -i -E 's/version = "[^"]+"/version = "'"$VERSION"'"/' api/pyproject.toml

echo "Changed to $VERSION"
