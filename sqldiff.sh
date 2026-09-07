#!/bin/sh
# Show a sqldiff between a GeoPackage/SQLite file's working tree copy and its version at REV
# (default: HEAD). Requires the sqldiff tool (part of the sqlite3-tools package).

# Usage: ./sqldiff.sh <path> [rev]
# Example: ./sqldiff.sh schema/data_formats/geopackage/network-schema.gpkg
# Example: ./sqldiff.sh examples/geopackage/network.gpkg
set -eu

path="$1"
rev="${2-HEAD}"

old=$(mktemp)
trap 'rm -f "$old"' EXIT

git show "$rev:$path" > "$old"
sqldiff "$old" "$path"
