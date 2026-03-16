#!/bin/bash
# Generate docs/index.html from the essay Markdown file.
# The MD file is the single source of truth — run this after any text edits.

set -e

cd "$(dirname "$0")"
python3 build-html.py
